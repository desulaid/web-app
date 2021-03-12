from json import dumps

from flask import Blueprint, render_template, request, url_for, flash
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


@dashboard.route('/group', methods=['GET'])
@login_required
def group():
    user_group = Group.query.filter_by(user_id=current_user.id).first()
    group_exist = False
    if user_group:
        group_exist = True
    group_students = Student.query.filter_by(group_id=user_group.id).all()
    form_values = [item.name for item in group_students]

    context = dict(group_exist=group_exist, data=dumps(form_values))

    return render_template('dashboard/group.html', **context)


@dashboard.route('/group-add-items', methods=['POST'])
@login_required
def add_items():
    user_group = Group.query.filter_by(user_id=current_user.id).first()

    if not user_group:
        Group(user_id=current_user.id)
        db.session.add(id)
        db.session.commit()

        flash('Ваша группа создана.', 'success')
    else:
        Student.query.delete()
        for key in request.form:
            if request.form[key]:
                db.session.add(Student(name=request.form[key], group_id=user_group.id))

        db.session.commit()

        flash('Информация о студентах обновлена.', 'warning')
    return redirect(url_for('.group'))

