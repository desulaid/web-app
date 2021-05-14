from flask import Blueprint, render_template, request
from flask_login import current_user as user

from app.database import Group

info = Blueprint('info', __name__, template_folder='templates')


@info.route('/info', methods=['GET', 'POST'])
@info.route('/', methods=['GET', 'POST'])
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

    return render_template('info/index.html', **context)


@info.route('/info/<string:name>/<int:id>', methods=['GET'])
def student_info(name: str):
    return f'{request.form}'


@info.route('/faq', methods=['GET'])
def faq():
    context = dict(
        title='Статистика',
        header='Посещаемые занятия!',
    )

    return render_template('info/faq.html', **context)
