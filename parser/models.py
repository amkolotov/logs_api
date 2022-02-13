from django.db import models


class Log(models.Model):
    """Модель лога"""
    ip = models.CharField('IP адрес', max_length=15, db_index=True)
    text = models.TextField('Текст лога')
    log_time = models.DateTimeField('Время лога', db_index=True)

    def __str__(self):
        return f'{self.ip} - {self.log_time}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
