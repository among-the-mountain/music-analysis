"""
生成示例音乐数据
用于测试和演示，无需下载完整的Kaggle数据集
"""

import pandas as pd
import numpy as np

def generate_sample_data(n_samples=1000, output_file='spotify_tracks.csv'):
    """
    生成示例Spotify音乐数据
    
    参数:
        n_samples: 生成的样本数量
        output_file: 输出文件路径
    """
    np.random.seed(42)
    
    # 艺术家列表
    artists = [
        'Taylor Swift', 'Ed Sheeran', 'Beyoncé', 'Drake', 'Ariana Grande',
        'The Weeknd', 'Bruno Mars', 'Post Malone', 'Billie Eilish', 'Justin Bieber',
        'Adele', 'Coldplay', 'Imagine Dragons', 'Maroon 5', 'Rihanna',
        'Katy Perry', 'Lady Gaga', 'Dua Lipa', 'Shawn Mendes', 'Sam Smith'
    ]
    
    # 歌曲名称前缀
    song_prefixes = [
        'Love', 'Dancing', 'Summer', 'Night', 'Dream', 'Heart', 'Paradise',
        'Midnight', 'Forever', 'Beautiful', 'Wonderful', 'Perfect', 'Golden',
        'Starlight', 'Moonlight', 'Sunshine', 'Firefly', 'Crystal', 'Ocean'
    ]
    
    song_suffixes = [
        'Song', 'Nights', 'Days', 'Memories', 'Story', 'Feelings', 'Vibes',
        'Dreams', 'Paradise', 'Heaven', 'Magic', 'Wonder', 'Soul', 'Harmony'
    ]
    
    # 生成数据
    data = {
        'name': [
            f"{np.random.choice(song_prefixes)} {np.random.choice(song_suffixes)}" 
            for _ in range(n_samples)
        ],
        'artists': np.random.choice(artists, n_samples),
        'danceability': np.random.beta(5, 2, n_samples),  # 偏向高值
        'energy': np.random.beta(3, 3, n_samples),  # 均匀分布
        'valence': np.random.beta(3, 3, n_samples),  # 均匀分布
        'acousticness': np.random.beta(2, 5, n_samples),  # 偏向低值
        'instrumentalness': np.random.beta(1, 9, n_samples),  # 大多数歌曲器乐度低
        'liveness': np.random.beta(2, 8, n_samples),  # 偏向低值
        'speechiness': np.random.beta(1, 9, n_samples),  # 偏向低值
    }
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 添加一些额外的列（虽然不用于分析）
    df['duration_ms'] = np.random.randint(120000, 300000, n_samples)
    df['popularity'] = np.random.randint(0, 100, n_samples)
    df['tempo'] = np.random.randint(60, 180, n_samples)
    
    # 保存到CSV
    df.to_csv(output_file, index=False)
    print(f"✓ 成功生成 {n_samples} 条示例数据")
    print(f"✓ 保存到: {output_file}")
    print("\n数据预览:")
    print(df.head())
    print("\n特征统计:")
    print(df[['danceability', 'energy', 'valence', 'acousticness']].describe())
    
    return df

if __name__ == '__main__':
    print("=" * 60)
    print("Spotify 音乐数据生成器")
    print("=" * 60)
    print("\n这将生成示例数据用于测试应用...")
    
    # 生成1000条示例数据
    generate_sample_data(n_samples=1000)
    
    print("\n" + "=" * 60)
    print("完成！现在可以运行 'python app.py' 启动应用")
    print("=" * 60)
