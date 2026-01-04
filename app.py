from flask import Flask, render_template, jsonify, request
import os
import json
from data_processor import MusicDataProcessor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 全局变量存储数据处理器
processor = None
data_loaded = False

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), 'spotify_tracks.csv')


def initialize_processor():
    """初始化数据处理器并加载数据"""
    global processor, data_loaded
    
    if not os.path.exists(DATA_FILE):
        print(f"警告: 数据文件不存在 {DATA_FILE}")
        print("请下载Spotify Tracks Dataset并重命名为 spotify_tracks.csv")
        return False
    
    try:
        processor = MusicDataProcessor(n_clusters=5)
        success = processor.process_pipeline(DATA_FILE)
        data_loaded = success
        return success
    except Exception as e:
        print(f"初始化失败: {e}")
        return False


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """获取数据加载状态"""
    return jsonify({
        'loaded': data_loaded,
        'file_exists': os.path.exists(DATA_FILE)
    })


@app.route('/api/cluster-stats')
def get_cluster_stats():
    """获取聚类统计信息"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    stats = processor.get_cluster_stats()
    return jsonify(stats)


@app.route('/api/cluster-samples')
def get_cluster_samples():
    """获取聚类样本"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    n_samples = request.args.get('n', default=10, type=int)
    samples = processor.get_sample_tracks(n_samples=n_samples)
    return jsonify(samples)


@app.route('/api/reload')
def reload_data():
    """重新加载数据"""
    success = initialize_processor()
    return jsonify({'success': success})


if __name__ == '__main__':
    print("=" * 50)
    print("音乐数据分析与可视化系统")
    print("=" * 50)
    
    # 尝试初始化数据
    initialize_processor()
    
    # 启动Flask应用
    print("\n启动服务器...")
    print("访问 http://localhost:5000 查看应用")
    
    # 从环境变量读取调试模式设置，生产环境应设为False
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
