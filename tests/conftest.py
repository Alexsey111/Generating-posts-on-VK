import pytest
import os
from unittest.mock import patch
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_env_vars():
    """Фикстура для мокирования переменных окружения"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'VK_API_KEY': 'test_vk_key',
        'VK_GROUP_ID': '123456'
    }):
        yield

@pytest.fixture
def mock_openai_client():
    """Фикстура для мокирования OpenAI клиента"""
    with patch('openai.OpenAI') as mock_client:
        mock_instance = mock_client.return_value
        # Настраиваем базовые моки для всех методов
        mock_instance.chat.completions.create.return_value.choices = [
            type('obj', (object,), {'message': type('obj', (object,), {'content': 'Test content'})()})()
        ]
        mock_instance.images.generate.return_value.data = [
            type('obj', (object,), {'url': 'https://example.com/test-image.png'})()
        ]
        yield mock_instance

@pytest.fixture
def mock_vk_api():
    """Фикстура для мокирования VK API"""
    with patch('requests.get') as mock_get, patch('requests.post') as mock_post:
        # Мок для GET запросов
        mock_get.return_value.json.return_value = {
            'response': {
                'count': 100,
                'items': [{'id': 1, 'text': 'Test post'}]
            }
        }
        
        # Мок для POST запросов
        mock_post.return_value.json.return_value = {'response': {'post_id': 12345}}
        
        yield {'get': mock_get, 'post': mock_post}

@pytest.fixture
def sample_post_data():
    """Фикстура с примерными данными поста"""
    return {
        'id': 123,
        'text': 'Test post content',
        'date': 1640995200,
        'likes': {'count': 25},
        'views': {'count': 500},
        'comments': {'count': 10}
    }