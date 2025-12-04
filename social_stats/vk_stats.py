import requests
import datetime
import json


class VKStats:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def get_group_info(self):
        """Получает базовую информацию о группе"""
        url = 'https://api.vk.com/method/groups.getById'
        
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_ids': self.group_id,
            'fields': 'members_count,description,activity,cover'
        }
        
        response = requests.get(url, params=params).json()
        
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            return response['response'][0]

    def get_stats(self, start_date, end_date):
        """Получает детальную статистику группы за период"""
        url = 'https://api.vk.com/method/stats.get'
        
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        end_date = end_date.replace(tzinfo=datetime.timezone.utc)
        
        start_unix_time = int(start_date.timestamp())
        end_unix_time = int(end_date.timestamp())
        
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id,
            'timestamp_from': start_unix_time,
            'timestamp_to': end_unix_time
        }
        
        response = requests.get(url, params=params).json()
        
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            return response['response']

    def get_followers(self):
        """Получает количество подписчиков"""
        url = 'https://api.vk.com/method/groups.getMembers'
        
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id
        }
        
        response = requests.get(url, params=params).json()
        
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            return response['response']['count']

    def get_posts(self, count=20, offset=0):
        """Получает последние посты группы"""
        url = 'https://api.vk.com/method/wall.get'
        
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'owner_id': f'-{self.group_id}',
            'count': count,
            'offset': offset
        }
        
        response = requests.get(url, params=params).json()
        
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            return response['response']['items']

    def get_post_stats(self, post_id):
        """Получает статистику конкретного поста"""
        url = 'https://api.vk.com/method/likes.getList'
        
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'type': 'post',
            'owner_id': f'-{self.group_id}',
            'item_id': post_id
        }
        
        likes_response = requests.get(url, params=params).json()
        
        # Получаем информацию о просмотрах через stats.get
        stats_params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id,
            'post_id': post_id
        }
        
        views_response = requests.get('https://api.vk.com/method/stats.getPostReach', 
                                    params=stats_params).json()
        
        return {
            'post_id': post_id,
            'likes': likes_response.get('response', {}).get('count', 0),
            'views': views_response.get('response', {}).get('views', 0)
        }

    def get_posts_analytics(self, count=10):
        """Получает аналитику последних постов"""
        posts = self.get_posts(count)
        analytics = []
        
        for post in posts:
            post_id = post['id']
            stats = self.get_post_stats(post_id)
            
            post_analytics = {
                'post_id': post_id,
                'date': datetime.datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M'),
                'text': post['text'][:100] + '...' if len(post['text']) > 100 else post['text'],
                'likes': stats['likes'],
                'views': stats['views'],
                'comments': post.get('comments', {}).get('count', 0),
                'reposts': post.get('reposts', {}).get('count', 0),
                'engagement_rate': self._calculate_engagement(stats['likes'], stats['views'])
            }
            analytics.append(post_analytics)
        
        return analytics

    def _calculate_engagement(self, likes, views):
        """Вычисляет коэффициент вовлеченности"""
        if views == 0:
            return 0
        return round((likes / views) * 100, 2)

    def generate_report(self, days=30):
        """Генерирует полный отчет по группе"""
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Базовая информация о группе
        group_info = self.get_group_info()
        followers = self.get_followers()
        
        # Статистика за период
        period_stats = self.get_stats(start_date.isoformat(), end_date.isoformat())
        
        # Аналитика постов
        posts_analytics = self.get_posts_analytics(20)
        
        # Сводная статистика
        total_likes = sum(post['likes'] for post in posts_analytics)
        total_views = sum(post['views'] for post in posts_analytics)
        total_comments = sum(post['comments'] for post in posts_analytics)
        total_reposts = sum(post['reposts'] for post in posts_analytics)
        
        avg_engagement = sum(post['engagement_rate'] for post in posts_analytics) / len(posts_analytics) if posts_analytics else 0
        
        report = {
            'period': f"{start_date} - {end_date}",
            'group_info': {
                'name': group_info['name'],
                'description': group_info.get('description', ''),
                'members_count': followers
            },
            'summary': {
                'total_posts': len(posts_analytics),
                'total_likes': total_likes,
                'total_views': total_views,
                'total_comments': total_comments,
                'total_reposts': total_reposts,
                'avg_engagement_rate': round(avg_engagement, 2)
            },
            'posts_analytics': posts_analytics,
            'period_stats': period_stats
        }
        
        return report
