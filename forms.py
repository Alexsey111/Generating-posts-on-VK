from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields import DateTimeLocalField

class RegistrationForm(FlaskForm):
    """Форма регистрации пользователя"""
    username = StringField('Имя пользователя', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=3, max=80, message='Имя пользователя должно содержать от 3 до 80 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Обязательное поле'),
        Email(message='Некорректный email адрес')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=6, message='Пароль должен содержать минимум 6 символов')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Обязательное поле'),
        EqualTo('password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    """Форма авторизации"""
    email = StringField('Email', validators=[
        DataRequired(message='Обязательное поле'),
        Email(message='Некорректный email адрес')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Обязательное поле')
    ])
    submit = SubmitField('Войти')

class PostGenerationForm(FlaskForm):
    """Форма генерации поста"""
    topic = StringField('Тема поста', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=3, max=200, message='Тема должна содержать от 3 до 200 символов')
    ])
    tone = SelectField('Тон поста', choices=[
        ('дружелюбный', 'Дружелюбный'),
        ('профессиональный', 'Профессиональный'),
        ('игривый', 'Игривый'),
        ('мотивационный', 'Мотивационный'),
        ('информативный', 'Информативный'),
        ('креативный', 'Креативный'),
        ('строгий', 'Строгий')
    ], validators=[DataRequired(message='Выберите тон поста')])
    submit = SubmitField('Сгенерировать пост')

class PostEditForm(FlaskForm):
    """Форма редактирования поста"""
    content = TextAreaField('Содержание поста', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=10, max=5000, message='Содержание должно содержать от 10 до 5000 символов')
    ])
    image_description = TextAreaField('Описание для изображения', validators=[
        Length(max=500, message='Описание не должно превышать 500 символов')
    ])
    submit = SubmitField('Сохранить изменения')

class VKSettingsForm(FlaskForm):
    """Форма настроек ВКонтакте"""
    vk_group_id = StringField('ID группы ВКонтакте', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=1, max=20, message='Некорректный ID группы')
    ])
    submit = SubmitField('Сохранить настройки')