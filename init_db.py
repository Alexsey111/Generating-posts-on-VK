#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных Flask приложения
Запускается один раз после установки зависимостей
"""

import os
import sys
from app import app, db
from models import User

def init_database():
    """Инициализация базы данных"""
    print("Initializing database...")
    
    with app.app_context():
        try:
            # Создаем все таблицы
            db.create_all()
            print("Database tables created successfully")
            
            # Проверяем, есть ли уже пользователи
            user_count = User.query.count()
            print(f"Number of users in database: {user_count}")
            
            print("\nDatabase is ready to use!")
            print("To start the application run: python app.py")
            
        except Exception as e:
            print(f"Error during database initialization: {e}")
            return False
    
    return True

def check_dependencies():
    """Проверка зависимостей"""
    print("Checking dependencies...")
    
    required_packages = [
        'flask', 'flask_login', 'flask_wtf', 
        'flask_sqlalchemy', 'openai', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"[OK] {package}")
        except ImportError:
            print(f"[MISSING] {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("\nAll dependencies are installed")
    return True

def check_env_file():
    """Проверка файла .env"""
    print("\nChecking .env file...")
    
    if not os.path.exists('.env'):
        print("[ERROR] .env file not found")
        print("Create it from example:")
        print("   cp .env.example .env")
        return False
    
    # Проверяем ключевые переменные
    with open('.env', 'r') as f:
        content = f.read()
        
    required_vars = ['OPENAI_API_KEY', 'VK_API_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if f"{var}=" not in content or f"{var}=your-" in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"[ERROR] Missing or unconfigured variables: {', '.join(missing_vars)}")
        print("Edit .env file and specify correct values")
        return False
    
    print("[OK] .env file configured correctly")
    return True

def main():
    """Основная функция"""
    print("=" * 50)
    print("VK Post Generator - Initialization")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        print("\nInstall missing dependencies and try again")
        sys.exit(1)
    
    # Проверяем файл .env
    if not check_env_file():
        print("\nConfigure .env file and try again")
        sys.exit(1)
    
    # Инициализируем базу данных
    if not init_database():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Initialization completed successfully!")
    print("=" * 50)
    print("\nTo start the application:")
    print("   python app.py")
    print("\nThen open your browser and go to:")
    print("   http://localhost:5000")

if __name__ == '__main__':
    main()