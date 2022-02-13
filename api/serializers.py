from rest_framework import serializers

from parser.models import Log


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = ['ip', 'text', 'log_time']
