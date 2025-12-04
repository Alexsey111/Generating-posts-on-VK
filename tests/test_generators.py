import pytest
import os
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator


class TestPostGenerator:
    """Тесты для PostGenerator"""
    
    def test_init(self):
        """Тест инициализации PostGenerator"""
        with patch('generators.text_gen.openai.OpenAI') as mock_openai:
            generator = PostGenerator("fake_key", "test_tone", "test_topic")
            assert generator.openai_key == "fake_key"
            assert generator.tone == "test_tone"
            assert generator.topic == "test_topic"
    
    def test_generate_post(self):
        """Тест генерации поста"""
        with patch('generators.text_gen.openai.OpenAI') as mock_openai:
            # Mock the OpenAI response
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="Тестовый пост"))
            ]
            
            generator = PostGenerator("fake_key", "test_tone", "test_topic")
            result = generator.generate_post()
            
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_generate_post_image_description(self):
        """Тест генерации описания изображения"""
        with patch('generators.text_gen.openai.OpenAI') as mock_openai:
            # Mock the OpenAI response
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="Описание изображения"))
            ]
            
            generator = PostGenerator("fake_key", "test_tone", "test_topic")
            result = generator.generate_post_image_description()
            
            assert isinstance(result, str)
            assert len(result) > 0


class TestImageGenerator:
    """Тесты для ImageGenerator"""
    
    def test_init(self):
        """Тест инициализации ImageGenerator"""
        with patch('generators.image_gen.openai.OpenAI') as mock_openai:
            generator = ImageGenerator("fake_key")
            assert generator.openai_key == "fake_key"
    
    def test_generate_image(self):
        """Тест генерации изображения"""
        with patch('generators.image_gen.openai.OpenAI') as mock_openai:
            # Mock the OpenAI response
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_client.images.generate.return_value.data = [
                MagicMock(url="https://example.com/test-image.png")
            ]
            
            generator = ImageGenerator("fake_key")
            result = generator.generate_image("test prompt")
            
            assert isinstance(result, str)
            assert result.startswith("https://")