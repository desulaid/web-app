from click import echo, argument
from flask import current_app as app
from flask.cli import AppGroup

from app.database import db, Role, Group, Teacher, Profile

cli = AppGroup ('database')


@cli.command ('init')
def cli_init () -> None:
    db.drop_all ()
    db.create_all ()

    echo ('База данных инициализированна.')


@cli.command ('admin')
@argument ('password')
def cli_admin (password: str) -> None:
    role = Role.query.filter_by (name='Администратор').first ()

    if role:
        db.session.add (Profile (login='admin',
                                 password=password,
                                 name='Администратор',
                                 verify=True,
                                 role_id=role.id,
                                 group_id=None,
                                 teacher_id=None))
        db.session.commit ()

        echo (f'Администратор добавлен. Пароль: {password}')
    else:
        echo ('Ошибка: Отсутствует роль администратора.')


@cli.command ('data')
def cli_data () -> None:
    data: list = app.config['DATA']

    for key in data:
        if key == 'Профили':
            for item in data[key]:
                db.session.add (Role (name=item))
        elif key == 'Группы':
            for item in data[key]:
                db.session.add (Group (name=item))
        elif key == 'Преподаватели':
            for item in data[key]:
                db.session.add (Teacher (name=item))

    db.session.commit ()

    echo ('Данные успешно внесены в базу.')
