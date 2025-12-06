#!/usr/bin/env python3
"""
Файл для запуска Flask приложения в продакшене
Используйте WSGI серверы как Gunicorn или uWSGI
"""

import os
from app import app

# Настройки для продакшена
if __name__ == "__main__":
    # Получаем порт из переменных окружения или используем по умолчанию
    port = int(os.environ.get('PORT', 5000))
    
    # Настройки для продакшена
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # В продакшене всегда False
        threaded=True
    )