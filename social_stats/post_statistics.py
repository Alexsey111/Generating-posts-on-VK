import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class PostStatistics:
    """Класс для сбора и анализа статистики по постам в ВКонтакте"""
    
    def __init__(self, vk_api_key: str, group_id: int):
        self.vk_api_key = vk_api_key
        self.group_id = group_id
        self.base_url = 'https://api.vk.com/method'
    
    def _make_request(self, method: str, params: Dict) -> Dict:
        """Выполняет запрос к VK API"""
        params['access_token'] = self.vk_api_key
        params['v'] = '5.236'
        
        response = requests.get(f'{self.base_url}/{method}', params=params).json()
        
        if 'error' in response:
            raise Exception(f"VK API Error: {response['error']['error_msg']}")
        
        return response.get('response', {})
    
    def get_posts(self, count: int = 100, offset: int = 0) -> List[Dict]:
        """Получает список постов со стены группы"""
        params = {
            'owner_id': f'-{self.group_id}',
            'count': min(count, 100),
            'offset': offset,
            'extended': 1
        }
        
        response = self._make_request('wall.get', params)
        return response.get('items', []) if isinstance(response, dict) else []
    
    def get_post_stats(self, post_id: int) -> Dict:
        """Получает детальную статистику по одному посту"""
        params = {
            'owner_id': f'-{self.group_id}',
            'post_id': post_id
        }
        
        posts = self._make_request('wall.getById', params)
        
        if not posts:
            return {}
        
        post = posts[0]
        
        return {
            'post_id': post.get('id'),
            'date': datetime.fromtimestamp(post.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S'),
            'text': post.get('text', '')[:100] + ('...' if len(post.get('text', '')) > 100 else ''),
            'likes': post.get('likes', {}).get('count', 0),
            'comments': post.get('comments', {}).get('count', 0),
            'reposts': post.get('reposts', {}).get('count', 0),
            'views': post.get('views', {}).get('count', 0),
        }
    
    def get_group_stats(self, date_from: str = None, date_to: str = None) -> Dict:
        """
        Получает статистику группы за период
        date_from, date_to: "YYYY-MM-DD"
        """
        if not date_from:
            date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = datetime.now().strftime('%Y-%m-%d')
        
        # Преобразуем даты в Unix timestamp
        date_from_ts = int(datetime.strptime(date_from, '%Y-%m-%d').timestamp())
        date_to_ts = int(datetime.strptime(date_to, '%Y-%m-%d').timestamp())
        
        params = {
            'group_id': self.group_id,
            'timestamp_from': date_from_ts,
            'timestamp_to': date_to_ts
        }
        
        stats = self._make_request('stats.get', params)
        
        if not stats:
            return {'error': 'No stats available'}
        
        # Выбираем первый элемент если это массив
        if isinstance(stats, list) and stats:
            stats = stats[0]
        
        return {
            'period': f'{date_from} to {date_to}',
            'views': stats.get('views', 0),
            'visitors': stats.get('visitors', 0),
            'reach': stats.get('reach', 0),
            'reach_subscribers': stats.get('reach_subscribers', 0),
            'positive_feedback': stats.get('positive_feedback', 0),
            'negative_feedback': stats.get('negative_feedback', 0),
        }
    
    def get_followers_count(self) -> int:
        """Получает количество подписчиков группы"""
        params = {'group_id': self.group_id}
        
        response = self._make_request('groups.getMembers', params)
        return response.get('count', 0) if isinstance(response, dict) else 0
    
    def get_likes_list(self, owner_id: int, item_id: int, count: int = 100) -> List[int]:
        """Получает список пользователей, поставивших лайк"""
        params = {
            'type': 'post',
            'owner_id': owner_id,
            'item_id': item_id,
            'count': min(count, 100),
            'extended': 0
        }
        
        response = self._make_request('likes.getList', params)
        return response.get('items', []) if isinstance(response, dict) else []
    
    def get_comments(self, owner_id: int, post_id: int, count: int = 100) -> List[Dict]:
        """Получает комментарии к посту"""
        params = {
            'owner_id': owner_id,
            'post_id': post_id,
            'count': min(count, 100),
            'extended': 1
        }
        
        response = self._make_request('wall.getComments', params)
        
        if not isinstance(response, dict):
            return []
        
        items = response.get('items', [])
        
        return [{
            'id': item.get('id'),
            'text': item.get('text', '')[:50] + ('...' if len(item.get('text', '')) > 50 else ''),
            'from_id': item.get('from_id'),
            'date': datetime.fromtimestamp(item.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S'),
            'likes': item.get('likes', 0)
        } for item in items]
    
    def get_detailed_report(self, num_posts: int = 10) -> Dict:
        """Получает детальный отчет по последним постам"""
        posts = self.get_posts(count=num_posts)
        
        posts_stats = []
        for post in posts:
            post_stat = self.get_post_stats(post.get('id'))
            posts_stats.append(post_stat)
        
        # Подсчитываем агрегированные метрики
        total_likes = sum(p.get('likes', 0) for p in posts_stats)
        total_comments = sum(p.get('comments', 0) for p in posts_stats)
        total_reposts = sum(p.get('reposts', 0) for p in posts_stats)
        total_views = sum(p.get('views', 0) for p in posts_stats)
        
        avg_likes = total_likes / len(posts_stats) if posts_stats else 0
        avg_comments = total_comments / len(posts_stats) if posts_stats else 0
        avg_views = total_views / len(posts_stats) if posts_stats else 0
        
        return {
            'summary': {
                'total_posts_analyzed': len(posts_stats),
                'total_likes': total_likes,
                'total_comments': total_comments,
                'total_reposts': total_reposts,
                'total_views': total_views,
                'avg_likes_per_post': round(avg_likes, 2),
                'avg_comments_per_post': round(avg_comments, 2),
                'avg_views_per_post': round(avg_views, 2),
                'engagement_rate': round((total_likes + total_comments + total_reposts) / total_views * 100, 2) if total_views > 0 else 0
            },
            'posts': posts_stats,
            'group_info': {
                'subscribers': self.get_followers_count()
            }
        }