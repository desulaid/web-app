from click import echo, argument
from flask import current_app as app
from flask.cli import AppGroup

from app.database import db, Role, Group, Teacher, Profile, Student, Post, Task

import random
from datetime import datetime, time

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


@cli.command('exam')
def cli_exam() -> None:
    data: list = app.config['EXAM_DATA']

    for key in data:
        if key == 'Студенты':
            for item in data[key]:
                db.session.add(Student(name=item,
                                       profile_id=1))
            db.session.commit()
        elif key == 'Предметы':
            for day in range(1, 29):                
                if (day == 6 or day == 7 or
                    day == 13 or day == 14 or
                    day == 20 or day == 21 or
                    day == 27 or day == 28):
                        continue
                
                hour = 8
                minute = 00

                date = datetime(2021, 2, day, hour, minute, 0)                 
                    
                for lesson in data[key][f'{date.weekday()}']:                                      
                    if hour >= 18:
                        hour = 8

                    if minute >= 59:
                        minute = 0
                    

                    timea = time(hour=hour, minute=minute)
                
                    post = Post(profile=1)

                    for i, student in enumerate(data['Студенты'], start=1):  
                        attended = bool(random.getrandbits(1))
                        comment = ''
                        
                        if not attended:
                            comment == 'Заболел'

                        post.tasks.append(Task(title=lesson,
                               attended=attended,
                               comment=comment,
                               datetime=datetime.combine(date.date(), timea),
                               student_id=int(i)))
                        db.session.add(post)
                    minute = 15
                    hour += 2

                db.session.commit()
            
    echo('Данные успешно внесены в базу.')
