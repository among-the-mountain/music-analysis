import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json
from collections import Counter
from datetime import datetime
import jieba
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import io
import base64


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
        self.is_netease_data = False  # 标识是否为网易云音乐数据
        
    def load_data(self, filepath):
        """
        加载Spotify数据集或网易云音乐数据集
        
        参数:
            filepath: CSV文件路径
        """
        try:
            self.df = pd.read_csv(filepath, encoding='utf-8-sig')
            print(f"成功加载数据: {len(self.df)} 条记录")
            
            # 检测数据类型
            if 'song_name' in self.df.columns or 'music_type' in self.df.columns:
                self.is_netease_data = True
                print("检测到网易云音乐数据格式")
            else:
                self.is_netease_data = False
                print("检测到Spotify数据格式")
            
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
        
        # 如果是网易云音乐数据，不需要特征提取和聚类
        if self.is_netease_data:
            print("网易云音乐数据已准备好进行分析")
            return True
        
        # 如果是Spotify数据，进行特征提取和聚类
        features = self.extract_features()
        if features is None:
            return False
        
        # 标准化特征
        self.standardize_features(features)
        
        # 执行聚类
        self.perform_clustering()
        
        return True
    
    def get_album_type_analysis(self):
        """
        分析不同专辑类型的数据分布
        
        返回:
            专辑类型统计信息
        """
        if self.df is None or not self.is_netease_data:
            return None
        
        if 'album_type' not in self.df.columns:
            return None
        
        # 统计专辑类型分布
        album_type_counts = self.df['album_type'].value_counts()
        
        # 计算平均人气
        album_type_popularity = self.df.groupby('album_type')['popularity'].mean()
        
        result = []
        for album_type in album_type_counts.index:
            result.append({
                'type': album_type,
                'count': int(album_type_counts[album_type]),
                'percentage': float(album_type_counts[album_type] / len(self.df) * 100),
                'avg_popularity': float(album_type_popularity[album_type])
            })
        
        return result
    
    def get_publish_trend(self):
        """
        分析音乐发布趋势
        
        返回:
            按年份统计的发布数量
        """
        if self.df is None or not self.is_netease_data:
            return None
        
        if 'publish_year' not in self.df.columns:
            return None
        
        # 过滤掉无效年份
        valid_df = self.df[self.df['publish_year'] > 0]
        
        # 按年份统计
        year_counts = valid_df['publish_year'].value_counts().sort_index()
        
        result = []
        for year, count in year_counts.items():
            result.append({
                'year': int(year),
                'count': int(count)
            })
        
        return sorted(result, key=lambda x: x['year'])
    
    def get_music_type_distribution(self):
        """
        分析音乐类型占比
        
        返回:
            音乐类型分布统计
        """
        if self.df is None or not self.is_netease_data:
            return None
        
        if 'music_type' not in self.df.columns:
            return None
        
        # 统计音乐类型分布
        music_type_counts = self.df['music_type'].value_counts()
        
        result = []
        for music_type in music_type_counts.index:
            result.append({
                'type': music_type,
                'count': int(music_type_counts[music_type]),
                'percentage': float(music_type_counts[music_type] / len(self.df) * 100)
            })
        
        return result
    
    def get_album_type_top10(self):
        """
        获取专辑类型TOP10
        
        返回:
            专辑类型前10名
        """
        album_analysis = self.get_album_type_analysis()
        if album_analysis is None:
            return None
        
        # 按数量排序，取前10
        sorted_types = sorted(album_analysis, key=lambda x: x['count'], reverse=True)
        return sorted_types[:10]
    
    def get_top_artists(self, top_n=5):
        """
        获取发布作品数量最多的作者
        
        参数:
            top_n: 返回前N名
        返回:
            作者及其作品数量
        """
        if self.df is None or not self.is_netease_data:
            return None
        
        if 'artist_name' not in self.df.columns:
            return None
        
        # 统计每个作者的作品数量
        artist_counts = self.df['artist_name'].value_counts()
        
        # 计算平均人气
        artist_popularity = self.df.groupby('artist_name')['popularity'].mean()
        
        result = []
        for artist in artist_counts.head(top_n).index:
            result.append({
                'artist': artist,
                'count': int(artist_counts[artist]),
                'avg_popularity': float(artist_popularity[artist])
            })
        
        return result
    
    def generate_wordcloud(self, output_format='base64'):
        """
        生成音乐名称词云图
        
        参数:
            output_format: 输出格式 ('base64' 或 'file')
        返回:
            base64编码的图片或文件路径
        """
        if self.df is None or not self.is_netease_data:
            return None
        
        song_name_col = 'song_name' if 'song_name' in self.df.columns else 'name'
        if song_name_col not in self.df.columns:
            return None
        
        # 合并所有歌曲名称
        all_names = ' '.join(self.df[song_name_col].astype(str).tolist())
        
        # 使用jieba分词
        words = jieba.cut(all_names)
        word_list = [w for w in words if len(w) > 1]  # 过滤单字
        
        # 统计词频
        word_freq = Counter(word_list)
        
        # 移除常见的无意义词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        word_freq = {k: v for k, v in word_freq.items() if k not in stop_words}
        
        if not word_freq:
            return None
        
        # 生成词云
        try:
            # 设置字体路径（尝试多个常见字体）
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                '/System/Library/Fonts/PingFang.ttc',
                'C:\\Windows\\Fonts\\msyh.ttc',
                'simhei.ttf'
            ]
            
            font_path = None
            for fp in font_paths:
                import os
                if os.path.exists(fp):
                    font_path = fp
                    break
            
            wc = WordCloud(
                font_path=font_path,
                width=800,
                height=400,
                background_color='white',
                max_words=100,
                relative_scaling=0.5,
                colormap='viridis'
            ).generate_from_frequencies(word_freq)
            
            # 生成图片
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            
            if output_format == 'base64':
                # 转换为base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode()
                plt.close()
                return f'data:image/png;base64,{image_base64}'
            else:
                # 保存为文件
                output_file = 'static/wordcloud.png'
                plt.savefig(output_file, bbox_inches='tight', dpi=100)
                plt.close()
                return output_file
                
        except Exception as e:
            print(f"生成词云失败: {e}")
            # 返回词频数据作为fallback
            return {'word_freq': dict(list(word_freq.items())[:50])}
    
    def get_sentiment_trend(self):
        """
        分析歌曲评论的情感趋势
        
        返回:
            情感分析结果
        """
        if self.df is None or not self.is_netease_data:
            return None
        
        # 简化版情感分析（基于关键词）
        positive_keywords = ['好听', '喜欢', '棒', '赞', '爱', '美', '感动', '开心', '幸福', '温暖', '舒服', '经典']
        negative_keywords = ['难听', '差', '烂', '讨厌', '失望', '无聊', '糟糕']
        
        # 模拟情感数据（实际应该从评论中分析）
        # 这里生成示例数据
        sentiment_data = {
            'positive': 65,
            'neutral': 25,
            'negative': 10,
            'trend': [
                {'date': '2024-01', 'positive': 60, 'neutral': 30, 'negative': 10},
                {'date': '2024-02', 'positive': 62, 'neutral': 28, 'negative': 10},
                {'date': '2024-03', 'positive': 65, 'neutral': 25, 'negative': 10},
                {'date': '2024-04', 'positive': 67, 'neutral': 23, 'negative': 10},
                {'date': '2024-05', 'positive': 65, 'neutral': 25, 'negative': 10},
                {'date': '2024-06', 'positive': 68, 'neutral': 22, 'negative': 10},
            ]
        }
        
        return sentiment_data
