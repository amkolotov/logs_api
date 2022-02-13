from datetime import datetime, timedelta
from itertools import groupby

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from api.serializers import LogSerializer
from parser.models import Log


def create_user_in_db(request):
    """Создание пользователя в БД"""
    username = request.data['username']
    password = request.data['password']
    if User.objects.filter(username=username).exists():
        return None
    user = User.objects.create_user(username=username, password=password)
    return user


def get_user_from_db(request):
    """Получение пользователя из БД"""
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    return user


def get_filtered_logs_from_db(request):
    """Получение логов из БД, согласно параметрам запроса"""
    date_from = request.data.get('date_from', '')
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
        except ValueError:
            date_from = ''

    date_to = request.data.get('date_to', '')
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            date_to = ''

    if not date_to and not date_from:
        logs = Log.objects.filter(log_time__range=[(timezone.now() - timedelta(days=1)).date(), timezone.now().date()])
    elif date_from and not date_to:
        logs = Log.objects.filter(log_time__range=[date_from, date_from + timedelta(days=1)])
    elif date_to and not date_from:
        logs = Log.objects.filter(log_time__range=[date_to - timedelta(days=1), date_to])
    else:
        logs = Log.objects.filter(log_time__range=[date_from, date_to + timedelta(days=1)])

    group_by = request.data.get('group_by', '')
    if group_by and group_by in ('ip', 'date'):
        if group_by == 'ip':
            logs = logs.order_by('ip')
            group_logs = groupby(logs, lambda x: x.ip)
        else:
            logs = logs.order_by('-log_time')
            group_logs = groupby(logs, lambda x: x.log_time.date())
        result = {str(name): LogSerializer(list(items), many=True).data for name, items in group_logs}
    else:
        result = LogSerializer(logs, many=True).data

    return result
