# 🎵 Music Analysis & Visualization System

一个基于Flask的大数据音乐分析可视化项目，使用机器学习算法对Spotify音乐数据集进行多维特征提取和情感聚类分析。

A big data music analysis and visualization project built with Flask, using machine learning algorithms for multi-dimensional feature extraction and emotion clustering on Spotify music datasets.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.2-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features / 功能特点

### 多维特征提取 (Multi-Dimensional Feature Extraction)
- **Danceability (舞曲性)**: 音乐适合跳舞的程度
- **Energy (能量值)**: 音乐的强度和活跃度
- **Valence (效价/快乐度)**: 音乐的积极情绪程度
- **Acousticness (声学性)**: 音乐的原声程度
- **Instrumentalness (器乐性)**: 音乐中器乐的占比
- **Speechiness (语音性)**: 音乐中语音的存在程度
- **Liveness (现场性)**: 录音中观众存在的可能性

### 数据处理 (Data Processing)
- ✅ 使用 **StandardScaler** 进行数据标准化处理
- ✅ 确保所有特征具有相同的权重
- ✅ 消除不同数值范围带来的偏差
- ✅ 为机器学习算法提供统一的特征空间

### K-Means 聚类 (K-Means Clustering)
- 🤖 非监督学习算法
- 🎯 自动将音乐分为5个情感簇
- 📊 基于多维特征的相似性分组
- 🎭 发现音乐中的隐藏模式

### 可视化功能 (Visualization Features)
- 📊 **雷达图 (Radar Charts)**: 展示每个聚类的特征画像
- 📍 **散点图 (Scatter Plots)**: 2D音乐分布可视化
- 🌐 **3D散点图 (3D Scatter Plots)**: 三维特征空间探索
- 🔥 **热力图 (Heatmaps)**: 特征相关性分析
- 📈 **柱状图 (Bar Charts)**: 聚类分布统计

## 📋 System Requirements / 系统要求

- **操作系统 (OS)**: Windows 10/11 (推荐), Linux, macOS
- **Python**: 3.10+
- **Conda**: Anaconda or Miniconda
- **内存 (RAM)**: 至少 4GB
- **硬盘空间 (Disk)**: 至少 2GB

## 🚀 Installation / 安装步骤

### 1. Clone the Repository / 克隆仓库

```bash
git clone https://github.com/among-the-mountain/music-analysis.git
cd music-analysis
```

### 2. Create Conda Environment / 创建Conda虚拟环境

**Windows系统:**
```bash
conda env create -f environment.yml
conda activate music-analysis
```

**或者使用 pip (Or use pip):**
```bash
conda create -n music-analysis python=3.10
conda activate music-analysis
pip install -r requirements.txt
```

### 3. Verify Installation / 验证安装

```bash
python -c "import flask, pandas, sklearn, plotly; print('All packages installed successfully!')"
```

## 🎯 Usage / 使用方法

### 启动应用 (Start the Application)

**Windows:**
```bash
conda activate music-analysis
python app.py
```

**Linux/macOS:**
```bash
conda activate music-analysis
python app.py
```

### 访问应用 (Access the Application)

1. 打开浏览器 (Open your browser)
2. 访问: `http://localhost:5000`
3. 开始探索音乐数据！(Start exploring music data!)

### 页面导航 (Page Navigation)

- **Dashboard (仪表盘)**: 
  - 项目概览和统计信息
  - Overview and statistics
  
- **Analysis (分析)**: 
  - 详细的可视化图表
  - Detailed visualizations
  - 2D/3D散点图、雷达图、热力图
  - 2D/3D scatter plots, radar charts, heatmaps
  
- **Clusters (聚类)**: 
  - 各个情感聚类的详细信息
  - Detailed information for each emotion cluster
  - 每个聚类的特征画像和代表性曲目
  - Feature profiles and representative tracks

## 📂 Project Structure / 项目结构

```
music-analysis/
├── app.py                      # Flask应用主文件 (Main Flask application)
├── analyzer.py                 # 数据分析模块 (Data analysis module)
├── visualizer.py              # 可视化模块 (Visualization module)
├── requirements.txt           # Python依赖 (Python dependencies)
├── environment.yml            # Conda环境配置 (Conda environment config)
├── README.md                  # 项目说明 (Project documentation)
├── data/
│   └── sample_spotify_data.csv # 示例数据集 (Sample dataset)
├── static/
│   └── css/
│       └── style.css          # 样式文件 (Stylesheet)
└── templates/
    ├── base.html              # 基础模板 (Base template)
    ├── index.html             # 首页 (Homepage)
    ├── analysis.html          # 分析页面 (Analysis page)
    └── clusters.html          # 聚类页面 (Clusters page)
```

## 🔧 Configuration / 配置

### 更改聚类数量 (Change Number of Clusters)

在 `app.py` 中修改:
```python
analyzer.perform_clustering(n_clusters=5)  # 修改这个数字 (Change this number)
```

### 使用自己的数据集 (Use Your Own Dataset)

1. 将CSV文件放入 `data/` 目录
2. 确保CSV包含以下列:
   - `danceability`, `energy`, `valence`, `acousticness`
   - `instrumentalness`, `speechiness`, `liveness`
   - `track_name`, `artists`
3. 在 `app.py` 中更新路径:
   ```python
   analyzer = MusicAnalyzer(data_path='data/your_dataset.csv')
   ```

## 📊 Data Source / 数据来源

本项目使用Spotify Tracks Dataset，可以从以下来源获取:

- **Kaggle**: [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
- 项目包含40首示例歌曲用于演示

Features included in the dataset:
- Audio features (danceability, energy, valence, etc.)
- Track metadata (name, artist, album, popularity)
- Temporal features (tempo, duration, time signature)

## 🎨 UI Features / 界面特点

- ✨ **现代化设计**: 深色主题，视觉舒适
- 📱 **响应式布局**: 适配各种屏幕尺寸
- 🎯 **直观导航**: 清晰的页面结构
- 📊 **交互式图表**: 使用Plotly实现动态可视化
- 🎨 **美学比例**: 符合黄金比例的设计

## 🛠️ Technology Stack / 技术栈

### Backend (后端)
- **Flask 3.0.0**: Web框架
- **Pandas 2.1.4**: 数据处理
- **NumPy 1.26.2**: 数值计算
- **Scikit-learn 1.3.2**: 机器学习

### Frontend (前端)
- **HTML5**: 页面结构
- **CSS3**: 现代化样式
- **Plotly 5.18.0**: 交互式可视化

## 📈 Algorithm Details / 算法细节

### K-Means Clustering
```python
# 配置参数
n_clusters = 5          # 聚类数量
random_state = 42       # 随机种子，确保可重现性
n_init = 10            # 不同初始化次数
max_iter = 300         # 最大迭代次数
```

### Feature Normalization
```python
# 使用StandardScaler标准化
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
# 结果: mean=0, std=1
```

## 🤝 Contributing / 贡献

欢迎提交Issue和Pull Request!

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 📝 License / 许可证

This project is licensed under the MIT License.

## 👤 Author / 作者

**among-the-mountain**
- GitHub: [@among-the-mountain](https://github.com/among-the-mountain)

## 🙏 Acknowledgments / 致谢

- Spotify for providing the music data
- Kaggle community for the datasets
- Flask and Scikit-learn teams for excellent frameworks

## 📞 Support / 支持

如果你喜欢这个项目，请给它一个 ⭐️!

If you like this project, please give it a ⭐️!

---

**Happy Music Analysis! 🎵**