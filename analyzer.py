"""
Music Data Analysis Module
Handles data loading, preprocessing, clustering, and analysis
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os


class MusicAnalyzer:
    """
    Main class for music data analysis and clustering
    """
    
    def __init__(self, data_path=None):
        """
        Initialize the analyzer
        
        Args:
            data_path: Path to the Spotify dataset CSV file
        """
        if data_path is None:
            # Default to sample data
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, 'data', 'sample_spotify_data.csv')
        
        self.data_path = data_path
        self.df = None
        self.scaled_features = None
        self.scaler = StandardScaler()
        self.kmeans = None
        self.n_clusters = 5
        
        # Features to extract for analysis
        self.feature_columns = [
            'danceability',
            'energy',
            'valence',
            'acousticness',
            'instrumentalness',
            'speechiness',
            'liveness'
        ]
    
    def load_data(self):
        """
        Load the Spotify dataset
        
        Returns:
            DataFrame: Loaded dataset
        """
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} tracks from dataset")
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def extract_features(self):
        """
        Extract relevant features from the dataset
        
        Returns:
            DataFrame: Features dataframe
        """
        if self.df is None:
            self.load_data()
        
        # Extract only the feature columns
        features = self.df[self.feature_columns].copy()
        
        # Handle missing values
        features = features.fillna(features.mean())
        
        return features
    
    def normalize_features(self, features=None):
        """
        Normalize features using StandardScaler
        
        Args:
            features: Features to normalize (if None, will extract from data)
            
        Returns:
            numpy.ndarray: Normalized features
        """
        if features is None:
            features = self.extract_features()
        
        # Fit and transform the features
        self.scaled_features = self.scaler.fit_transform(features)
        
        print("Features normalized using StandardScaler")
        return self.scaled_features
    
    def perform_clustering(self, n_clusters=5):
        """
        Perform K-Means clustering on the normalized features
        
        Args:
            n_clusters: Number of clusters to create
            
        Returns:
            numpy.ndarray: Cluster labels for each track
        """
        self.n_clusters = n_clusters
        
        if self.scaled_features is None:
            self.normalize_features()
        
        # Initialize and fit K-Means
        self.kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        
        cluster_labels = self.kmeans.fit_predict(self.scaled_features)
        
        # Add cluster labels to dataframe
        self.df['cluster'] = cluster_labels
        
        print(f"Clustering completed with {n_clusters} clusters")
        return cluster_labels
    
    def get_cluster_characteristics(self):
        """
        Calculate average characteristics for each cluster
        
        Returns:
            DataFrame: Cluster characteristics
        """
        if 'cluster' not in self.df.columns:
            self.perform_clustering()
        
        # Group by cluster and calculate mean for each feature
        cluster_stats = self.df.groupby('cluster')[self.feature_columns].mean()
        
        # Add cluster size
        cluster_stats['count'] = self.df.groupby('cluster').size()
        
        return cluster_stats
    
    def get_cluster_name(self, cluster_id):
        """
        Get a descriptive name for a cluster based on its characteristics
        
        Args:
            cluster_id: ID of the cluster
            
        Returns:
            str: Descriptive name for the cluster
        """
        if 'cluster' not in self.df.columns:
            return f"Cluster {cluster_id}"
        
        cluster_data = self.df[self.df['cluster'] == cluster_id][self.feature_columns].mean()
        
        # Determine dominant characteristics
        if cluster_data['energy'] > 0.7 and cluster_data['valence'] > 0.7:
            return "🎉 Energetic & Happy"
        elif cluster_data['energy'] > 0.7 and cluster_data['valence'] < 0.4:
            return "🔥 Intense & Dark"
        elif cluster_data['danceability'] > 0.7 and cluster_data['energy'] > 0.6:
            return "💃 Dance Party"
        elif cluster_data['acousticness'] > 0.5 and cluster_data['energy'] < 0.5:
            return "🎸 Acoustic & Calm"
        elif cluster_data['valence'] < 0.4 and cluster_data['energy'] < 0.5:
            return "😢 Melancholic"
        else:
            return f"🎵 Cluster {cluster_id + 1}"
    
    def get_tracks_by_cluster(self, cluster_id, limit=10):
        """
        Get top tracks in a specific cluster
        
        Args:
            cluster_id: ID of the cluster
            limit: Maximum number of tracks to return
            
        Returns:
            DataFrame: Tracks in the cluster
        """
        if 'cluster' not in self.df.columns:
            self.perform_clustering()
        
        cluster_tracks = self.df[self.df['cluster'] == cluster_id].copy()
        
        # Sort by popularity if available
        if 'popularity' in cluster_tracks.columns:
            cluster_tracks = cluster_tracks.sort_values('popularity', ascending=False)
        
        return cluster_tracks.head(limit)
    
    def get_summary_statistics(self):
        """
        Get summary statistics for the dataset
        
        Returns:
            dict: Summary statistics
        """
        if self.df is None:
            self.load_data()
        
        stats = {
            'total_tracks': len(self.df),
            'feature_stats': self.df[self.feature_columns].describe().to_dict(),
            'avg_popularity': self.df['popularity'].mean() if 'popularity' in self.df.columns else 0
        }
        
        return stats
