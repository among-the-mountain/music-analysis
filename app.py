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
DATA_FILE = os.path.join(os.path.dirname(__file__), 'netease_music_data.csv')
# 备用文件路径（兼容旧数据）
SPOTIFY_DATA_FILE = os.path.join(os.path.dirname(__file__), 'spotify_tracks.csv')


def initialize_processor():
    """初始化数据处理器并加载数据"""
    global processor, data_loaded
    
    # 优先使用网易云音乐数据，如果不存在则使用Spotify数据
    data_file = DATA_FILE if os.path.exists(DATA_FILE) else SPOTIFY_DATA_FILE
    
    if not os.path.exists(data_file):
        print(f"警告: 数据文件不存在")
        print("请运行 'python netease_scraper.py' 生成数据")
        return False
    
    try:
        processor = MusicDataProcessor(n_clusters=5)
        success = processor.process_pipeline(data_file)
        data_loaded = success
        return success
    except Exception as e:
        print(f"初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False


@app.route('/')
def index():
    """主页面"""
    return render_template('dashboard.html')


@app.route('/api/status')
def get_status():
    """获取数据加载状态"""
    data_file = DATA_FILE if os.path.exists(DATA_FILE) else SPOTIFY_DATA_FILE
    return jsonify({
        'loaded': data_loaded,
        'file_exists': os.path.exists(data_file),
        'is_netease_data': processor.is_netease_data if processor else False,
        'data_file': os.path.basename(data_file) if os.path.exists(data_file) else None
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


@app.route('/api/album-type-analysis')
def get_album_type_analysis():
    """获取专辑类型分析"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    result = processor.get_album_type_analysis()
    if result is None:
        return jsonify({'error': '不支持此分析（仅网易云音乐数据）'}), 400
    
    return jsonify(result)


@app.route('/api/publish-trend')
def get_publish_trend():
    """获取音乐发布趋势"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    result = processor.get_publish_trend()
    if result is None:
        return jsonify({'error': '不支持此分析（仅网易云音乐数据）'}), 400
    
    return jsonify(result)


@app.route('/api/music-type-distribution')
def get_music_type_distribution():
    """获取音乐类型分布"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    result = processor.get_music_type_distribution()
    if result is None:
        return jsonify({'error': '不支持此分析（仅网易云音乐数据）'}), 400
    
    return jsonify(result)


@app.route('/api/album-type-top10')
def get_album_type_top10():
    """获取专辑类型TOP10"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    result = processor.get_album_type_top10()
    if result is None:
        return jsonify({'error': '不支持此分析（仅网易云音乐数据）'}), 400
    
    return jsonify(result)


@app.route('/api/top-artists')
def get_top_artists():
    """获取发布作品最多的作者TOP5"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    top_n = request.args.get('top', default=5, type=int)
    result = processor.get_top_artists(top_n=top_n)
    if result is None:
        return jsonify({'error': '不支持此分析（仅网易云音乐数据）'}), 400
    
    return jsonify(result)


@app.route('/api/wordcloud')
def get_wordcloud():
    """获取词云图"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    result = processor.generate_wordcloud()
    if result is None:
        return jsonify({'error': '生成词云失败'}), 400
    
    return jsonify({'image': result})


@app.route('/api/sentiment-trend')
def get_sentiment_trend():
    """获取情感趋势分析"""
    if not data_loaded or processor is None:
        return jsonify({'error': '数据未加载'}), 400
    
    result = processor.get_sentiment_trend()
    if result is None:
        return jsonify({'error': '不支持此分析（仅网易云音乐数据）'}), 400
    
    return jsonify(result)


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
