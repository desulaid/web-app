from json import dumps

from flask import Blueprint, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from app import db
from app.models import Group, Student

dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates')


@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('dashboard/index.html')


@dashboard.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    group = Group.query.filter_by(user_id=current_user.id).first()
    group_exist = False
    form_values = []
    if group:
        group_exist = True

    if request.method == 'POST':
        id = 0
        if not group:
            id = Group(user_id=current_user.id)
            db.session.add(id)
            db.session.commit()
        else:
            # id =
            pass

    context = dict(group_exist=group_exist, data=dumps(form_values))

    return render_template('dashboard/group.html', **context)
