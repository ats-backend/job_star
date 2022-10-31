from django.db import models

from jobs.models import Job

# Create your models here.


class Application(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE,
        related_name='applications'
    )
