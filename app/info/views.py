from flask import Blueprint, render_template, url_for
from flask_login import current_user as user


info = Blueprint('info', __name__, template_folder='templates')


@info.route('/info', methods=['GET'])
@info.route('/', methods=['GET'])
def index():

    context = dict(
        title='Статистика',
        header='Статистика по посещаемым занятиям',
        user=user
    )

    return render_template('info/index.html', **context)
