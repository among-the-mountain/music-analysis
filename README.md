# 🎵 音乐数据分析与可视化系统

基于 Flask + K-Means 聚类算法的 Spotify 音乐情绪分析与可视化项目。

![Music Analysis Dashboard](https://github.com/user-attachments/assets/fc32deb2-4b0b-409d-8a9a-334201ccfc01)

> 现代化的音乐数据分析与可视化系统，展示多维度特征雷达图、散点分布图和详细统计信息。

## 功能特性

- ✨ **多维特征提取**: 提取舞曲性（Danceability）、能量值（Energy）、效价（Valence）等7个维度的音乐特征
- 📊 **数据标准化**: 使用 StandardScaler 对不同维度进行标准化处理
- 🎯 **K-Means 聚类**: 将音乐自动分类为5个不同的"情绪簇"
- 📈 **可视化展示**: 
  - 雷达图展示各簇的多维特征分布
  - 散点图展示能量值与快乐度的二维分布
- 🎨 **现代化UI**: 简洁美观的界面设计，符合比例美学
- 🔄 **动态加载**: 支持数据重新加载和实时更新

## 技术栈

- **后端**: Flask 3.0.0
- **数据处理**: pandas, numpy, scikit-learn
- **可视化**: Plotly.js
- **前端**: HTML5, CSS3, JavaScript (原生)

## 环境要求

- Python 3.10+
- Conda (推荐用于 Windows 环境)
- 现代浏览器 (Chrome, Firefox, Edge)

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/among-the-mountain/music-analysis.git
cd music-analysis
```

### 2. 创建 Conda 虚拟环境

```bash
conda env create -f environment.yml
conda activate music-analysis
```

或者使用 pip 安装依赖：

```bash
conda create -n music-analysis python=3.10
conda activate music-analysis
pip install -r requirements.txt
```

### 3. 获取数据集

从 Kaggle 下载 Spotify Tracks Dataset：

1. 访问 [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
2. 下载 CSV 文件
3. 将文件重命名为 `spotify_tracks.csv`
4. 将文件放置在项目根目录

**注意**: 数据集应包含以下列：
- `name` 或 `track_name`: 音乐名称
- `artists` 或 `artist_name`: 艺术家
- `danceability`: 舞曲性
- `energy`: 能量值
- `valence`: 快乐度/效价
- `acousticness`: 原声度
- `instrumentalness`: 器乐度
- `liveness`: 现场感
- `speechiness`: 语音度

### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

**安全提示**: 在生产环境中，请设置环境变量 `SECRET_KEY`：
```bash
# Windows PowerShell
$env:SECRET_KEY="your-secure-random-secret-key"
python app.py

# Windows CMD
set SECRET_KEY=your-secure-random-secret-key
python app.py

# Linux/Mac
export SECRET_KEY="your-secure-random-secret-key"
python app.py
```

## 使用说明

1. 启动应用后，在浏览器中访问 `http://localhost:5000`
2. 如果数据文件已正确放置，系统会自动加载并进行聚类分析
3. 查看以下可视化内容：
   - **雷达图**: 展示5个情绪簇的多维特征对比
   - **散点图**: 展示音乐在能量值-快乐度空间的分布
   - **统计信息**: 每个簇的详细特征数据
   - **样本音乐**: 每个簇的代表性音乐列表

## 项目结构

```
music-analysis/
├── app.py                  # Flask 应用主文件
├── data_processor.py       # 数据处理模块（特征提取、标准化、聚类）
├── requirements.txt        # Python 依赖
├── environment.yml         # Conda 环境配置
├── templates/
│   └── index.html         # 主页面模板
├── static/
│   ├── css/
│   │   └── style.css      # 样式文件
│   └── js/
│       └── main.js        # 前端 JavaScript
└── README.md              # 项目说明文档
```

## API 接口

- `GET /` - 主页面
- `GET /api/status` - 获取数据加载状态
- `GET /api/cluster-stats` - 获取聚类统计信息
- `GET /api/cluster-samples?n=10` - 获取样本音乐（可指定数量）
- `GET /api/reload` - 重新加载数据

## 情绪簇说明

系统将音乐分为5个情绪簇：

1. **高能激情簇**: 高能量、高快乐度的音乐
2. **轻松愉悦簇**: 中等能量、高快乐度的音乐
3. **平静内敛簇**: 低能量、低快乐度的音乐
4. **活力舞曲簇**: 高舞曲性的音乐
5. **深沉情感簇**: 高情感表达的音乐

## 常见问题

### Q: 数据文件应该是什么格式？
A: CSV 格式，包含必要的音乐特征列（详见"获取数据集"部分）。

### Q: 可以更改聚类数量吗？
A: 可以，在 `app.py` 中修改 `MusicDataProcessor(n_clusters=5)` 参数。

### Q: 为什么图表不显示？
A: 请确保：
1. 数据文件已正确加载
2. 浏览器控制台没有错误
3. 网络连接正常（Plotly.js 需要从CDN加载）

### Q: 如何在其他端口运行？
A: 修改 `app.py` 中的 `app.run(port=5000)` 参数。

## 性能说明

- 首次加载数据时可能需要几秒钟，取决于数据集大小
- 聚类过程使用 K-Means 算法，数据量大时会占用一定内存
- 建议数据集不超过 100,000 条记录以保证流畅运行

## 开发者

本项目为大数据音乐分析课程项目。

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-01-04)
- 初始版本发布
- 实现基本的聚类分析功能
- 实现雷达图和散点图可视化
- 添加样本音乐展示功能