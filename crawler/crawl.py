import os
# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

from waifuc.action import NoMonochromeAction, FilterSimilarAction, \
    TaggingAction, PersonSplitAction, FaceCountAction, FirstNSelectAction, \
    CCIPAction, ModeConvertAction, ClassFilterAction, RandomFilenameAction, AlignMinSizeAction
from waifuc.export import TextualInversionExporter
from waifuc.source import DanbooruSource

if __name__ == '__main__':
    # 选择爬取模式
    mode = input("选择爬取模式 (1: phainon, 2: mydei): ")
    
    if mode == "1":
        # 原版本：phainon_(honkai:_star_rail) 带AI处理
        print("爬取 phainon_(honkai:_star_rail) 带AI处理...")
        s = DanbooruSource(['phainon_(honkai:_star_rail)'])
        
        s.attach(
            # 以RGB色彩模式加载图像并将透明背景替换为白色背景
            ModeConvertAction('RGB', 'white'),

            # 图像预过滤
            NoMonochromeAction(),  # 丢弃单色、灰度或素描等单色图像
            ClassFilterAction(['illustration', 'bangumi']),  # 丢弃漫画或3D图像
            # RatingFilterAction(['safe', 'r15']),  # 可选，丢弃非全年龄或R15的图像
            FilterSimilarAction('all'),  # 丢弃相似或重复的图像

            # 人像处理
            FaceCountAction(1),  # 丢弃没有人脸或有多个人脸的图像
            PersonSplitAction(),  # 将多人图像中每个人物裁出
            FaceCountAction(1),  # 丢弃裁出内容中没有人脸或有多个人脸的图像

            # CCIP，丢弃内容为非指定角色的图像
            CCIPAction(),

            # 将短边大于800像素的图像等比例调整至短边为800像素
            AlignMinSizeAction(1024),

            # 使用wd14 v2进行标注，如果不需要角色标注，将character_threshold设置为1.01
            TaggingAction(force=True),

            FilterSimilarAction('all'),  # 再次丢弃相似或重复的图像
            FirstNSelectAction(100),  # 当已有100张图像到达此步骤时，停止后继图像处理
            # MirrorAction(),  # 可选，镜像处理图像进行数据增强
            RandomFilenameAction(ext='.png'),  # 随机重命名图像
        ).export(
            # 保存到F:/data/phainon_dataset目录
            TextualInversionExporter('F:/data/phainon_dataset')
        )
        
    elif mode == "2":
        # 新版本：mydei_(honkai:_star_rail) 不使用AI处理
        print("爬取 mydei_(honkai:_star_rail) 不使用AI处理...")
        s = DanbooruSource(['mydei_(honkai:_star_rail)'])
        
        s.attach(
            # 以RGB色彩模式加载图像并将透明背景替换为白色背景
            ModeConvertAction('RGB', 'white'),

            # 图像预过滤
            NoMonochromeAction(),  # 丢弃单色、灰度或素描等单色图像
            ClassFilterAction(['illustration', 'bangumi']),  # 丢弃漫画或3D图像
            # RatingFilterAction(['safe', 'r15']),  # 可选，丢弃非全年龄或R15的图像
            FilterSimilarAction('all'),  # 丢弃相似或重复的图像

            # 人像处理
            FaceCountAction(1),  # 丢弃没有人脸或有多个人脸的图像
            PersonSplitAction(),  # 将多人图像中每个人物裁出
            FaceCountAction(1),  # 丢弃裁出内容中没有人脸或有多个人脸的图像

            # 不使用CCIP和TaggingAction，跳过AI处理

            # 将短边大于800像素的图像等比例调整至短边为800像素
            AlignMinSizeAction(1024),

            FilterSimilarAction('all'),  # 再次丢弃相似或重复的图像
            FirstNSelectAction(1000),  # 当已有100张图像到达此步骤时，停止后继图像处理
            # MirrorAction(),  # 可选，镜像处理图像进行数据增强
            RandomFilenameAction(ext='.png'),  # 随机重命名图像
        ).export(
            # 保存到F:/data/mydei_dataset目录
            TextualInversionExporter('F:/data/mydei_dataset')
        )
        
    else:
        print("无效选择，请重新运行程序")