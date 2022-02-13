Приложение для парсинга логов доступа Apache.

Парсинг разработан исходя из наличия в папке логов двух файлов access.old и access.log.
Путь к папке прописывается в .env, имена файлов в settings.py.

Для запуска приложения необходимо:
- добавить в папку конфиг .env файл;
- активировать виртуальное окружение;
- установить зависимости, командой pip install -r requirements.txt;
- установить PostgreSQL, выполнить миграции, командой python manage.py migrate,
- создать суперпользователя, командой python manage.py createsuperuser,
- запустить приложение python manage.py runserver,
- установить redis и запустить redis-server,
- запустить celery, командой celery -A config worker,
- запустить celery beat, командой celery -A config bea

Запуск тестов командой python manage.py test --settings=config.test_settings

Документация API по ссылке: https://documenter.getpostman.com/view/12798618/UVeNkhbu

Содержание файла .env:
[settings]
DEBUG=True
SECRET_KEY=''
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''
LOG_DIR_PATH = ''

 

