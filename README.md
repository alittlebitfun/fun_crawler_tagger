# 星穹铁道角色数据集处理工具

一个专门用于处理《崩坏：星穹铁道》角色图片数据集的Python工具集，包含图片爬取和标签管理两大核心功能。

## 📁 项目结构

```
├── crawler/              # 图片爬虫模块
│   ├── alternative_scraper.py      # 替代爬虫方案（Safebooru）
│   ├── batch_crawl.py              # 批量角色爬取
│   ├── crawl.py                    # 基础爬虫脚本
│   ├── danbooru_scraper.py        # Danbooru爬虫
│   ├── character_list.py          # 角色列表（基础版）
│   ├── complete_character_list.py  # 完整角色列表
│   ├── test_connection.py         # 连接测试
│   ├── 完整角色清单.txt            # 角色清单文档
│   └── 角色清单.txt               # 基础角色清单
├── tagging/              # 标签管理模块
│   ├── tag_processor_gradio.py    # Gradio标签处理界面
│   ├── excel_to_txt.py           # Excel转TXT工具
│   ├── 预设/                      # 预设标签文件
│   │   ├── 人物特征.txt
│   │   ├── 服装.txt
│   │   └── 饰品.txt
│   ├── tag_backup/               # 标签备份目录
│   ├── 数据集.txt                 # 数据集说明
│   └── 数据集.xlsx               # 数据集Excel文件
├── datasets/             # 数据集存储
│   ├── data/                     # 原始数据
│   ├── downloads/                # 下载文件
│   └── txt_files/                # 文本文件
├── requirements.txt       # 依赖包列表
└── README.md             # 项目说明文档
```

## 🚀 功能特性

### 🕷️ 爬虫功能 (crawler/)

- **多源支持**：支持Danbooru、Safebooru等多个图片源
- **批量爬取**：支持批量爬取多个角色图片
- **智能过滤**：自动过滤相似图片、单色图片等
- **AI处理**：可选的CCIP和WD14标签处理
- **角色管理**：包含完整的星穹铁道角色列表

#### 主要脚本：

- `batch_crawl.py` - 批量爬取角色图片（推荐使用）
- `alternative_scraper.py` - 替代爬虫方案
- `danbooru_scraper.py` - Danbooru专用爬虫
- `complete_character_list.py` - 完整角色列表定义

### 🏷️ 标签管理 (tagging/)

- **可视化界面**：基于Gradio的友好Web界面
- **批量处理**：支持批量删除、替换标签
- **预设管理**：预设标签分类管理
- **安全备份**：操作前自动备份
- **文本处理**：支持Excel转TXT等格式转换

#### 主要功能：

- 标签统计与分析
- 批量删除指定标签
- 预设标签批量删除
- 添加前缀/后缀
- 标签替换
- 文本内容替换

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

### 额外依赖（爬虫功能）

```bash
pip install waifuc pandas openpyxl
```

## 🎯 使用方法

### 1. 图片爬取

#### 批量爬取角色图片：
```bash
cd crawler
python batch_crawl.py
```

#### 使用替代爬虫：
```bash
cd crawler
python alternative_scraper.py
```

### 2. 标签管理

#### 启动标签处理界面：
```bash
cd tagging
python tag_processor_gradio.py
```

访问 `http://localhost:7860` 使用Web界面

#### Excel转TXT：
```bash
cd tagging
python excel_to_txt.py
```

## 📊 支持的角色

项目支持《崩坏：星穹铁道》中的所有主要角色，包括：

- **主角团**：开拓者、三月七、丹恒、姬子、瓦尔特
- **贝洛伯格**：布洛妮娅、希儿、克拉拉、希露瓦等
- **仙舟罗浮**：景元、罗刹、刃、素裳、停云等
- **星核猎手**：卡芙卡、银狼
- **其他角色**：托帕、桂乃芬、花火等

完整角色列表请查看 `crawler/complete_character_list.py`

## ⚙️ 配置说明

### 爬虫配置

- **代理设置**：在脚本中修改代理配置
- **输出目录**：可自定义图片保存路径
- **图片数量**：可设置每个角色的爬取数量
- **AI处理**：可选择是否启用CCIP和标签处理

### 标签管理配置

- **默认路径**：在 `tag_processor_gradio.py` 中修改默认数据集路径
- **预设标签**：在 `tagging/预设/` 目录中添加自定义预设
- **备份设置**：自动备份到 `tagging/tag_backup/` 目录

## 🔧 高级功能

### 爬虫高级选项

- **相似度过滤**：自动去除重复图片
- **人脸检测**：确保图片包含单个人脸
- **尺寸调整**：自动调整图片尺寸
- **格式转换**：支持多种图片格式

### 标签管理高级功能

- **递归处理**：支持子文件夹递归处理
- **预览功能**：操作前预览影响范围
- **批量操作**：支持大量文件批量处理
- **版本控制**：自动备份和版本管理

## 📝 注意事项

1. **网络要求**：爬虫功能需要稳定的网络连接
2. **存储空间**：确保有足够的存储空间保存图片和备份
3. **版权声明**：请遵守相关网站的爬虫协议和版权规定
4. **数据备份**：重要操作前建议手动备份数据

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

## 🔗 相关链接

- [Danbooru](https://danbooru.donmai.us/)
- [Safebooru](https://safebooru.org/)
- [Gradio](https://gradio.app/)
- [Waifuc](https://github.com/deepghs/waifuc)

---

**免责声明**：本项目仅用于学习和研究目的，使用者需自行承担使用风险并遵守相关法律法规。
