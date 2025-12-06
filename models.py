from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    posts = db.relationship('GeneratedPost', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Устанавливает хеш пароля"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверяет пароль"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Преобразует объект в словарь"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class GeneratedPost(db.Model):
    """Модель сгенерированного поста"""
    __tablename__ = 'generated_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Данные поста
    topic = db.Column(db.String(200), nullable=False)
    tone = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    
    # Статус публикации
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    
    # Временные метки
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Преобразует объект в словарь"""
        return {
            'id': self.id,
            'topic': self.topic,
            'tone': self.tone,
            'content': self.content,
            'image_description': self.image_description,
            'image_url': self.image_url,
            'published': self.published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }