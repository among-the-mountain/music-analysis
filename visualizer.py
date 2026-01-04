"""
Visualization Module
Creates interactive charts using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots


def create_radar_chart(cluster_stats, cluster_id, cluster_name):
    """
    Create a radar chart for cluster characteristics
    
    Args:
        cluster_stats: DataFrame with cluster statistics
        cluster_id: ID of the cluster
        cluster_name: Name of the cluster
        
    Returns:
        str: HTML div containing the radar chart
    """
    features = ['danceability', 'energy', 'valence', 'acousticness', 
                'instrumentalness', 'speechiness', 'liveness']
    
    values = cluster_stats.loc[cluster_id, features].values.tolist()
    values.append(values[0])  # Close the radar chart
    
    feature_labels = ['Danceability', 'Energy', 'Valence (Happiness)', 
                     'Acousticness', 'Instrumentalness', 'Speechiness', 'Liveness']
    feature_labels.append(feature_labels[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=feature_labels,
        fill='toself',
        name=cluster_name,
        line_color='rgb(99, 110, 250)',
        fillcolor='rgba(99, 110, 250, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title=dict(
            text=f"{cluster_name} - Feature Profile",
            x=0.5,
            xanchor='center'
        ),
        height=450,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig.to_html(include_plotlyjs=False, div_id=f"radar_{cluster_id}")


def create_all_clusters_radar(cluster_stats, get_cluster_name_func):
    """
    Create radar charts for all clusters
    
    Args:
        cluster_stats: DataFrame with cluster statistics
        get_cluster_name_func: Function to get cluster names
        
    Returns:
        str: HTML div containing all radar charts
    """
    features = ['danceability', 'energy', 'valence', 'acousticness', 
                'instrumentalness', 'speechiness', 'liveness']
    
    feature_labels = ['Danceability', 'Energy', 'Valence', 
                     'Acousticness', 'Instrumentalness', 'Speechiness', 'Liveness']
    
    fig = go.Figure()
    
    colors = ['rgb(99, 110, 250)', 'rgb(239, 85, 59)', 'rgb(0, 204, 150)', 
              'rgb(171, 99, 250)', 'rgb(255, 161, 90)']
    
    for idx, cluster_id in enumerate(cluster_stats.index):
        values = cluster_stats.loc[cluster_id, features].values.tolist()
        values.append(values[0])
        
        labels = feature_labels.copy()
        labels.append(labels[0])
        
        cluster_name = get_cluster_name_func(cluster_id)
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=cluster_name,
            line_color=colors[idx % len(colors)],
            fillcolor=colors[idx % len(colors)].replace('rgb', 'rgba').replace(')', ', 0.2)')
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title=dict(
            text="All Music Emotion Clusters - Feature Comparison",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        height=600,
        margin=dict(l=100, r=100, t=100, b=80),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1
        )
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="radar_all")


def create_scatter_plot(df, feature_x='energy', feature_y='valence', get_cluster_name_func=None):
    """
    Create scatter plot of tracks colored by cluster
    
    Args:
        df: DataFrame with track data
        feature_x: Feature for x-axis
        feature_y: Feature for y-axis
        get_cluster_name_func: Function to get cluster names
        
    Returns:
        str: HTML div containing the scatter plot
    """
    # Add cluster names to dataframe
    if get_cluster_name_func and 'cluster' in df.columns:
        df['cluster_name'] = df['cluster'].apply(get_cluster_name_func)
    else:
        df['cluster_name'] = df['cluster'].astype(str)
    
    fig = px.scatter(
        df,
        x=feature_x,
        y=feature_y,
        color='cluster_name',
        hover_data=['track_name', 'artists', 'danceability', 'energy', 'valence'],
        title=f"Music Distribution: {feature_x.title()} vs {feature_y.title()}",
        labels={
            feature_x: feature_x.title(),
            feature_y: feature_y.title(),
            'cluster_name': 'Emotion Cluster'
        },
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='white')))
    
    fig.update_layout(
        height=600,
        hovermode='closest',
        margin=dict(l=80, r=80, t=100, b=80),
        font=dict(size=12)
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="scatter_plot")


def create_cluster_distribution(df, get_cluster_name_func):
    """
    Create bar chart showing distribution of tracks across clusters
    
    Args:
        df: DataFrame with track data
        get_cluster_name_func: Function to get cluster names
        
    Returns:
        str: HTML div containing the bar chart
    """
    cluster_counts = df['cluster'].value_counts().sort_index()
    cluster_names = [get_cluster_name_func(i) for i in cluster_counts.index]
    
    fig = go.Figure(data=[
        go.Bar(
            x=cluster_names,
            y=cluster_counts.values,
            marker_color='rgb(99, 110, 250)',
            text=cluster_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Track Distribution Across Emotion Clusters",
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Cluster",
        yaxis_title="Number of Tracks",
        height=400,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="cluster_dist")


def create_feature_heatmap(cluster_stats):
    """
    Create heatmap of cluster features
    
    Args:
        cluster_stats: DataFrame with cluster statistics
        
    Returns:
        str: HTML div containing the heatmap
    """
    features = ['danceability', 'energy', 'valence', 'acousticness', 
                'instrumentalness', 'speechiness', 'liveness']
    
    data = cluster_stats[features].values
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=['Danceability', 'Energy', 'Valence', 'Acousticness', 
           'Instrumentalness', 'Speechiness', 'Liveness'],
        y=[f'Cluster {i}' for i in range(len(cluster_stats))],
        colorscale='Viridis',
        text=np.round(data, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Feature Value")
    ))
    
    fig.update_layout(
        title=dict(
            text="Cluster Feature Heatmap",
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="heatmap")


def create_3d_scatter(df, get_cluster_name_func):
    """
    Create 3D scatter plot of tracks
    
    Args:
        df: DataFrame with track data
        get_cluster_name_func: Function to get cluster names
        
    Returns:
        str: HTML div containing the 3D scatter plot
    """
    df['cluster_name'] = df['cluster'].apply(get_cluster_name_func)
    
    fig = px.scatter_3d(
        df,
        x='danceability',
        y='energy',
        z='valence',
        color='cluster_name',
        hover_data=['track_name', 'artists'],
        title="3D Music Feature Space",
        labels={
            'danceability': 'Danceability',
            'energy': 'Energy',
            'valence': 'Valence (Happiness)',
            'cluster_name': 'Emotion Cluster'
        },
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_traces(marker=dict(size=5, opacity=0.8))
    
    fig.update_layout(
        height=700,
        margin=dict(l=0, r=0, t=100, b=0),
        scene=dict(
            xaxis_title='Danceability',
            yaxis_title='Energy',
            zaxis_title='Valence'
        )
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="scatter_3d")
