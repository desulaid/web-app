from datetime import datetime
from click import echo, argument
from flask import current_app as app
from flask.cli import AppGroup

from app.database import db, Role, Student, Group, Teacher, Post, Task, Profile

cli = AppGroup('database')


@cli.command('init')
def cli_init() -> None:
    db.drop_all()
    db.create_all()

    echo('База данных инициализированна.')


@cli.command('admin')
@argument('password')
def cli_admin(password: str) -> None:
    role = Role.query.filter_by(name='Администратор').first()

    if role:
        db.session.add(Profile(login='admin', 
                            password=password, 
                            name='Администратор', 
                            verify=True, 
                            role_id=role.id, 
                            group_id=None, 
                            teacher_id=None))
        db.session.commit()

        echo(f'Администратор добавлен. Пароль: {password}')
    else:
        echo('Ошибка: Отсутствует роль администратора.')


@cli.command('data')
def cli_data() -> None:
    data: list = app.config['DATA']

    for key in data:
        if key == 'Профили':
            for item in data[key]:
                db.session.add(Role(name=item))
        elif key == 'Группы':
            for item in data[key]:
                db.session.add(Group(name=item))
        elif key == 'Преподаватели':
            for item in data[key]:
                db.session.add(Teacher(name=item))

    db.session.commit()

    echo('Данные успешно внесены в базу.')


@cli.command('test')
def test_database() -> None:
    group = Group.query.get(1)
    teacher = Teacher.query.get(1)
    role = Role.query.get(1)
    profile = Profile(login='test', password='123', name='Test Test', verify=True, role_id=role.id, group_id=group.id, teacher_id=teacher.id)
    db.session.add(profile)
    db.session.commit()

    student = Student(name='Тестовое имя', profile_id=1)
    db.session.add(student)
    db.session.commit()

    task = Task(title='Тествый таск', datetime=datetime.now(), student_id=1)
    db.session.add(task)
    db.session.commit()

    task1 = Task(title='Тествый таск', datetime=datetime.now(), student_id=1)
    db.session.add(task1)
    db.session.commit()

    post = Post(profile=1)
    tesks = ['Тествый таск 1', 'Тествый таск 2']
    for i, value in enumerate(tesks):
        post.tasks.append(Task(title=value, datetime=datetime.now(), student_id=1))
    db.session.add(post)
    db.session.commit()



    student = db.session.query(Student).get(1)
    posts = db.session.query(Post).filter_by(profile=1).all()
    for post in posts:
        tasks = post.tasks.filter_by(student=1).all()
        for task in tasks:
            db.session.delete(task)
    db.session.commit()

