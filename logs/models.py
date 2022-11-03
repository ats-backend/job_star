from django.db import models

# Create your models here.


class Log(models.Model):
    actor = models.IntegerField()
    event = models.CharField(max_length=50)
    level = models.CharField(max_length=10)
    message = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def info(event, message):
        log = Log.objects.create(actor='Admin', event=event,
                                 level='info', message=message)
        return log

    @staticmethod
    def warning(event, message):
        log = Log.objects.create(actor='Admin', event=event,
                                 level='info', message=message)
        return log

    @staticmethod
    def error(event, message):
        log = Log.objects.create(actor='Admin', event=event,
                                 level='info', message=message)
        return log