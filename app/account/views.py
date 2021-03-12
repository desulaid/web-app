from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, url_for, redirect, flash, request

from flask_login import login_required, logout_user, login_user, current_user


from app import db
from app.account.forms import LoginForm, RegisterForm
from app.models import User

account = Blueprint('account', __name__,
                    template_folder='templates',
                    url_prefix='/auth')


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        error = None

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            error = 'Неправильная почта или пароль.'

        if error is None:
            login_user(user, remember=True)

            next_to = request.args.get('next')
            if not is_safe_url(next_to):
                return redirect(url_for("dashboard.index"))

            return redirect(next_to or url_for('dashboard.index'))

        flash(error, 'warning')

    return render_template('account/login.html', form=form)


@account.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        error = None

        exist = User.query.filter_by(email=email).first()
        if exist:
            error = f"Почта {email} уже занята другим пользователем."

        if error is None:
            user = User(name=name,
                        email=email,
                        password=password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('.login'))

        flash(error, 'warning')

    return render_template('account/register.html', form=form)


@account.route('/logout', methods=['GET', 'POST'])
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return render_template('account/redirect.html')


def is_safe_url(target):
    """Загулил в Яндексе"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc