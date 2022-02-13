import logging

from celery import shared_task

from parser.backend import LogDb


logger = logging.getLogger('tasks')


@shared_task
def parse_logs():
    """Парсинг логов и сохранение в БД"""
    try:
        LogDb().save_db_new_logs()
    except Exception as e:
        logger.exception(e)
