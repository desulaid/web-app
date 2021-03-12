from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(),
                                   Length(1, 64),
                                   Email()], 
                       render_kw={"placeholder": "Электронная почта"})
    password = PasswordField(validators=[InputRequired()], 
                             render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти в аккаунт')


class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(),
                                   Length(min=10, 
                                          message='Имя должно быть больше 10 символов')],
                       render_kw={"placeholder": "Имя"})
    email = EmailField(validators=[InputRequired(),
                                   Email(message='Некорректный формат электронной почты')],
                       render_kw={"placeholder": "Электронная почта"})
    password = PasswordField(validators=[InputRequired()], 
                             render_kw={"placeholder": "Пароль"})
    confirm = PasswordField(validators=[InputRequired(),
                                        EqualTo('password', 
                                                message='Пароли должны совпадать')],
                            render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрировать в аккаунт')
