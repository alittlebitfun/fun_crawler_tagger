# 爬虫模块 (Crawler)

专门用于从各种图片网站爬取角色图片的Python工具集。

## 📁 文件说明

- `batch_crawl.py` - **主要爬虫脚本**，支持批量爬取多个角色
- `alternative_scraper.py` - 替代爬虫方案，使用Safebooru作为备用源
- `crawl.py` - 基础爬虫脚本，支持phainon和mydei角色
- `danbooru_scraper.py` - Danbooru专用爬虫
- `character_list.py` - 基础角色列表（10个角色）
- `complete_character_list.py` - 完整角色列表（30+个角色）
- `test_connection.py` - 网络连接测试工具

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install waifuc requests pandas
```

### 2. 批量爬取（推荐）

```bash
python batch_crawl.py
```

### 3. 替代爬虫方案

```bash
python alternative_scraper.py
```

## ⚙️ 配置选项

### 代理设置
在脚本开头修改代理配置：
```python
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
```

### 输出目录
修改 `batch_crawl.py` 中的输出路径：
```python
base_dir = "F:/honkai_star_rail_characters"  # 修改为你的路径
```

### 爬取数量
设置每个角色的图片数量：
```python
max_images = 100  # 每个角色爬取100张图片
```

## 🔧 高级功能

### AI处理选项
- **CCIP处理**：内容一致性检查
- **WD14标签**：自动生成标签
- **人脸检测**：确保单个人脸
- **相似度过滤**：去除重复图片

### 图片处理
- **格式转换**：RGB模式转换
- **尺寸调整**：自动调整到1024px
- **背景处理**：透明背景转白色
- **随机命名**：避免文件名冲突

## 📊 使用示例

### 爬取单个角色
```python
from complete_character_list import all_characters, character_names

# 爬取丹恒的图片
character_tag = "dan_heng_(honkai:_star_rail)"
character_name = "丹恒"
```

### 批量爬取所有角色
```python
# 在batch_crawl.py中选择"爬取所有角色"
crawl_all = "y"  # 或 "yes"
```

### 自定义角色选择
```python
# 选择特定角色编号
selected_indices = "1,3,5"  # 爬取第1、3、5个角色
```

## ⚠️ 注意事项

1. **网络连接**：确保网络稳定，可能需要代理
2. **存储空间**：每个角色约100张图片，需要足够空间
3. **爬取速度**：AI处理模式较慢，但质量更高
4. **网站限制**：遵守各网站的爬虫协议
5. **版权声明**：仅用于学习研究，请勿商用

## 🛠️ 故障排除

### 连接问题
```bash
python test_connection.py
```

### 代理问题
检查代理设置是否正确：
```python
# 确保代理地址正确
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
```

### 依赖问题
```bash
pip install --upgrade waifuc requests pandas
```

## 📈 性能优化

- 使用非AI模式可显著提升速度
- 调整图片数量以平衡质量和速度
- 使用SSD存储提升I/O性能
- 确保网络带宽充足

## 🔗 相关资源

- [Waifuc文档](https://github.com/deepghs/waifuc)
- [Danbooru API](https://danbooru.donmai.us/wiki_pages/help:api)
- [Safebooru API](https://safebooru.org/index.php?page=help&topic=cheatsheet)
