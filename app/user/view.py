from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user

from app.database import db
from app.database.models import Profile
from .forms import LoginForm, RegisterForm
from .login_manager import UserLogin

user = Blueprint('user', __name__,
                 template_folder='templates',
                 url_prefix='/auth')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        error = None
        login = form.login.data
        password = form.password.data
        account = UserLogin.query.filter_by(login=login).first()

        if account is None or not account.check_password(password):
            error = 'Неправильная почта или пароль.'

        if not account.verify:
            error = 'Ваш аккаунт не подтвержден. Ожидайте.'

        if error is None:
            login_user(account, remember=True)
            return redirect(url_for('dashboard.index'))

        flash(error, 'warning')

    context = dict(
        title='Вход в учетную запись',
        header='Авторизация',
        form=form
    )

    return render_template('user/login.html', **context)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        error = None
        name = form.name.data
        login = form.login.data
        password = form.password.data

        if db.session.query(
                Profile.query.filter_by(login=login).exists()
        ).scalar():
            error = f"Аккаунт {login} уже зарегистрирован в системе."

        if error is None:
            db.session.add(Profile(
                name=name,
                login=login,
                password=password,
                verify=False
            ))
            db.session.commit()

            return redirect(url_for('.login'))

        flash(error, 'warning')

    context = dict(
        title='Регистрация учетной записи',
        header='Регистрация',
        form=form
    )

    return render_template('user/register.html', **context)


@user.route('/logout', methods=['GET'])
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return render_template('user/redirect.html')
