
from rest_framework import serializers

from .models import Log


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = (
            'actor', 'event', 'level', 'message', 'timestamp'
        )
