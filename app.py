import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from config import openai_key, vk_api_key, vk_group_id, validate_config
from models import db, User, GeneratedPost
from forms import RegistrationForm, LoginForm, PostGenerationForm
from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher

# Создание Flask приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверяем, существует ли пользователь с таким email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('register.html', form=form)
        
        # Создаем нового пользователя
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Успешный вход в систему!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('login.html', form=form)

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Панель управления
@app.route('/dashboard')
@login_required
def dashboard():
    user_posts = GeneratedPost.query.filter_by(user_id=current_user.id).order_by(GeneratedPost.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', posts=user_posts)

# Генерация поста
@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    form = PostGenerationForm()
    
    if form.validate_on_submit():
        try:
            # Проверяем конфигурацию
            validate_config()
            
            # Создаем генераторы
            post_gen = PostGenerator(openai_key, form.tone.data, form.topic.data)
            image_gen = ImageGenerator(openai_key)
            
            # Генерируем пост
            post_content = post_gen.generate_post()
            
            # Генерируем описание для изображения
            image_description = post_gen.generate_post_image_description()
            
            # Генерируем изображение
            image_url = image_gen.generate_image(image_description)
            
            # Сохраняем в базу данных
            generated_post = GeneratedPost(
                user_id=current_user.id,
                topic=form.topic.data,
                tone=form.tone.data,
                content=post_content,
                image_description=image_description,
                image_url=image_url,
                published=False
            )
            db.session.add(generated_post)
            db.session.commit()
            
            flash('Пост и изображение успешно сгенерированы!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Ошибка при генерации: {str(e)}', 'error')
            return render_template('generate.html', form=form)
    
    return render_template('generate.html', form=form)

# Публикация поста
@app.route('/publish/<int:post_id>')
@login_required
def publish(post_id):
    post = GeneratedPost.query.filter_by(id=post_id, user_id=current_user.id).first()
    
    if not post:
        flash('Пост не найден', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Создаем публикатор
        publisher = VKPublisher(vk_api_key, vk_group_id)
        
        # Публикуем пост
        result = publisher.publish_post(post.content, post.image_url)
        
        if result:
            post.published = True
            post.published_at = datetime.utcnow()
            db.session.commit()
            flash('Пост успешно опубликован в ВКонтакте!', 'success')
        else:
            flash('Ошибка при публикации поста', 'error')
            
    except Exception as e:
        flash(f'Ошибка при публикации: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# API для получения истории постов
@app.route('/api/posts')
@login_required
def api_posts():
    posts = GeneratedPost.query.filter_by(user_id=current_user.id).order_by(GeneratedPost.created_at.desc()).all()
    
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'topic': post.topic,
            'tone': post.tone,
            'content': post.content[:100] + '...' if len(post.content) > 100 else post.content,
            'image_url': post.image_url,
            'published': post.published,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'published_at': post.published_at.strftime('%Y-%m-%d %H:%M:%S') if post.published_at else None
        })
    
    return jsonify(posts_data)

# Инициализация базы данных при первом запуске
def init_db():
    """Инициализация базы данных"""
    with app.app_context():
        db.create_all()

# Инициализация при импорте модуля
init_db()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)