import os
# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

from waifuc.action import NoMonochromeAction, FilterSimilarAction, \
    TaggingAction, PersonSplitAction, FaceCountAction, FirstNSelectAction, \
    CCIPAction, ModeConvertAction, ClassFilterAction, RandomFilenameAction, AlignMinSizeAction
from waifuc.export import TextualInversionExporter
from waifuc.source import DanbooruSource
from complete_character_list import all_characters, character_names

def crawl_character(character_tag, character_name, output_dir, use_ai=True, max_images=100):
    """
    爬取单个角色的图片
    
    Args:
        character_tag: 角色标签，如 'dan_heng_(honkai:_star_rail)'
        character_name: 角色中文名称，如 '丹恒'
        output_dir: 输出目录
        use_ai: 是否使用AI处理
        max_images: 最大图片数量
    """
    print(f"开始爬取 {character_name} ({character_tag})...")
    
    # 创建角色专用目录
    character_dir = os.path.join(output_dir, f"{character_name}_dataset")
    
    # 创建Danbooru源
    s = DanbooruSource([character_tag])
    
    # 构建处理流水线
    actions = [
        # 以RGB色彩模式加载图像并将透明背景替换为白色背景
        ModeConvertAction('RGB', 'white'),

        # 图像预过滤
        NoMonochromeAction(),  # 丢弃单色、灰度或素描等单色图像
        ClassFilterAction(['illustration', 'bangumi']),  # 丢弃漫画或3D图像
        FilterSimilarAction('all'),  # 丢弃相似或重复的图像

        # 人像处理
        FaceCountAction(1),  # 丢弃没有人脸或有多个人脸的图像
        PersonSplitAction(),  # 将多人图像中每个人物裁出
        FaceCountAction(1),  # 丢弃裁出内容中没有人脸或有多个人脸的图像
    ]
    
    # 根据是否使用AI处理添加相应动作
    if use_ai:
        actions.extend([
            # CCIP，丢弃内容为非指定角色的图像
            CCIPAction(),
            # 使用wd14 v2进行标注
            TaggingAction(force=True),
        ])
    
    # 添加后续处理
    actions.extend([
        # 将短边大于1024像素的图像等比例调整至短边为1024像素
        AlignMinSizeAction(1024),
        FilterSimilarAction('all'),  # 再次丢弃相似或重复的图像
        FirstNSelectAction(max_images),  # 限制图片数量
        RandomFilenameAction(ext='.png'),  # 随机重命名图像
    ])
    
    # 执行爬取
    try:
        s.attach(*actions).export(
            TextualInversionExporter(character_dir)
        )
        print(f"✅ {character_name} 爬取完成，保存到: {character_dir}")
        return True
    except Exception as e:
        print(f"❌ {character_name} 爬取失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 星穹铁道角色批量爬取脚本 ===")
    print("支持的角色:")
    for i, tag in enumerate(all_characters, 1):
        name = character_names.get(tag, tag)
        print(f"{i:2d}. {name} ({tag})")
    
    print("\n选择爬取模式:")
    print("1. 带AI处理 (CCIP + Tagging)")
    print("2. 不使用AI处理 (更快)")
    
    mode = input("请选择模式 (1/2): ").strip()
    use_ai = mode == "1"
    
    # 设置输出目录
    base_dir = "F:/honkai_star_rail_characters"
    
    # 询问爬取数量
    try:
        max_images = int(input("每个角色爬取多少张图片? (默认100): ") or "100")
    except ValueError:
        max_images = 500
    
    # 询问是否爬取所有角色
    crawl_all = input("是否爬取所有角色? (y/n, 默认y): ").strip().lower()
    
    if crawl_all in ['n', 'no']:
        # 让用户选择特定角色
        print("\n请选择要爬取的角色 (输入数字，用逗号分隔):")
        selected_indices = input("角色编号: ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in selected_indices.split(',')]
            selected_characters = [(all_characters[i], character_names[all_characters[i]]) for i in indices if 0 <= i < len(all_characters)]
        except (ValueError, IndexError):
            print("输入格式错误，将爬取所有角色")
            selected_characters = [(tag, character_names[tag]) for tag in all_characters]
    else:
        selected_characters = [(tag, character_names[tag]) for tag in all_characters]
    
    print(f"\n开始批量爬取 {len(selected_characters)} 个角色...")
    print(f"输出目录: {base_dir}")
    print(f"AI处理: {'是' if use_ai else '否'}")
    print(f"每个角色图片数: {max_images}")
    
    # 创建基础目录
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # 统计结果
    success_count = 0
    total_count = len(selected_characters)
    
    # 开始爬取
    for i, (character_tag, character_name) in enumerate(selected_characters, 1):
        print(f"\n[{i}/{total_count}] 正在处理: {character_name}")
        if crawl_character(character_tag, character_name, base_dir, use_ai, max_images):
            success_count += 1
    
    # 输出总结
    print(f"\n=== 爬取完成 ===")
    print(f"成功: {success_count}/{total_count}")
    print(f"失败: {total_count - success_count}/{total_count}")
    print(f"输出目录: {base_dir}")

if __name__ == "__main__":
    main()
