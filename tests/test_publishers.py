import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from social_publishers.vk_publisher import VKPublisher


class TestVKPublisher:
    """Тесты для VKPublisher"""
    
    def test_init(self):
        """Тест инициализации VKPublisher"""
        publisher = VKPublisher("fake_api_key", 123456)
        assert publisher.vk_api_key == "fake_api_key"
        assert publisher.group_id == 123456
    
    def test_upload_photo(self):
        """Тест загрузки фотографии"""
        with patch('social_publishers.vk_publisher.requests.post') as mock_post:
            # Mock VK API response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'response': {
                    'upload_url': 'https://example.com/upload',
                    'photo': '{"photo":"test"}'
                }
            }
            mock_post.return_value = mock_response
            
            publisher = VKPublisher("fake_api_key", 123456)
            result = publisher.upload_photo("https://example.com/image.jpg")
            
            assert result is not None
            mock_post.assert_called()
    
    def test_publish_post(self):
        """Тест публикации поста"""
        with patch('social_publishers.vk_publisher.requests.post') as mock_post:
            # Mock VK API response
            mock_response = MagicMock()
            mock_response.json.return_value = {'response': {'post_id': 12345}}
            mock_post.return_value = mock_response
            
            publisher = VKPublisher("fake_api_key", 123456)
            result = publisher.publish_post("Test post content")
            
            assert result is not None
            mock_post.assert_called()