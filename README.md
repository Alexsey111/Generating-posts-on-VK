# Проект для работы с социальными сетями

Проект для автоматической генерации и публикации контента в социальных сетях (в частности, ВКонтакте). Включает генерацию контента с помощью OpenAI, автоматическую публикацию в ВКонтакте и детальную аналитику.

## 🚀 Возможности

- **Генерация контента**: Создание текстов для постов с помощью OpenAI GPT-4 и изображений через DALL-E 3
- **Автоматическая публикация**: Публикация в группах ВКонтакте с поддержкой изображений
- **Аналитика и статистика**: Детальный анализ эффективности постов, вовлеченности аудитории
- **Визуализация данных**: Генерация отчетов в CSV и HTML формате
- **Высокое качество кода**: Полное покрытие тестами, типизация, линтинг

## 📦 Установка

### Базовый вариант
1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе примера:
```bash
cp .env.example .env
```

4. Отредактируйте `.env` и укажите ваши API ключи:
```env
OPENAI_API_KEY=ваш-openai-api-ключ
VK_API_KEY=ваш-vk-api-ключ
VK_GROUP_ID=ID-вашей-группы
```

### Разработка
```bash
# Установка с зависимостями для разработки
make install-dev

# Настройка окружения разработки
make dev-setup
```

## 🧪 Тестирование

Проект включает полное покрытие тестами основного функционала:

```bash
# Запуск всех тестов
make test

# Тесты с покрытием
make test-cov

# Запуск конкретного тестового файла
pytest tests/test_generators.py -v
```

**Покрытие тестами:**
- `test_generators.py` - тесты генераторов текста и изображений
- `test_publishers.py` - тесты публикации в ВКонтакте  
- `test_statistics.py` - тесты аналитики и статистики

## 🛠️ Команды разработки

```bash
# Форматирование кода
make format

# Проверка кода линтером
make lint

# Проверка типов
make type-check

# Полная проверка качества кода
make ci

# Очистка временных файлов
make clean

# Запуск примера
make run
```

## 📖 Использование

### Базовый пример (test.py)

```python
from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
import config as conf

# Создание генератора постов
post_gen = PostGenerator(
    conf.openai_key,
    tone="позитивный и весёлый",
    topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
)

# Генерация текста и описания изображения
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

# Генерация изображения
img_gen = ImageGenerator(conf.openai_key)
image_url = img_gen.generate_image(img_desc)

print("=== СГЕНЕРИРОВАННЫЙ ПОСТ ===")
print(content)
print("\n=== URL ИЗОБРАЖЕНИЯ ===")
print(image_url)
```

### Публикация в ВКонтакте

```python
from social_publishers.vk_publisher import VKPublisher
import config as conf

publisher = VKPublisher(conf.vk_api_key, conf.vk_group_id)
result = publisher.publish_post("Текст поста", image_url="https://example.com/image.jpg")
```

### Получение статистики и аналитика

```python
from social_stats.vk_stats import VKStats
from social_stats.statistics_visualizer import StatisticsVisualizer
import config as conf

stats = VKStats(conf.vk_api_key, conf.vk_group_id)
visualizer = StatisticsVisualizer()

# Получение статистики постов
posts_analytics = stats.get_posts_analytics(count=10)

# Генерация отчета
report_data = stats.generate_report(days=30)
visualizer.generate_csv_report(posts_analytics, 'analytics_report.csv')
visualizer.generate_dashboard(report_data, 'dashboard.html')
```

## 📁 Структура проекта

```
├── config.py                 # Конфигурация и валидация
├── requirements.txt          # Основные зависимости
├── requirements-dev.txt      # Зависимости разработки
├── .env.example             # Пример переменных окружения
├── .gitignore               # Исключения Git
├── Makefile                 # Команды разработки
├── pytest.ini              # Конфигурация тестов
├── pyproject.toml           # Конфигурация Black
├── .flake8                  # Конфигурация линтера
├── mypy.ini                 # Конфигурация типизации
│
├── generators/              # Генерация контента
│   ├── __init__.py
│   ├── text_gen.py          # Генерация текста постов
│   └── image_gen.py         # Генерация изображений
│
├── social_publishers/       # Публикация контента
│   ├── __init__.py
│   └── vk_publisher.py      # Публикация в ВКонтакте
│
├── social_stats/           # Аналитика и статистика
│   ├── __init__.py
│   ├── vk_stats.py         # Основная статистика ВК
│   ├── post_statistics.py  # Детальная статистика постов
│   ├── statistics_visualizer.py  # Визуализация данных
│   └── statistics_example.py     # Примеры использования
│
├── tests/                  # Тестирование
│   ├── __init__.py
│   ├── conftest.py         # Фикстуры для тестов
│   ├── test_generators.py  # Тесты генераторов
│   ├── test_publishers.py  # Тесты публикации
│   └── test_statistics.py  # Тесты статистики
│
└── test.py                # Пример использования
```

## 📋 Зависимости

### Основные
- **openai** (>=1.0.0) - GPT-4 и DALL-E 3 API
- **python-dotenv** (>=0.19.0) - Переменные окружения
- **requests** (>=2.25.0) - HTTP клиент
- **pandas** (>=2.0.0) - Обработка данных
- **matplotlib** (>=3.7.0) - Визуализация
- **seaborn** (>=0.12.0) - Статистическая визуализация
- **loguru** (>=0.7.0) - Логирование
- **tqdm** (>=4.65.0) - Прогресс-бары

### Разработка
- **pytest** (>=7.0.0) - Фреймворк тестирования
- **pytest-cov** (>=4.0.0) - Покрытие тестами
- **black** (>=23.0.0) - Форматирование кода
- **flake8** (>=6.0.0) - Линтинг
- **mypy** (>=1.0.0) - Проверка типов

## 🔑 Требования к API

### OpenAI API
- API ключ с доступом к GPT-4 и DALL-E 3
- Тарификация согласно тарифам OpenAI
- Рекомендуемый лимит: 1000 запросов/месяц для тестирования

### VK API
- API ключ с правами для работы с группами
- ID группы для публикации и получения статистики
- Необходимые права: `groups`, `wall`, `photos`, `stats`

## 🔒 Безопасность

⚠️ **Важно**: 
- Никогда не коммитьте файл `.env` в репозиторий
- Все API ключи должны храниться в переменных окружения
- Регулярно обновляйте зависимости для безопасности
- Используйте отдельные API ключи для разработки и продакшена

## 📈 Мониторинг качества кода

Проект использует современные практики контроля качества:

```bash
# Проверка всех аспектов качества
make ci

# Отчет о покрытии тестами
make test-cov
# Отчет будет сохранен в htmlcov/index.html
```

## 🚀 Быстрый старт

```bash
# 1. Клонирование и установка
git clone <repository-url>
cd <project-directory>
make install-dev

# 2. Настройка окружения
make dev-setup
# Отредактируйте .env файл

# 3. Проверка работоспособности
make test
make run

# 4. Полная проверка качества
make ci
```

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.