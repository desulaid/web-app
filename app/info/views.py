from flask import Blueprint, url_for

info = Blueprint('info', __name__, template_folder='templates')


@info.route('/info', methods=['GET'])
@info.route('/', methods=['GET'])
def index():
    url = url_for('dashboard.group')

    return f'<a href="{url}">Перейти, пока что</a>'
