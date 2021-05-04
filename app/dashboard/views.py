from calendar import monthrange
from json import dumps

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

from app.database import db, Profile, Group, Teacher, Student

dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates')


@dashboard.route('/', methods=['GET'])
def index():
    form = ManageForm()
    students = Profile.query.filter_by().all()
    context = dict(
        title='Главная страница',
        header='Глвная',
        data=dumps([]),
        form=form,
        monthrange=monthrange(2020, 4)
    )

    return render_template('dashboard/index.html', **context)


@dashboard.route('/group', methods=['GET'])
def group():
    students = Student.query.filter_by(master_id=current_user.id).all()

    context = dict(
        title='Студенты моей группы',
        header='Моя группа',
        data=dumps([i.name for i in students]),
        current_user=current_user,
    )

    return render_template('dashboard/group.html', **context)


@dashboard.route('/group/<id>', methods=['POST'])
def group_save(id):
    Student.query.delete()

    for key in request.form:
        if request.form[key]:
            db.session.add(Student(name=request.form[key], master_id=current_user.id))

    db.session.commit()

    return redirect(url_for('.group'))


@dashboard.route('/settings', methods=['GET'])
def settings():
    groups = Group.query.all()
    teachers = Teacher.query.all()

    context = dict(
        title='Настройки профиля',
        header='Настройки',
        current_user=current_user,
        groups=groups,
        teachers=teachers
    )

    return render_template('dashboard/settings.html', **context)


@dashboard.route('/profile/update/<login>/prof', methods=['POST'])
def update_profile_prof(login):
    profile = Profile.query.filter_by(login=login).first()

    error = None
    group_id = request.form['group-id']
    group_teacher_id = request.form['group-teacher']
    group_name = Group.query.get(group_id)

    if db.session.query(
            Profile.query.filter_by(group_id=group_id,
                                    teacher_id=group_teacher_id).exists()
    ).scalar():
        error = f'Староста группы {group_name.name} уже назначен'

    if error is None:
        profile.group_id = group_id
        profile.teacher_id = group_teacher_id
        db.session.commit()
    else:
        flash(error, 'warning')

    return redirect(url_for('.settings'))


@dashboard.route('/profile/update/<login>/main', methods=['POST'])
def update_profile_main(login):
    profile = Profile.query.filter_by(login=login).first()

    error = None
    name = request.form['name']
    login = request.form['login']
    password = request.form['password']
    password_confirm = request.form['password-confirm']

    if db.session.query(
            Profile.query.filter_by(login=login).exists()
    ).scalar():
        error = 'Логин уже занят'
    elif password != password_confirm:
        error = 'Пароли не совпадают'

    if error is None:
        profile.name = name
        profile.login = login
        profile.password = password
        db.session.commit()
    else:
        flash(error, 'warning')

    return redirect(url_for('.settings'))


@dashboard.route('/verify', methods=['GET'])
def verify():
    profiles = Profile.query.filter_by(verify=False).all()

    context = dict(
        title='Подтверждение профилей',
        header='Верфикация',
        profiles=profiles
    )

    return render_template('dashboard/verify.html', **context)


@dashboard.route('/verifying/<login>', methods=['POST'])
def verifying(login):
    status = True if request.form['status'] == 'yes' else False

    profile = Profile.query.filter_by(login=login).first()

    if status:
        profile.verify = True
        db.session.commit()

        flash(f'Аккаунт {login} подтвержен', 'success')
    else:
        db.session.delete(profile)
        db.session.commit()

        flash(f'Аккаунт {login} удален', 'warning')

    return redirect(url_for('.verify'))


@dashboard.route('/add', methods=['GET'])
def add():
    context = dict(
        title='Добавить новую запись',
        header='Новая запись',
        data=dumps([])
    )
    return render_template('dashboard/add.html', **context)
