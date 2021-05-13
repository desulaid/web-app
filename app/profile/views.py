from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user as user

from .forms import LoginForm, RegisterForm
from .login_manager import UserLogin
from app.database import db, Profile

profile = Blueprint('profile', __name__, template_folder='templates', url_prefix='/auth')


@profile.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        error = None
        login = form.login.data
        password = form.password.data
        account = UserLogin.query.filter_by(login=login).first()

        if not account:
            error = f'Аккаунт {login} не зарегистрирован в системе'
        else:
            if not account.verify:
                error = 'Ваш аккаунт не подтвержден. Ожидайте.'

            if not account.check_password(password):
                error = 'Неправильный пароль.'

            if not error:
                login_user(account, remember=True)
                return redirect(url_for('dashboard.settings'))

        flash(error, 'warning')

    context = dict(
        title='Авторизация существующего аккаунта',
        header='Авторизация',
        form=form
    )

    return render_template('profile/login.html', **context)


@profile.route('/register', methods=['GET', 'POST'])
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
        title='Регистрация существующего аккаунта',
        header='Регистрация',
        form=form
    )

    return render_template('profile/register.html', **context)


@profile.route('/logout', methods=['GET'])
@login_required
def logout():
    user.authenticated = False
    logout_user()

    return redirect(url_for('.login'))