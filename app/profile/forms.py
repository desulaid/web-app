from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length


class LoginForm(FlaskForm):
    login = StringField(validators=[InputRequired(),
                                    Length(1, 64)],
                        render_kw={"placeholder": "Логин"})
    password = PasswordField(validators=[InputRequired()],
                             render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти в аккаунт')


class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(),
                                   Length(min=10,
                                          message='Имя должно быть больше 10 символов')],
                       render_kw={"placeholder": "Имя"})
    login = StringField(validators=[InputRequired()],
                        render_kw={"placeholder": "Логин"})
    password = PasswordField(validators=[InputRequired()],
                             render_kw={"placeholder": "Пароль"})
    confirm = PasswordField(validators=[InputRequired(),
                                        EqualTo('password',
                                                message='Пароли должны совпадать')],
                            render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрировать в аккаунт')