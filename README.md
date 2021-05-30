# web ~~app~~

#### Инструкаж

```shell
# Скачай
$ git clone https://github.com/desulaid/web-app

# Создай виртуальное окружение
$ python -m venv .venv

# Активируй его
$ source ./.venv/bin/activate

# Установи все пакеты
$ (.venv) pip install -r requirements.txt

# Инициализируй бд
# Создай/измени в .env строку ALCHEMY_DATABASE_URL
# По дефолту sqlite
$ (.venv) flask database init

# Заполни дефолтной инфой
$ (.venv) flask database data

# Добавь локального администратора
$ (.venv) flask database admin [пароль]

# Запусти
$ (.venv) flask run
```

#### .env переменные

```bash
FLASK_APP=app:create_app()
FLASK_ENV=development
SECRET_KEY=рандомная строка
ALCHEMY_DATABASE_URL=postgresql://логин:пароль@хост/бд
```

#### Так, ссылочки

[Connection URI Format](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format)