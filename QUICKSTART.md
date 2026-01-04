# 快速开始指南 / Quick Start Guide

## 中文说明

### 1. 环境准备

#### 安装 Anaconda
1. 下载 Anaconda: https://www.anaconda.com/download
2. 安装 Anaconda（选择 "Add Anaconda to PATH" 选项）
3. 重启终端/命令提示符

### 2. 安装项目

```bash
# 克隆仓库
git clone https://github.com/among-the-mountain/music-analysis.git
cd music-analysis

# 创建 conda 环境
conda env create -f environment.yml

# 激活环境
conda activate music-analysis
```

### 3. 运行应用

#### Windows 用户:
双击运行 `start.bat` 文件

或在命令提示符中运行:
```cmd
start.bat
```

#### Linux/macOS 用户:
```bash
./start.sh
```

或者直接运行:
```bash
conda activate music-analysis
python app.py
```

### 4. 访问应用

打开浏览器访问: http://localhost:5000

### 5. 使用自己的数据集

1. 下载 Spotify 数据集 (Kaggle: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
2. 将 CSV 文件放入 `data/` 目录
3. 在 `app.py` 中修改数据路径:
```python
analyzer = MusicAnalyzer(data_path='data/your_dataset.csv')
```

### 常见问题

**Q: 如何停止服务器？**  
A: 在终端中按 `Ctrl+C`

**Q: 如何更改聚类数量？**  
A: 在 `app.py` 中修改:
```python
analyzer.perform_clustering(n_clusters=5)  # 改为你想要的数量
```

**Q: 端口 5000 被占用怎么办？**  
A: 在 `app.py` 的最后一行修改端口:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # 改为 8080 或其他端口
```

---

## English Instructions

### 1. Environment Setup

#### Install Anaconda
1. Download Anaconda: https://www.anaconda.com/download
2. Install Anaconda (check "Add Anaconda to PATH" option)
3. Restart your terminal/command prompt

### 2. Install Project

```bash
# Clone repository
git clone https://github.com/among-the-mountain/music-analysis.git
cd music-analysis

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate music-analysis
```

### 3. Run Application

#### Windows Users:
Double-click `start.bat` file

Or run in Command Prompt:
```cmd
start.bat
```

#### Linux/macOS Users:
```bash
./start.sh
```

Or run directly:
```bash
conda activate music-analysis
python app.py
```

### 4. Access Application

Open browser and visit: http://localhost:5000

### 5. Use Your Own Dataset

1. Download Spotify dataset (Kaggle: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
2. Place CSV file in `data/` directory
3. Modify data path in `app.py`:
```python
analyzer = MusicAnalyzer(data_path='data/your_dataset.csv')
```

### Troubleshooting

**Q: How to stop the server?**  
A: Press `Ctrl+C` in the terminal

**Q: How to change number of clusters?**  
A: Modify in `app.py`:
```python
analyzer.perform_clustering(n_clusters=5)  # Change to desired number
```

**Q: Port 5000 is already in use?**  
A: Modify port in the last line of `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change to 8080 or other port
```

---

## 功能特点 / Features

### 数据分析 / Data Analysis
- ✅ 7维特征提取 (7-dimensional feature extraction)
- ✅ StandardScaler 标准化 (StandardScaler normalization)
- ✅ K-Means 聚类 (K-Means clustering)

### 可视化 / Visualization
- 📊 雷达图 (Radar charts)
- 📍 2D/3D 散点图 (2D/3D scatter plots)
- 🔥 热力图 (Heatmaps)
- 📈 分布图 (Distribution charts)

### 交互功能 / Interactive Features
- 🎯 动态图表 (Dynamic charts)
- 📱 响应式设计 (Responsive design)
- 🎨 现代化界面 (Modern UI)

---

## 技术栈 / Tech Stack

- **Backend**: Flask 3.0.0
- **ML**: Scikit-learn 1.3.2
- **Data**: Pandas 2.1.4, NumPy 1.26.2
- **Visualization**: Plotly 5.18.0
- **Frontend**: HTML5, CSS3

---

## 支持 / Support

如遇问题，请在 GitHub 提交 Issue:
https://github.com/among-the-mountain/music-analysis/issues

For issues, please submit on GitHub:
https://github.com/among-the-mountain/music-analysis/issues
