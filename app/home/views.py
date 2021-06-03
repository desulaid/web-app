from flask import Blueprint, render_template, request, flash
from flask_login import current_user as user

from app.database import Group, Profile, Task, Student

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/home', methods=['GET'])
@home.route('/', methods=['GET'])
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


@home.route('/home/stat', methods=['POST'])
def statistic():
    group_id = request.form['group']
    date = request.form['date']
    group_name = Group.query.get(group_id)
    profile = Profile.query.filter_by(group=group_id).first()

    data = []

    if not profile:
        flash('У этой группы не зарегистрирован староста', 'warning')
    else:
        students = Student.query.filter_by(profile=profile.id).all()

        for i, student in enumerate(students):
            tasks = Task.query.filter_by(student=student.id).all()
            lessons = []

            for task in tasks:

                if task.datetime.strftime('%Y-%m-%d') == date:
                    lessons.append({
                        'title': task.title,
                        'attended': task.attended,
                        'comment': task.comment,
                        'time': task.datetime.strftime('%H:%M')
                    })

            data.append({
                'name': student.name,
                'lessons': lessons
            })

        if not data[0]['lessons']:
            flash('Отсутствуют данные за этот период', 'warning')

    context = dict(
        title=f'Просмотри статистика за {date}',
        header=f'Группа {group_name.name} в {date}',
        data=data,
        user=user,
    )

    return render_template('home/stat/group_ymd.html', **context)


@home.route('/faq', methods=['GET'])
def faq():
    context = dict(
        title='Статистика',
        header='Посещаемые занятия!',
        user=user,
    )

    return render_template('home/faq.html', **context)


@home.route('/student/<student_id>/group/<group_id>', methods=['GET'])
def student_stat(student_id, group_id):
    student = Student.query.get(student_id)
    group_name = Group.query.get(group_id)
    profile = Profile.query.filter_by(group=group_id).first()
    student_data = []

    if profile:
        # posts = Post.query.filter_by (profile=profile.id).all ()
        tasks = Task.query.where(Student.profile == profile.id).all()
        attended_count = Task.query.where(Student.profile == profile.id).filter_by(attended=False).all()
        for task in tasks:
            student_data.append({
                'name': task.title,
                'date': task.datetime.strftime('%Y-%m-%d'),
                'time': task.datetime.strftime('%H:%m'),
                'attended_count': len(attended_count),
                'count': len(tasks)
            })

    print(student_data)

    context = dict(
        title=f'Индивидуальная статистика для студента {student.name}',
        header=f'Студент {student.name}',
        user=user,
        student_data=student_data
    )

    return render_template('home/stat/student.html', **context)
