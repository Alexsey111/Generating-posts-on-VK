import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from social_stats.vk_stats import VKStats
from social_stats.post_statistics import PostStatistics


class TestVKStats:
    """Тесты для VKStats"""
    
    def test_init(self):
        """Тест инициализации VKStats"""
        stats = VKStats("fake_api_key", 123456)
        assert stats.vk_api_key == "fake_api_key"
        assert stats.group_id == 123456
    
    def test_get_followers(self):
        """Тест получения количества подписчиков"""
        with patch('social_stats.vk_stats.requests.get') as mock_get:
            # Mock VK API response
            mock_response = MagicMock()
            mock_response.json.return_value = {'response': {'count': 1000, 'items': []}}
            mock_get.return_value = mock_response
            
            stats = VKStats("fake_api_key", 123456)
            result = stats.get_followers()
            
            assert isinstance(result, int)
            assert result == 1000
    
    def test_get_posts(self):
        """Тест получения постов"""
        with patch('social_stats.vk_stats.requests.get') as mock_get:
            # Mock VK API response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'response': {
                    'count': 10,
                    'items': [{'id': 1, 'text': 'Test post'}]
                }
            }
            mock_get.return_value = mock_response
            
            stats = VKStats("fake_api_key", 123456)
            result = stats.get_posts(count=5)
            
            assert isinstance(result, list)
            assert len(result) == 1
    
    def test_calculate_engagement(self):
        """Тест расчета вовлеченности"""
        stats = VKStats("fake_api_key", 123456)
        engagement = stats._calculate_engagement(likes=10, views=100)
        
        assert isinstance(engagement, float)
        assert engagement == 10.0  # (10/100) * 100


class TestPostStatistics:
    """Тесты для PostStatistics"""
    
    def test_init(self):
        """Тест инициализации PostStatistics"""
        post_stats = PostStatistics("fake_api_key", 123456)
        assert post_stats.vk_api_key == "fake_api_key"
        assert post_stats.group_id == 123456
    
    def test_get_post_stats(self):
        """Тест получения статистики поста"""
        with patch('social_stats.post_statistics.requests.get') as mock_get:
            # Mock VK API response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'response': [{
                    'id': 123,
                    'likes': {'count': 15},
                    'views': {'count': 200}
                }]
            }
            mock_get.return_value = mock_response
            
            post_stats = PostStatistics("fake_api_key", 123456)
            result = post_stats.get_post_stats(123)
            
            assert result is not None
            assert 'likes' in result
            assert 'views' in result