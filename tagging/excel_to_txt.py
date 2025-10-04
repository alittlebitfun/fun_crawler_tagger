import pandas as pd
import os

def excel_to_txt(excel_file, output_dir):
    """
    将Excel文件导出为多个txt文件
    第一列是文本内容，第二列是文件名
    每一行生成一个单独的txt文件
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        
        # 检查是否有至少两列
        if len(df.columns) < 2:
            print(f"错误：Excel文件至少需要2列，当前只有{len(df.columns)}列")
            return False
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 获取前两列
        text_column = df.iloc[:, 0]  # 第一列（文本）
        filename_column = df.iloc[:, 1]  # 第二列（文件名）
        
        success_count = 0
        
        # 为每一行创建单独的txt文件
        for i in range(len(df)):
            text = str(text_column.iloc[i]) if pd.notna(text_column.iloc[i]) else ""
            filename = str(filename_column.iloc[i]) if pd.notna(filename_column.iloc[i]) else ""
            
            # 清理文件名，移除不合法字符
            safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
            if not safe_filename:
                safe_filename = f"file_{i+1}"
            
            # 确保文件名以.txt结尾
            if not safe_filename.endswith('.txt'):
                safe_filename += '.txt'
            
            # 创建文件路径
            file_path = os.path.join(output_dir, safe_filename)
            
            # 写入文本内容到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            success_count += 1
            print(f"已创建文件: {safe_filename}")
        
        print(f"成功创建 {success_count} 个txt文件到 {output_dir} 目录")
        return True
        
    except Exception as e:
        print(f"处理文件时出错：{e}")
        return False

if __name__ == "__main__":
    excel_file = "数据集.xlsx"
    output_dir = "txt_files"  # 输出目录
    
    if os.path.exists(excel_file):
        excel_to_txt(excel_file, output_dir)
    else:
        print(f"文件 {excel_file} 不存在")
