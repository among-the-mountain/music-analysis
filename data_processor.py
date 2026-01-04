import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json


class MusicDataProcessor:
    """处理音乐数据的类，包括特征提取、标准化和聚类"""
    
    def __init__(self, n_clusters=5):
        """
        初始化音乐数据处理器
        
        参数:
            n_clusters: K-Means聚类的簇数量
        """
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = None
        self.feature_columns = [
            'danceability', 'energy', 'valence', 
            'acousticness', 'instrumentalness', 'liveness', 'speechiness'
        ]
        self.df = None
        self.scaled_features = None
        
    def load_data(self, filepath):
        """
        加载Spotify数据集
        
        参数:
            filepath: CSV文件路径
        """
        try:
            self.df = pd.read_csv(filepath)
            print(f"成功加载数据: {len(self.df)} 条记录")
            return True
        except Exception as e:
            print(f"加载数据失败: {e}")
            return False
    
    def extract_features(self):
        """提取多维特征"""
        if self.df is None:
            print("请先加载数据")
            return None
        
        # 确保所有需要的列都存在
        available_features = [col for col in self.feature_columns if col in self.df.columns]
        
        if not available_features:
            print("数据集中没有找到需要的特征列")
            return None
        
        # 提取特征并处理缺失值
        features = self.df[available_features].fillna(0)
        return features
    
    def standardize_features(self, features):
        """
        使用StandardScaler标准化特征
        
        参数:
            features: 特征数据框
        """
        self.scaled_features = self.scaler.fit_transform(features)
        print("特征标准化完成")
        return self.scaled_features
    
    def perform_clustering(self, features=None):
        """
        执行K-Means聚类
        
        参数:
            features: 要聚类的特征，如果为None则使用已标准化的特征
        """
        if features is None:
            if self.scaled_features is None:
                print("请先标准化特征")
                return None
            features = self.scaled_features
        
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init='auto')
        clusters = self.kmeans.fit_predict(features)
        
        self.df['cluster'] = clusters
        print(f"聚类完成，共{self.n_clusters}个簇")
        return clusters
    
    def get_cluster_stats(self):
        """获取每个簇的统计信息"""
        if self.df is None or 'cluster' not in self.df.columns:
            return None
        
        stats = []
        available_features = [col for col in self.feature_columns if col in self.df.columns]
        
        for cluster_id in range(self.n_clusters):
            cluster_data = self.df[self.df['cluster'] == cluster_id]
            cluster_stats = {
                'cluster_id': int(cluster_id),
                'count': int(len(cluster_data)),
                'features': {}
            }
            
            for feature in available_features:
                cluster_stats['features'][feature] = float(cluster_data[feature].mean())
            
            stats.append(cluster_stats)
        
        return stats
    
    def get_sample_tracks(self, n_samples=10):
        """获取每个簇的样本音乐"""
        if self.df is None or 'cluster' not in self.df.columns:
            return None
        
        samples = []
        for cluster_id in range(self.n_clusters):
            cluster_data = self.df[self.df['cluster'] == cluster_id]
            sample_data = cluster_data.head(n_samples)
            
            # 构建样本信息
            cluster_samples = {
                'cluster_id': int(cluster_id),
                'tracks': []
            }
            
            for _, row in sample_data.iterrows():
                track_info = {
                    'name': str(row.get('name', row.get('track_name', 'Unknown'))),
                    'artists': str(row.get('artists', row.get('artist_name', 'Unknown'))),
                }
                
                # 添加可用的特征
                for feature in self.feature_columns:
                    if feature in row:
                        track_info[feature] = float(row[feature])
                
                cluster_samples['tracks'].append(track_info)
            
            samples.append(cluster_samples)
        
        return samples
    
    def process_pipeline(self, filepath):
        """
        完整的数据处理流程
        
        参数:
            filepath: 数据文件路径
        
        返回:
            处理成功返回True，否则返回False
        """
        # 加载数据
        if not self.load_data(filepath):
            return False
        
        # 提取特征
        features = self.extract_features()
        if features is None:
            return False
        
        # 标准化特征
        self.standardize_features(features)
        
        # 执行聚类
        self.perform_clustering()
        
        return True
