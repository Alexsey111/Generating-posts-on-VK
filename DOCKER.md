# Запуск VK Post Generator в Docker

Этот файл содержит инструкции по запуску VK Post Generator в Docker контейнерах.

## 🐳 Быстрый запуск с Docker

### 1. Подготовка файла конфигурации
```bash
# Скопируйте пример файла конфигурации
cp .env.example .env

# Отредактируйте .env файл и укажите ваши API ключи:
# - OPENAI_API_KEY
# - VK_API_KEY  
# - VK_GROUP_ID
# - SECRET_KEY
```

### 2. Запуск с PostgreSQL
```bash
# Запуск всех сервисов (приложение + база данных)
docker-compose up -d

# Просмотр логов
docker-compose logs -f app
```

### 3. Инициализация базы данных
```bash
# Выполнение миграций (если необходимо)
docker-compose exec app python init_db.py
```

### 4. Открыть в браузере
Перейдите на: http://localhost:5000

## 🔧 Команды Docker

### Управление контейнерами
```bash
# Запуск в фоновом режиме
docker-compose up -d

# Остановка
docker-compose down

# Пересборка и запуск
docker-compose up -d --build

# Просмотр логов
docker-compose logs app
docker-compose logs db

# Подключение к контейнеру приложения
docker-compose exec app bash

# Подключение к базе данных
docker-compose exec db psql -U app -d vk_post_generator
```

### Только приложение (без базы данных)
```bash
# Сборка образа
docker build -t vk-post-generator .

# Запуск контейнера
docker run -p 5000:5000 --env-file .env vk-post-generator
```

## 🗄️ База данных

### PostgreSQL
- **Хост**: localhost
- **Порт**: 5432
- **База данных**: vk_post_generator
- **Пользователь**: app
- **Пароль**: password

### Подключение к базе данных
```bash
# Через docker-compose
docker-compose exec db psql -U app -d vk_post_generator

# Через внешний клиент
psql -h localhost -U app -d vk_post_generator
```

## 🌐 Продакшен с Nginx

### Запуск с Nginx (HTTPS)
```bash
# Запуск с профилем production
docker-compose --profile production up -d

# Для этого потребуется настроить:
# - nginx.conf
# - SSL сертификаты в папке ssl/
```

## 📁 Структура файлов для Docker

```
├── Dockerfile              # Образ приложения
├── docker-compose.yml      # Оркестрация сервисов
├── .dockerignore           # Исключения для сборки
├── .env                    # Переменные окружения
├── init.sql               # Инициализация БД (опционально)
└── nginx.conf             # Конфигурация Nginx (опционально)
```

## 🔒 Безопасность

### Рекомендации для продакшена:
1. **Измените пароли** в docker-compose.yml
2. **Используйте SSL** сертификаты
3. **Ограничьте доступ** к базе данных
4. **Регулярно обновляйте** образы
5. **Мониторьте логи** контейнеров

### Переменные окружения
```bash
# Обязательные переменные в .env
OPENAI_API_KEY=your-key
VK_API_KEY=your-key
VK_GROUP_ID=your-group-id
SECRET_KEY=secure-random-key

# Опциональные для продакшена
DATABASE_URL=postgresql://user:password@db:5432/dbname
FLASK_ENV=production
LOG_LEVEL=INFO
```

## 🐛 Устранение неполадок

### Проблемы с базой данных
```bash
# Проверка статуса PostgreSQL
docker-compose exec db pg_isready -U app

# Просмотр логов БД
docker-compose logs db

# Пересоздание БД
docker-compose down -v
docker-compose up -d
```

### Проблемы с приложением
```bash
# Пересборка образа
docker-compose up -d --build --force-recreate

# Просмотр подробных логов
docker-compose logs --tail=100 app
```

### Очистка
```bash
# Полная очистка (включая volumes)
docker-compose down -v --rmi all

# Очистка образов
docker rmi $(docker images -q)
```

## 📈 Мониторинг

### Просмотр ресурсов
```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats

# Размер образов
docker images
```

### Резервное копирование БД
```bash
# Создание дампа
docker-compose exec db pg_dump -U app vk_post_generator > backup.sql

# Восстановление из дампа
docker-compose exec -T db psql -U app vk_post_generator < backup.sql
```