import os
import re
from datetime import datetime

from django.conf import settings

from parser.models import Log


class LogParser:
    """Парсер лог файлов"""
    def __init__(self):
        self.dir_path = settings.LOG_DIR_PATH
        self.old_name = settings.OLD_LOG_NAME
        self.log_name = settings.LOG_NAME
        self.logs = None

        self.pattern_log = settings.RE_PATTERN_LOG
        self.pattern_ip = settings.RE_PATTERN_IP
        self.pattern_date = settings.RE_PATTERN_DATE

    def find_all(self):
        paths = [self.dir_path + self.old_name, self.dir_path + self.log_name]
        logs = []
        for path in paths:
            if os.path.exists(path):
                with open(path) as f:
                    data = f.read()
                    current_logs = re.findall(self.pattern_log, data)
                    logs += current_logs
        return logs

    def parse_date(self, log):
        date_str = re.findall(self.pattern_date, log)[0][1:-1]
        date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S %z')
        return date

    def parse_ip(self, log):
        return re.findall(self.pattern_ip, log)[0]


class LogDb:
    """Класс для работы с объектами Log в БД"""
    def __init__(self):
        self.parser = LogParser()

    def save_db_new_logs(self):
        logs = self.parser.find_all()
        last_log = Log.objects.last()
        text_log = last_log.text if last_log else ''
        try:
            idx = logs.index(text_log)
            idx += 1
        except ValueError:
            idx = 0
        if idx <= len(logs):
            for log in logs[idx:]:
                Log.objects.create(
                    ip=self.parser.parse_ip(log),
                    text=log,
                    log_time=self.parser.parse_date(log)
                )
