from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.users.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField(
        label='نام',
        validators=[
            DataRequired(),
            Length(min=2, max=30, message='نام باید بین حداقل 3 و حداکثر 30 کاراکتر باشد!')
        ],
        render_kw={
            "placeholder": "نام خود را وارد کنید ..."
        }
    )
    last_name = StringField(
        label='نام خانوادگی',
        validators=[
            DataRequired(),
            Length(min=2, max=30, message='نام خانوادگی باید بین حداقل 3 و حداکثر 30 کاراکتر باشد!')
        ],
        render_kw={
            "placeholder": "نام خانوادگی خود را وارد کنید ..."
        }
    )
    username = StringField(
        label='نام کاربری',
        validators=[
            DataRequired(),
            Length(min=4, max=30, message='نام کاربری باید بین حداقل 4 و حداکثر 30 کاراکتر باشد!')
        ],
        render_kw={
            "placeholder": "نام کاربری خود را وارد کنید ..."
        }
    )
    phone = StringField(
        label='شماره تلفن همراه',
        validators=[
            DataRequired(),
            Length(min=11, max=11, message='شماره تلفن همراه باید 11 رقم باشد!')
        ],
        render_kw={
            "placeholder": "شماره تلفن همراه خود را وارد کنید ..."
        }
    )
    password = PasswordField(
        label='گذرواژه',
        validators=[
            DataRequired(),
            Length(min=8, max=30, message='گذرواژه باید بین حداقل 8 و حداکثر 30 کاراکتر باشد!')
        ],
        render_kw={
            "placeholder": "گذرواژه خود را وارد کنید ..."
        }
    )
    confirm_password = PasswordField(
        label='تایید گذرواژه',
        validators=[
            DataRequired(),
            EqualTo('password', message='گذرواژه باید یکسان باشد!')
        ],
        render_kw={
            "placeholder": "گذرواژه خود را دوباره وارد کنید ..."
        }
    )
    role = SelectField(
        label='نقش',
        validators=[
            DataRequired(),
        ],
        choices=[
            ("کاربر عادی", "کاربر عادی"),
            ("مدیر سیستم", "مدیر سیستم"),
        ]
    )
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('کاربری با این نام کاربری وجود دارد!')
    
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('کاربری با این شماره تلفن وجود دارد!')
        


class LoginForm(FlaskForm):
	username = StringField(
        label='نام کاربری',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "نام کاربری خود را وارد کنید ..."
        }
    )
	password = PasswordField(
        label='گذرواژه',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "گذرواژه خود را وارد کنید ..."
        }
    )
	remember = BooleanField(
        label='مرا بخاطر بسپار'
    )
    