# 🎵 音乐数据分析与可视化系统

基于 Flask + K-Means 聚类算法的 Spotify 音乐情绪分析与可视化项目。

**🆕 新功能**: 现在支持网易云音乐数据分析！[查看中文文档](README_CN.md)

![Music Analysis Dashboard](https://github.com/user-attachments/assets/fc32deb2-4b0b-409d-8a9a-334201ccfc01)

> 现代化的音乐数据分析与可视化系统，展示多维度特征雷达图、散点分布图和详细统计信息。

## ✨ Features

### Original Spotify Analysis
- K-Means clustering of music tracks based on audio features
- Interactive radar charts showing cluster characteristics
- Scatter plots visualizing energy vs valence distribution
- Detailed statistics for each music cluster

### 🆕 NetEase Cloud Music Analysis (New!)
- 🎵 Web scraping of NetEase Cloud Music data
- 📊 Music genre distribution analysis
- 💿 Album type analysis with TOP10 rankings
- 📈 Music release trend over time
- 👨‍🎤 Top artists by number of works
- 📝 Word cloud visualization of song titles
- 💭 Sentiment analysis of user comments

[📖 完整中文文档 / Full Chinese Documentation](README_CN.md)

## 🚀 Quick Start

### For NetEase Cloud Music Analysis (网易云音乐分析)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data
python netease_scraper.py

# 3. Run the application
python app.py

# 4. Open browser
# Visit: http://localhost:5000
```

### For Spotify Analysis (Original)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data
python generate_sample_data.py

# 3. Run the application
python app.py
```

## 📊 Screenshots

### NetEase Cloud Music Dashboard
![Dashboard Overview](https://github.com/user-attachments/assets/5dc117e6-5cda-4929-91c2-f50a5e02a1e8)
![Album Analysis](https://github.com/user-attachments/assets/f0607b47-bc9d-4a2e-b9bd-8f6260fa4d2a)
![Trend Analysis](https://github.com/user-attachments/assets/97bb95b8-44c9-4318-9f3e-c0c409113d01)

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly 5.18.0
- **Chinese NLP**: jieba (for word segmentation)
- **Word Cloud**: WordCloud
- **Web Scraping**: Requests

## 📁 Project Structure

```
music-analysis/
├── app.py                  # Flask application
├── data_processor.py       # Data processing and analysis
├── netease_scraper.py     # NetEase Cloud Music scraper (New!)
├── generate_sample_data.py # Spotify sample data generator
├── templates/
│   ├── dashboard.html     # NetEase dashboard (New!)
│   └── index.html         # Spotify dashboard
├── static/
│   ├── css/
│   │   ├── dashboard.css  # NetEase styles (New!)
│   │   └── style.css      # Spotify styles
│   └── js/
│       ├── dashboard.js   # NetEase scripts (New!)
│       └── main.js        # Spotify scripts
└── requirements.txt
```

## 🌏 Language Support

- 🇨🇳 **Chinese (中文)**: Full support for NetEase Cloud Music analysis
- 🇬🇧 **English**: Original Spotify analysis

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

⭐ If you find this project helpful, please give it a star! 