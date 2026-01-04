# 🎵 网易云音乐大数据分析可视化系统

基于 Flask 的音乐数据爬取、分析与可视化平台，实现网易云音乐数据的多维度分析展示。

![Dashboard Overview](https://github.com/user-attachments/assets/5dc117e6-5cda-4929-91c2-f50a5e02a1e8)

## ✨ 功能特性

### 1. 数据爬取
- ✅ 爬取网易云音乐热门歌单数据
- ✅ 支持生成示例数据用于测试
- ✅ 自动去重和数据清洗

### 2. 数据分析功能

#### 📊 音乐类型占比分析
分析并展示不同音乐类型（流行、摇滚、民谣、电子、说唱等）的市场占比情况。

#### 💿 专辑类型分析
- 分析不同专辑类型（录音室专辑、现场专辑、EP/单曲、精选集、合辑）的数据分布
- 展示各类型专辑的受欢迎程度和用户评价
- TOP10专辑类型排行榜

![Album Analysis](https://github.com/user-attachments/assets/f0607b47-bc9d-4a2e-b9bd-8f6260fa4d2a)

#### 📈 音乐发布趋势分析
统计并展示音乐作品的发布时间趋势，通过折线图呈现市场的季节性变化。

![Publish Trend](https://github.com/user-attachments/assets/97bb95b8-44c9-4318-9f3e-c0c409113d01)

#### 👨‍🎤 音乐作者分析
列出发布作品数量最多的TOP5音乐作者，展示活跃创作者及其作品影响力。

![Artists Analysis](https://github.com/user-attachments/assets/a07c5062-51ba-4324-82fc-ad3364411b6b)

#### 📝 音乐名称词云图
使用词云图展示热门音乐名称和关键词，基于jieba分词技术分析音乐热点。

#### 💭 评论情感分析
分析歌曲评论区的用户情感趋势，展示积极、中性、消极情感的分布和变化。

![Sentiment Analysis](https://github.com/user-attachments/assets/b5ee9ddb-bf01-4d7e-b021-038b1cde1024)

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/among-the-mountain/music-analysis.git
cd music-analysis
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **生成数据**
```bash
python netease_scraper.py
```
选择选项1生成示例数据（推荐用于测试），或选择选项2爬取真实数据。

4. **启动应用**
```bash
python app.py
```

5. **访问应用**
打开浏览器访问: http://localhost:5000

## 📁 项目结构

```
music-analysis/
├── app.py                      # Flask应用主文件
├── data_processor.py           # 数据处理模块
├── netease_scraper.py         # 网易云音乐爬虫
├── requirements.txt            # Python依赖
├── templates/
│   ├── dashboard.html         # 主仪表板页面
│   └── index.html             # 原Spotify分析页面（保留）
├── static/
│   ├── css/
│   │   ├── dashboard.css      # 仪表板样式
│   │   └── style.css          # 原样式（保留）
│   └── js/
│       ├── dashboard.js       # 仪表板交互脚本
│       └── main.js            # 原脚本（保留）
└── README.md
```

## 🔧 技术栈

- **后端**: Flask 3.0.0
- **数据处理**: Pandas, NumPy, Scikit-learn
- **可视化**: Plotly 5.18.0
- **中文分词**: jieba
- **词云生成**: WordCloud
- **HTTP请求**: Requests

## 📊 API端点

### 数据状态
- `GET /api/status` - 获取数据加载状态

### 分析数据
- `GET /api/music-type-distribution` - 音乐类型分布
- `GET /api/album-type-analysis` - 专辑类型分析
- `GET /api/album-type-top10` - 专辑类型TOP10
- `GET /api/publish-trend` - 发布趋势数据
- `GET /api/top-artists?top=5` - TOP作者数据
- `GET /api/wordcloud` - 词云图数据
- `GET /api/sentiment-trend` - 情感分析数据

### 操作
- `GET /api/reload` - 重新加载数据

## 📝 使用说明

### 数据生成

**选项1: 生成示例数据（推荐）**
```bash
python netease_scraper.py
# 选择 1
```
快速生成500条测试数据，包含所有必要字段。

**选项2: 爬取真实数据**
```bash
python netease_scraper.py
# 选择 2
```
从网易云音乐API爬取真实数据（可能受网络限制）。

### 自定义配置

修改 `netease_scraper.py` 中的参数：
```python
# 生成更多数据
generate_sample_netease_data(n_samples=1000)

# 爬取更多歌单
scraper.scrape_music_data(num_playlists=10, include_comments=True)
```

## 🎨 界面特点

- **响应式设计**: 支持桌面和移动设备
- **标签页导航**: 5个分析模块，清晰分类
- **交互式图表**: 基于Plotly的动态可视化
- **现代化UI**: 渐变色设计，视觉效果出色
- **中文支持**: 完整的中文界面和数据展示

## 🔍 数据分析示例

生成的示例数据包含：
- **500首歌曲**: 来自20位热门中文歌手
- **5种专辑类型**: 录音室专辑、现场专辑、EP/单曲、精选集、合辑
- **9种音乐类型**: 流行、摇滚、民谣、电子、说唱、古风、轻音乐、爵士、R&B
- **时间跨度**: 2000-2024年，25年音乐发展历程

## 🐛 故障排除

### 问题1: 数据未加载
**解决方案**: 确保运行了 `python netease_scraper.py` 生成数据文件

### 问题2: 词云图不显示
**解决方案**: 安装中文字体
```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei

# macOS 自带中文字体
```

### 问题3: Plotly图表不显示
**解决方案**: 检查网络连接，确保可以访问CDN
```html
<!-- 或使用本地Plotly库 -->
<script src="/static/js/plotly-latest.min.js"></script>
```

## 📈 未来规划

- [ ] 实时数据更新
- [ ] 更多数据源集成
- [ ] 高级情感分析（使用深度学习）
- [ ] 用户登录和个性化推荐
- [ ] 数据导出功能（Excel/PDF）
- [ ] 更多图表类型（桑基图、热力图等）

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

among-the-mountain

---

⭐ 如果这个项目对你有帮助，欢迎给个Star！
