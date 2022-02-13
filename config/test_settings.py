from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOG_DIR_PATH = str(BASE_DIR / 'test_logs/') + '/'
OLD_LOG_NAME = 'test_access.old'
LOG_NAME = 'test_access.log'

