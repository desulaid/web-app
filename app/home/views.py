from flask import Blueprint, render_template, request
from flask_login import current_user as user

from app.database import Group

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/home', methods=['GET', 'POST'])
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass

    groups = Group.query.all()

    context = dict(
        title='Статистика',
        header='Посещаемые занятия!',
        user=user,
        groups=groups
    )

    return render_template('home/index.html', **context)


@home.route('/home/<string:name>/<int:id>', methods=['GET'])
def student_info(name: str):
    return f'{request.form}'


@home.route('/faq', methods=['GET'])
def faq():
    context = dict(
        title='Статистика',
        header='Посещаемые занятия!',
    )

    return render_template('home/faq.html', **context)
