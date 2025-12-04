import os
from dotenv import load_dotenv

load_dotenv()

# Open AI
openai_key = os.getenv("OPENAI_API_KEY", "your-key-here")

# VK
vk_api_key = os.getenv("VK_API_KEY", "your-key-here")
vk_group_id = int(os.getenv("VK_GROUP_ID", "226084011"))

# Проверка наличия необходимых API ключей
def validate_config():
    """Проверяет наличие всех необходимых API ключей"""
    errors = []
    
    if openai_key == "your-key-here" or not openai_key:
        errors.append("OPENAI_API_KEY не установлен или недействителен")
    
    if vk_api_key == "your-key-here" or not vk_api_key:
        errors.append("VK_API_KEY не установлен или недействителен")
    
    if errors:
        raise ValueError("Ошибки конфигурации:\n" + "\n".join(f"- {error}" for error in errors))
    
    return True

# Автоматическая проверка конфигурации при импорте
try:
    validate_config()
except ValueError as e:
    print(f"⚠️  {e}")
    print("Убедитесь, что в файле .env указаны правильные API ключи")