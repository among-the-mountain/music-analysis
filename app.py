"""
Flask Web Application for Music Analysis
"""
from flask import Flask, render_template, jsonify, request
from analyzer import MusicAnalyzer
from visualizer import (
    create_radar_chart, 
    create_scatter_plot, 
    create_cluster_distribution,
    create_feature_heatmap,
    create_3d_scatter,
    create_all_clusters_radar
)
import os

app = Flask(__name__)

# Initialize the analyzer
analyzer = MusicAnalyzer()

# Load and process data on startup
analyzer.load_data()
analyzer.normalize_features()
analyzer.perform_clustering(n_clusters=5)


@app.route('/')
def index():
    """
    Main page - Dashboard
    """
    # Get summary statistics
    stats = analyzer.get_summary_statistics()
    cluster_stats = analyzer.get_cluster_characteristics()
    
    return render_template('index.html', 
                         total_tracks=stats['total_tracks'],
                         n_clusters=analyzer.n_clusters,
                         cluster_stats=cluster_stats)


@app.route('/analysis')
def analysis():
    """
    Analysis page with detailed visualizations
    """
    cluster_stats = analyzer.get_cluster_characteristics()
    
    # Create visualizations
    scatter_html = create_scatter_plot(
        analyzer.df.copy(), 
        'energy', 
        'valence', 
        analyzer.get_cluster_name
    )
    
    distribution_html = create_cluster_distribution(
        analyzer.df.copy(),
        analyzer.get_cluster_name
    )
    
    heatmap_html = create_feature_heatmap(cluster_stats)
    
    radar_all_html = create_all_clusters_radar(
        cluster_stats,
        analyzer.get_cluster_name
    )
    
    scatter_3d_html = create_3d_scatter(
        analyzer.df.copy(),
        analyzer.get_cluster_name
    )
    
    return render_template('analysis.html',
                         scatter_plot=scatter_html,
                         distribution_plot=distribution_html,
                         heatmap=heatmap_html,
                         radar_all=radar_all_html,
                         scatter_3d=scatter_3d_html)


@app.route('/clusters')
def clusters():
    """
    Clusters page showing individual cluster details
    """
    cluster_stats = analyzer.get_cluster_characteristics()
    
    # Create data for each cluster
    clusters_data = []
    for cluster_id in range(analyzer.n_clusters):
        cluster_name = analyzer.get_cluster_name(cluster_id)
        radar_html = create_radar_chart(cluster_stats, cluster_id, cluster_name)
        tracks = analyzer.get_tracks_by_cluster(cluster_id, limit=10)
        
        clusters_data.append({
            'id': cluster_id,
            'name': cluster_name,
            'radar_chart': radar_html,
            'tracks': tracks.to_dict('records') if not tracks.empty else [],
            'count': int(cluster_stats.loc[cluster_id, 'count']),
            'features': {
                'danceability': float(cluster_stats.loc[cluster_id, 'danceability']),
                'energy': float(cluster_stats.loc[cluster_id, 'energy']),
                'valence': float(cluster_stats.loc[cluster_id, 'valence']),
                'acousticness': float(cluster_stats.loc[cluster_id, 'acousticness']),
            }
        })
    
    return render_template('clusters.html', clusters=clusters_data)


@app.route('/api/cluster/<int:cluster_id>')
def get_cluster_data(cluster_id):
    """
    API endpoint to get data for a specific cluster
    
    Args:
        cluster_id: ID of the cluster
        
    Returns:
        JSON response with cluster data
    """
    if cluster_id < 0 or cluster_id >= analyzer.n_clusters:
        return jsonify({'error': 'Invalid cluster ID'}), 400
    
    cluster_stats = analyzer.get_cluster_characteristics()
    tracks = analyzer.get_tracks_by_cluster(cluster_id, limit=20)
    
    return jsonify({
        'cluster_id': cluster_id,
        'name': analyzer.get_cluster_name(cluster_id),
        'features': cluster_stats.loc[cluster_id].to_dict(),
        'tracks': tracks.to_dict('records')
    })


@app.route('/api/recalculate', methods=['POST'])
def recalculate_clusters():
    """
    API endpoint to recalculate clusters with different parameters
    
    Returns:
        JSON response with success status
    """
    try:
        data = request.get_json()
        n_clusters = int(data.get('n_clusters', 5))
        
        if n_clusters < 2 or n_clusters > 10:
            return jsonify({'error': 'Number of clusters must be between 2 and 10'}), 400
        
        analyzer.perform_clustering(n_clusters=n_clusters)
        
        return jsonify({
            'success': True,
            'n_clusters': n_clusters,
            'message': f'Clustering recalculated with {n_clusters} clusters'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """
    API endpoint to get overall statistics
    
    Returns:
        JSON response with statistics
    """
    stats = analyzer.get_summary_statistics()
    cluster_stats = analyzer.get_cluster_characteristics()
    
    return jsonify({
        'total_tracks': stats['total_tracks'],
        'n_clusters': analyzer.n_clusters,
        'cluster_sizes': cluster_stats['count'].to_dict(),
        'feature_stats': stats['feature_stats']
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Music Analysis Visualization System")
    print("=" * 60)
    print(f"Loaded {len(analyzer.df)} tracks")
    print(f"Created {analyzer.n_clusters} emotion clusters")
    print("=" * 60)
    print("Starting Flask server...")
    print("Visit: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
