# Веб приложение на Python

Приложение разрабатывается в рамках дипломной работы. Его суть - учет и ведение посещаемости занятий студентами.


## Установить зависимости
```bash
pip install -r requirements.txt
```

## [.flaskenv](./flaskenv.example)
Используйте `Development` или 
```bash
FLASK_APP=app:create_app('Development')
```


## Создание базы данных
```bash
flask migrate
```

## Запуск приложения
```bash
flask run
```