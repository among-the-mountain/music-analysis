"""
网易云音乐数据爬虫
爬取热门歌单的音乐数据
"""

import requests
import json
import time
import random
import pandas as pd
from datetime import datetime
import os


class NetEaseMusicScraper:
    """网易云音乐爬虫类"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://music.163.com/'
        }
        self.base_url = 'https://music.163.com/api'
        
    def get_hot_playlists(self, limit=50):
        """
        获取热门歌单列表
        
        参数:
            limit: 获取歌单数量
        返回:
            歌单ID列表
        """
        print(f"正在获取热门歌单...")
        # 网易云音乐API
        url = f'https://music.163.com/api/playlist/list'
        params = {
            'cat': '全部',
            'order': 'hot',
            'limit': limit,
            'offset': 0
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'playlists' in data:
                    playlist_ids = [p['id'] for p in data['playlists']]
                    print(f"✓ 成功获取 {len(playlist_ids)} 个热门歌单")
                    return playlist_ids
        except Exception as e:
            print(f"获取歌单失败: {e}")
        
        # 如果API失败，使用预定义的热门歌单ID
        print("使用预定义热门歌单ID...")
        return self._get_default_playlist_ids()
    
    def _get_default_playlist_ids(self):
        """返回一些知名的歌单ID"""
        return [
            3778678,    # 云音乐热歌榜
            19723756,   # 云音乐飙升榜
            3779629,    # 云音乐新歌榜
            2884035,    # 华语金曲榜
            991319590,  # 抖音排行榜
        ]
    
    def get_playlist_tracks(self, playlist_id):
        """
        获取歌单中的歌曲信息
        
        参数:
            playlist_id: 歌单ID
        返回:
            歌曲信息列表
        """
        url = f'https://music.163.com/api/playlist/detail'
        params = {'id': playlist_id}
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'tracks' in data['result']:
                    tracks = data['result']['tracks']
                    print(f"  ✓ 歌单 {playlist_id}: 获取 {len(tracks)} 首歌曲")
                    return tracks
        except Exception as e:
            print(f"  获取歌单详情失败 {playlist_id}: {e}")
        
        return []
    
    def get_song_comments(self, song_id, limit=20):
        """
        获取歌曲评论
        
        参数:
            song_id: 歌曲ID
            limit: 评论数量
        返回:
            评论列表
        """
        url = f'https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}'
        params = {
            'limit': limit,
            'offset': 0
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'comments' in data:
                    return [c['content'] for c in data['comments']]
        except Exception as e:
            print(f"  获取评论失败: {e}")
        
        return []
    
    def parse_track_info(self, track, include_comments=False):
        """
        解析歌曲信息
        
        参数:
            track: 原始歌曲数据
            include_comments: 是否包含评论
        返回:
            结构化的歌曲信息
        """
        try:
            # 基本信息
            track_info = {
                'song_id': track.get('id', ''),
                'song_name': track.get('name', '未知'),
                'artist_name': ', '.join([a.get('name', '') for a in track.get('artists', [])]),
                'album_name': track.get('album', {}).get('name', '未知专辑'),
                'album_type': track.get('album', {}).get('type', '未知类型'),
                'duration_ms': track.get('duration', 0),
                'popularity': track.get('popularity', 0),
            }
            
            # 发布时间
            publish_time = track.get('album', {}).get('publishTime', 0)
            if publish_time:
                track_info['publish_date'] = datetime.fromtimestamp(publish_time / 1000).strftime('%Y-%m-%d')
                track_info['publish_year'] = datetime.fromtimestamp(publish_time / 1000).year
            else:
                track_info['publish_date'] = ''
                track_info['publish_year'] = 0
            
            # 音乐类型（从标签或默认值）
            music_type = '流行'  # 默认类型
            if 'type' in track:
                music_type = track.get('type', '流行')
            track_info['music_type'] = music_type
            
            # 获取评论（如果需要）
            if include_comments:
                comments = self.get_song_comments(track_info['song_id'], limit=10)
                track_info['comments'] = comments
            else:
                track_info['comments'] = []
            
            return track_info
            
        except Exception as e:
            print(f"  解析歌曲信息失败: {e}")
            return None
    
    def scrape_music_data(self, num_playlists=5, include_comments=False, output_file='netease_music_data.csv'):
        """
        爬取网易云音乐数据
        
        参数:
            num_playlists: 爬取歌单数量
            include_comments: 是否包含评论
            output_file: 输出文件路径
        返回:
            DataFrame
        """
        print("=" * 60)
        print("网易云音乐数据爬虫启动")
        print("=" * 60)
        
        # 获取热门歌单
        playlist_ids = self.get_hot_playlists(limit=num_playlists)[:num_playlists]
        
        all_tracks = []
        seen_ids = set()
        
        # 遍历每个歌单
        for idx, playlist_id in enumerate(playlist_ids, 1):
            print(f"\n[{idx}/{len(playlist_ids)}] 处理歌单 {playlist_id}...")
            
            # 获取歌单歌曲
            tracks = self.get_playlist_tracks(playlist_id)
            
            # 解析每首歌曲
            for track in tracks:
                track_info = self.parse_track_info(track, include_comments)
                if track_info and track_info['song_id'] not in seen_ids:
                    all_tracks.append(track_info)
                    seen_ids.add(track_info['song_id'])
            
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(0.5, 1.5))
        
        print(f"\n✓ 共爬取 {len(all_tracks)} 首不重复的歌曲")
        
        # 转换为DataFrame
        df = pd.DataFrame(all_tracks)
        
        # 保存到文件
        if output_file:
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"✓ 数据已保存到: {output_file}")
        
        return df


def generate_sample_netease_data(n_samples=500, output_file='netease_music_data.csv'):
    """
    生成网易云音乐示例数据（用于测试，无需实际爬取）
    
    参数:
        n_samples: 生成样本数量
        output_file: 输出文件路径
    返回:
        DataFrame
    """
    import numpy as np
    
    print("=" * 60)
    print("生成网易云音乐示例数据")
    print("=" * 60)
    
    np.random.seed(42)
    
    # 中文歌手列表
    artists = [
        '周杰伦', '林俊杰', '邓紫棋', '薛之谦', '毛不易',
        '李荣浩', '陈奕迅', '张学友', '王力宏', '孙燕姿',
        '五月天', '许嵩', '汪苏泷', '徐佳莹', '田馥甄',
        '蔡依林', '张杰', '华晨宇', '李宇春', '周深'
    ]
    
    # 专辑类型
    album_types = ['录音室专辑', '现场专辑', 'EP/单曲', '精选集', '合辑']
    album_type_weights = [0.5, 0.1, 0.25, 0.1, 0.05]
    
    # 音乐类型
    music_types = ['流行', '摇滚', '民谣', '电子', '说唱', '古风', '轻音乐', '爵士', 'R&B']
    music_type_weights = [0.4, 0.15, 0.15, 0.1, 0.08, 0.05, 0.03, 0.02, 0.02]
    
    # 歌曲名称元素
    song_prefixes = [
        '晴天', '夜曲', '告白气球', '七里香', '青花瓷', '彩虹',
        '稻香', '不能说的秘密', '等你下课', '说好不哭', '爱情转移',
        '十年', '富士山下', '好久不见', '浮夸', '红玫瑰',
        '演员', '丑八怪', '认真的雪', '意外', '天后'
    ]
    
    song_titles = []
    for _ in range(n_samples):
        if random.random() < 0.3:
            # 使用预定义标题
            song_titles.append(random.choice(song_prefixes))
        else:
            # 组合生成
            parts = ['爱', '心', '梦', '夜', '天', '海', '星', '月', '雨', '风',
                    '花', '城', '路', '桥', '歌', '诗', '舞', '光', '影', '声']
            title = ''.join(random.choices(parts, k=random.randint(2, 4)))
            song_titles.append(title)
    
    # 生成数据
    current_year = 2024
    # 生成年份分布（2000-2024，共25年）
    year_probs = [0.02] * 10 + [0.05] * 5 + [0.1] * 5 + [0.15] * 5
    # 归一化确保总和为1
    year_probs = np.array(year_probs) / sum(year_probs)
    years = np.random.choice(range(2000, current_year + 1), n_samples, p=year_probs)
    
    data = {
        'song_id': range(1000000, 1000000 + n_samples),
        'song_name': song_titles,
        'artist_name': np.random.choice(artists, n_samples),
        'album_name': [f'{artist}专辑_{random.randint(1, 10)}' 
                      for artist in np.random.choice(artists, n_samples)],
        'album_type': np.random.choice(album_types, n_samples, p=album_type_weights),
        'music_type': np.random.choice(music_types, n_samples, p=music_type_weights),
        'duration_ms': np.random.randint(180000, 360000, n_samples),
        'popularity': np.random.randint(0, 100, n_samples),
        'publish_year': years,
        'publish_date': [f'{year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}' 
                        for year in years],
    }
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存到CSV
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✓ 成功生成 {n_samples} 条示例数据")
    print(f"✓ 保存到: {output_file}")
    print("\n数据预览:")
    print(df.head(10))
    print("\n数据统计:")
    print(df[['music_type', 'album_type', 'publish_year']].describe())
    
    return df


if __name__ == '__main__':
    # 可以选择真实爬取或生成示例数据
    
    # 方式1: 生成示例数据（推荐用于测试）
    print("\n选择数据获取方式:")
    print("1. 生成示例数据（快速，用于测试）")
    print("2. 爬取真实数据（需要网络，可能受限）")
    
    choice = input("\n请选择 (1/2，默认1): ").strip() or '1'
    
    if choice == '2':
        # 真实爬取
        scraper = NetEaseMusicScraper()
        df = scraper.scrape_music_data(
            num_playlists=5,
            include_comments=False,
            output_file='netease_music_data.csv'
        )
    else:
        # 生成示例数据
        df = generate_sample_netease_data(
            n_samples=500,
            output_file='netease_music_data.csv'
        )
    
    print("\n" + "=" * 60)
    print("完成！现在可以运行 'python app.py' 启动应用")
    print("=" * 60)
