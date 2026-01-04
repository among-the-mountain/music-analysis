# 快速开始指南

## Windows 系统快速启动

### 方法一：使用示例数据（推荐用于快速测试）

1. **打开命令提示符或 PowerShell**

2. **创建 Conda 环境**
   ```bash
   conda env create -f environment.yml
   conda activate music-analysis
   ```

3. **生成示例数据**
   ```bash
   python generate_sample_data.py
   ```

4. **启动应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   
   在浏览器中打开：`http://localhost:5000`

### 方法二：使用真实 Kaggle 数据集

1. **下载数据集**
   - 访问 [Kaggle Spotify Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
   - 登录 Kaggle 账户
   - 点击 "Download" 下载数据

2. **准备数据文件**
   - 解压下载的文件
   - 将 CSV 文件重命名为 `spotify_tracks.csv`
   - 放置在项目根目录

3. **创建环境并启动**
   ```bash
   conda env create -f environment.yml
   conda activate music-analysis
   python app.py
   ```

## 仅使用 pip 安装（不使用 Conda）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 生成示例数据
python generate_sample_data.py

# 启动应用
python app.py
```

## 验证安装

成功启动后，你应该看到：

```
==================================================
音乐数据分析与可视化系统
==================================================
成功加载数据: 1000 条记录
特征标准化完成
聚类完成，共5个簇

启动服务器...
访问 http://localhost:5000 查看应用
 * Running on http://0.0.0.0:5000
```

## 故障排除

### 问题：模块未找到

**解决方案**：
```bash
pip install -r requirements.txt
```

### 问题：端口被占用

**解决方案**：修改 `app.py` 中的端口号
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为 5001
```

### 问题：数据文件未找到

**解决方案**：
1. 运行 `python generate_sample_data.py` 生成示例数据
2. 或确保 `spotify_tracks.csv` 在项目根目录

### 问题：Plotly 图表不显示

**解决方案**：
1. 检查网络连接（需要加载 Plotly CDN）
2. 清除浏览器缓存
3. 使用 Chrome 或 Firefox 浏览器

## 下一步

- 探索不同的可视化图表
- 查看各个情绪簇的特征
- 浏览样本音乐列表
- 尝试调整聚类参数（修改 `app.py` 中的 `n_clusters`）

## 获取帮助

如遇问题，请检查：
1. Python 版本是否为 3.10+
2. 所有依赖是否正确安装
3. 浏览器控制台是否有错误信息
