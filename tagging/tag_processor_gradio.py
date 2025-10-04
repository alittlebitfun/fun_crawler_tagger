import gradio as gr
import os
import glob
from collections import Counter
import re
import shutil
from datetime import datetime

class TagProcessor:
    def __init__(self):
        self.default_path = r"C:\Users\DINGDASHI\Pictures\模型\code\data\surtr_dataset"
        self.current_tags = []
        self.tag_counts = {}
        self.preset_tags = self.load_preset_tags()
        
    def load_preset_tags(self):
        """从预设文件夹中加载所有预设标签文件"""
        preset_tags = {}
        preset_dir = "预设"
        
        # 检查预设文件夹是否存在
        if not os.path.exists(preset_dir):
            print(f"预设文件夹 '{preset_dir}' 不存在")
            return preset_tags
        
        # 获取预设文件夹中的所有txt文件
        preset_files = glob.glob(os.path.join(preset_dir, "*.txt"))
        
        for file_path in preset_files:
            # 获取文件名（不含扩展名）作为类别名
            category_name = os.path.splitext(os.path.basename(file_path))[0]
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tags = [line.strip() for line in f.readlines() if line.strip()]
                    preset_tags[category_name] = tags
                    print(f"已加载预设文件: {category_name} ({len(tags)}个标签)")
            except Exception as e:
                print(f"加载预设文件 {file_path} 时出错: {e}")
                preset_tags[category_name] = []
        
        return preset_tags
    
    def create_backup(self, directory_path, operation_description="", include_subfolders=False):
        """创建备份文件夹并备份所有txt文件"""
        backup_dir = os.path.join(os.path.dirname(directory_path), "tag_backup")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = os.path.basename(directory_path)
        
        # 清理操作描述中的特殊字符，避免文件名问题
        clean_description = operation_description.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "")
        if clean_description:
            backup_subdir = os.path.join(backup_dir, f"{folder_name}_{clean_description}_{timestamp}")
        else:
            backup_subdir = os.path.join(backup_dir, f"{folder_name}_backup_{timestamp}")
        
        # 创建备份目录
        os.makedirs(backup_subdir, exist_ok=True)
        
        # 备份所有txt文件
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        backed_up = 0
        
        for file_path in txt_files:
            try:
                # 保持子文件夹结构
                if include_subfolders:
                    # 计算相对路径
                    rel_path = os.path.relpath(file_path, directory_path)
                    backup_path = os.path.join(backup_subdir, rel_path)
                    # 确保目标目录存在
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                else:
                    filename = os.path.basename(file_path)
                    backup_path = os.path.join(backup_subdir, filename)
                
                shutil.copy2(file_path, backup_path)
                backed_up += 1
            except Exception as e:
                print(f"备份文件 {file_path} 时出错: {e}")
        
        return backup_subdir, backed_up
        
    def get_txt_files(self, directory_path, include_subfolders=False):
        """获取目录下所有txt文件"""
        if not os.path.exists(directory_path):
            return []
        
        if include_subfolders:
            # 递归搜索所有子文件夹中的txt文件
            return glob.glob(os.path.join(directory_path, "**", "*.txt"), recursive=True)
        else:
            # 只搜索当前文件夹
            return glob.glob(os.path.join(directory_path, "*.txt"))
    
    def read_txt_content(self, file_path):
        """读取txt文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return ""
    
    def write_txt_content(self, file_path, content):
        """写入txt文件内容"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"写入文件 {file_path} 时出错: {e}")
            return False
    
    def parse_tags(self, content):
        """解析标签，用逗号分隔"""
        if not content:
            return []
        return [tag.strip() for tag in content.split(',') if tag.strip()]
    
    def join_tags(self, tags):
        """将标签列表用逗号连接"""
        return ', '.join(tags)
    
    def count_tags(self, directory_path, include_subfolders=False):
        """统计所有txt文件中的标签出现次数"""
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        all_tags = []
        
        for file_path in txt_files:
            content = self.read_txt_content(file_path)
            tags = self.parse_tags(content)
            all_tags.extend(tags)
        
        self.tag_counts = Counter(all_tags)
        self.current_tags = list(self.tag_counts.keys())
        
        # 按出现次数从多到少排序
        sorted_tags = sorted(self.tag_counts.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_tags
    
    def preview_delete_tags(self, directory_path, tags_to_delete, include_subfolders=False):
        """预览删除操作，返回删除统计信息"""
        if not tags_to_delete:
            return "没有选择要删除的标签", ""
        
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        delete_preview = []
        total_deleted_count = 0
        
        for file_path in txt_files:
            content = self.read_txt_content(file_path)
            tags = self.parse_tags(content)
            
            # 计算要删除的标签
            tags_to_remove = [tag for tag in tags if tag in tags_to_delete]
            if tags_to_remove:
                filename = os.path.basename(file_path)
                delete_preview.append(f"{filename}: 将删除 {len(tags_to_remove)} 个标签 - {', '.join(tags_to_remove)}")
                total_deleted_count += len(tags_to_remove)
        
        preview_text = f"删除预览：\n将影响 {len(delete_preview)} 个文件，总共删除 {total_deleted_count} 个标签\n\n详细列表：\n" + "\n".join(delete_preview)
        
        return preview_text, total_deleted_count
    
    def batch_delete_tags(self, directory_path, tags_to_delete, include_subfolders=False):
        """批量删除选中的标签"""
        if not tags_to_delete:
            return "没有选择要删除的标签"
        
        # 创建操作描述
        if len(tags_to_delete) <= 3:
            operation_desc = f"删除标签_{'_'.join(tags_to_delete[:3])}"
        else:
            operation_desc = f"删除标签_{len(tags_to_delete)}个"
        
        # 创建备份
        backup_dir, backed_up = self.create_backup(directory_path, operation_desc, include_subfolders)
        
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        deleted_count = 0
        processed_files = 0
        
        for file_path in txt_files:
            content = self.read_txt_content(file_path)
            tags = self.parse_tags(content)
            
            # 删除选中的标签
            original_count = len(tags)
            tags = [tag for tag in tags if tag not in tags_to_delete]
            deleted_count += original_count - len(tags)
            
            # 重新写入文件
            new_content = self.join_tags(tags)
            if self.write_txt_content(file_path, new_content):
                processed_files += 1
        
        return f"✅ 删除完成！\n📁 备份位置: {backup_dir}\n📊 成功处理 {processed_files} 个文件，删除了 {deleted_count} 个标签\n💾 已备份 {backed_up} 个文件"
    
    def add_prefix_suffix(self, directory_path, prefix="", suffix="", include_subfolders=False):
        """为整个文本内容添加前缀或后缀"""
        if not prefix and not suffix:
            return "请输入前缀或后缀"
        
        # 创建操作描述
        operation_desc = "添加前后缀"
        if prefix and suffix:
            operation_desc = f"添加前缀_{prefix}_后缀_{suffix}"
        elif prefix:
            operation_desc = f"添加前缀_{prefix}"
        elif suffix:
            operation_desc = f"添加后缀_{suffix}"
        
        # 创建备份
        backup_dir, backed_up = self.create_backup(directory_path, operation_desc, include_subfolders)
        
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        processed_files = 0
        
        for file_path in txt_files:
            content = self.read_txt_content(file_path)
            
            # 在整个文本内容前后添加前缀和后缀
            new_content = content
            if prefix:
                new_content = prefix + new_content
            if suffix:
                new_content = new_content + suffix
            
            # 重新写入文件
            if self.write_txt_content(file_path, new_content):
                processed_files += 1
        
        return f"✅ 添加完成！\n📁 备份位置: {backup_dir}\n📊 成功处理 {processed_files} 个文件\n💾 已备份 {backed_up} 个文件"
    
    def replace_tags(self, directory_path, old_tag, new_tag, include_subfolders=False):
        """替换标签"""
        if not old_tag or not new_tag:
            return "请输入要替换的标签和新标签"
        
        # 创建操作描述
        operation_desc = f"替换标签_{old_tag}_为_{new_tag}"
        
        # 创建备份
        backup_dir, backed_up = self.create_backup(directory_path, operation_desc, include_subfolders)
        
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        processed_files = 0
        replaced_count = 0
        
        for file_path in txt_files:
            content = self.read_txt_content(file_path)
            tags = self.parse_tags(content)
            
            # 替换标签
            original_count = len(tags)
            tags = [new_tag if tag == old_tag else tag for tag in tags]
            replaced_count += original_count - len([tag for tag in tags if tag != new_tag])
            
            # 重新写入文件
            new_content = self.join_tags(tags)
            if self.write_txt_content(file_path, new_content):
                processed_files += 1
        
    def replace_text_content(self, directory_path, old_text, new_text, include_subfolders=False):
        """整体文本搜索替换"""
        if not old_text:
            return "请输入要替换的文本"
        
        # 创建操作描述
        operation_desc = f"文本替换_{old_text}_为_{new_text}"
        
        # 创建备份
        backup_dir, backed_up = self.create_backup(directory_path, operation_desc, include_subfolders)
        
        txt_files = self.get_txt_files(directory_path, include_subfolders)
        processed_files = 0
        replaced_count = 0
        
        for file_path in txt_files:
            content = self.read_txt_content(file_path)
            
            # 计算替换次数
            original_count = content.count(old_text)
            if original_count > 0:
                # 执行文本替换
                new_content = content.replace(old_text, new_text)
                
                # 重新写入文件
                if self.write_txt_content(file_path, new_content):
                    processed_files += 1
                    replaced_count += original_count
        
        return f"✅ 文本替换完成！\n📁 备份位置: {backup_dir}\n📊 成功处理 {processed_files} 个文件，替换了 {replaced_count} 处文本\n💾 已备份 {backed_up} 个文件"

# 创建TagProcessor实例
processor = TagProcessor()

def update_tag_statistics(directory_path, include_subfolders):
    """更新标签统计"""
    if not directory_path:
        directory_path = processor.default_path
    
    sorted_tags = processor.count_tags(directory_path, include_subfolders)
    
    # 创建选项列表
    choices = []
    for tag, count in sorted_tags:
        choices.append(f"{tag} ({count}次)")
    
    return gr.CheckboxGroup(choices=choices, label="选择要删除的标签"), f"共找到 {len(sorted_tags)} 个不同的标签"

def preview_delete_operation(directory_path, selected_tags, include_subfolders):
    """预览删除操作"""
    if not directory_path:
        directory_path = processor.default_path
    
    # 从选择中提取标签名
    tags_to_delete = []
    for choice in selected_tags:
        # 提取标签名（去掉次数信息）
        tag_name = choice.split(' (')[0]
        tags_to_delete.append(tag_name)
    
    preview_text, total_count = processor.preview_delete_tags(directory_path, tags_to_delete, include_subfolders)
    return preview_text, total_count

def execute_delete_operation(directory_path, selected_tags, include_subfolders):
    """执行删除操作"""
    if not directory_path:
        directory_path = processor.default_path
    
    # 从选择中提取标签名
    tags_to_delete = []
    for choice in selected_tags:
        # 提取标签名（去掉次数信息）
        tag_name = choice.split(' (')[0]
        tags_to_delete.append(tag_name)
    
    result = processor.batch_delete_tags(directory_path, tags_to_delete, include_subfolders)
    return result

def get_preset_tags():
    """获取预设标签选项"""
    preset_choices = []
    for category, tags in processor.preset_tags.items():
        if tags:
            preset_choices.append(f"【{category}】({len(tags)}个标签)")
    
    return gr.CheckboxGroup(choices=preset_choices, label="选择预设删除标签")

def initialize_preset_tags():
    """初始化预设标签选项"""
    return get_preset_tags()

def preview_preset_delete(directory_path, selected_presets, include_subfolders):
    """预览预设删除操作"""
    if not directory_path:
        directory_path = processor.default_path
    
    if not selected_presets:
        return "没有选择预设标签", 0
    
    # 从选择中提取标签
    tags_to_delete = []
    for choice in selected_presets:
        category = choice.split('】')[0].replace('【', '')
        if category in processor.preset_tags:
            tags_to_delete.extend(processor.preset_tags[category])
    
    preview_text, total_count = processor.preview_delete_tags(directory_path, tags_to_delete, include_subfolders)
    return preview_text, total_count

def execute_preset_delete(directory_path, selected_presets, include_subfolders):
    """执行预设删除操作"""
    if not directory_path:
        directory_path = processor.default_path
    
    if not selected_presets:
        return "没有选择预设标签"
    
    # 从选择中提取标签
    tags_to_delete = []
    for choice in selected_presets:
        category = choice.split('】')[0].replace('【', '')
        if category in processor.preset_tags:
            tags_to_delete.extend(processor.preset_tags[category])
    
    result = processor.batch_delete_tags(directory_path, tags_to_delete, include_subfolders)
    return result

def add_prefix_suffix_to_tags(directory_path, prefix, suffix, include_subfolders):
    """添加前缀或后缀"""
    if not directory_path:
        directory_path = processor.default_path
    
    result = processor.add_prefix_suffix(directory_path, prefix, suffix, include_subfolders)
    return result

def replace_tag_in_files(directory_path, old_tag, new_tag, include_subfolders):
    """替换标签"""
    if not directory_path:
        directory_path = processor.default_path
    
    result = processor.replace_tags(directory_path, old_tag, new_tag, include_subfolders)
    return result

def replace_text_in_files(directory_path, old_text, new_text, include_subfolders):
    """整体文本搜索替换"""
    if not directory_path:
        directory_path = processor.default_path
    
    result = processor.replace_text_content(directory_path, old_text, new_text, include_subfolders)
    return result

# 创建Gradio界面
with gr.Blocks(title="标签处理工具") as demo:
    gr.Markdown("# 🏷️ 标签处理工具")
    gr.Markdown("用于处理txt文件中的标签，支持统计、安全删除、添加前缀后缀和替换功能")
    
    with gr.Tab("📊 标签统计与批量删除"):
        gr.Markdown("## 📊 标签统计与批量删除")
        
        with gr.Row():
            directory_input = gr.Textbox(
                label="📁 目录路径",
                value=processor.default_path,
                placeholder="请输入txt文件所在目录路径"
            )
            include_subfolders_checkbox = gr.Checkbox(
                label="📂 包含子文件夹",
                value=False,
                info="勾选后将递归搜索所有子文件夹中的txt文件"
            )
            stats_button = gr.Button("🔍 统计标签", variant="primary")
        
        with gr.Row():
            # 左侧：标签统计和选择
            with gr.Column():
                stats_output = gr.Textbox(label="📈 统计结果", interactive=False)
                tag_checkboxes = gr.CheckboxGroup(label="✅ 选择要删除的标签")
                
                with gr.Row():
                    preview_button = gr.Button("👁️ 预览删除", variant="secondary")
                    confirm_delete_button = gr.Button("🗑️ 确认删除", variant="stop")
                
                preview_output = gr.Textbox(label="👁️ 删除预览", interactive=False, lines=8)
                delete_output = gr.Textbox(label="✅ 删除结果", interactive=False)
            
            # 右侧：预设删除和其他功能
            with gr.Column():
                gr.Markdown("### 🎯 预设删除")
                preset_checkboxes = gr.CheckboxGroup(
                    choices=[f"【{category}】({len(tags)}个标签)" for category, tags in processor.preset_tags.items() if tags],
                    label="✅ 选择预设删除标签"
                )
                
                with gr.Row():
                    preset_preview_button = gr.Button("👁️ 预览删除", variant="secondary")
                    preset_confirm_button = gr.Button("🗑️ 确认删除", variant="stop")
                
                preset_preview_output = gr.Textbox(label="👁️ 删除预览", interactive=False, lines=8)
                preset_delete_output = gr.Textbox(label="✅ 删除结果", interactive=False)
                
                gr.Markdown("### 🔧 其他功能")
                gr.Markdown("**文本前后缀**：在整个文本内容前后添加")
                with gr.Row():
                    prefix_input = gr.Textbox(label="📝 前缀", placeholder="输入要添加的前缀")
                    suffix_input = gr.Textbox(label="📝 后缀", placeholder="输入要添加的后缀")
                
                prefix_suffix_button = gr.Button("➕ 添加前缀/后缀", variant="primary")
                prefix_suffix_output = gr.Textbox(label="✅ 处理结果", interactive=False)
                
                gr.Markdown("**标签替换**：精确替换单个标签")
                with gr.Row():
                    old_tag_input = gr.Textbox(label="🗑️ 要替换的标签", placeholder="输入要替换的标签")
                    new_tag_input = gr.Textbox(label="✨ 新标签", placeholder="输入新的标签")
                
                replace_button = gr.Button("🔄 替换标签", variant="primary")
                replace_output = gr.Textbox(label="✅ 替换结果", interactive=False)
                
                gr.Markdown("**文本替换**：整体搜索替换文本内容")
                with gr.Row():
                    old_text_input = gr.Textbox(label="🔍 要替换的文本", placeholder="输入要替换的文本内容")
                    new_text_input = gr.Textbox(label="✨ 新文本", placeholder="输入新的文本内容")
                
                text_replace_button = gr.Button("🔄 文本替换", variant="primary")
                text_replace_output = gr.Textbox(label="✅ 替换结果", interactive=False)
        
        # 事件绑定
        stats_button.click(
            fn=update_tag_statistics,
            inputs=[directory_input, include_subfolders_checkbox],
            outputs=[tag_checkboxes, stats_output]
        )
        
        preview_button.click(
            fn=preview_delete_operation,
            inputs=[directory_input, tag_checkboxes, include_subfolders_checkbox],
            outputs=[preview_output]
        )
        
        confirm_delete_button.click(
            fn=execute_delete_operation,
            inputs=[directory_input, tag_checkboxes, include_subfolders_checkbox],
            outputs=[delete_output]
        )
        
        # 预设删除事件绑定
        preset_preview_button.click(
            fn=preview_preset_delete,
            inputs=[directory_input, preset_checkboxes, include_subfolders_checkbox],
            outputs=[preset_preview_output]
        )
        
        preset_confirm_button.click(
            fn=execute_preset_delete,
            inputs=[directory_input, preset_checkboxes, include_subfolders_checkbox],
            outputs=[preset_delete_output]
        )
        
        # 其他功能事件绑定
        prefix_suffix_button.click(
            fn=add_prefix_suffix_to_tags,
            inputs=[directory_input, prefix_input, suffix_input, include_subfolders_checkbox],
            outputs=[prefix_suffix_output]
        )
        
        replace_button.click(
            fn=replace_tag_in_files,
            inputs=[directory_input, old_tag_input, new_tag_input, include_subfolders_checkbox],
            outputs=[replace_output]
        )
        
        text_replace_button.click(
            fn=replace_text_in_files,
            inputs=[directory_input, old_text_input, new_text_input, include_subfolders_checkbox],
            outputs=[text_replace_output]
        )
    

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
