from django.contrib import admin

from parser.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['ip', 'log_time']

