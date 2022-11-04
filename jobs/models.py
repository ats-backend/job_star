
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone


class Job(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    responsibilities = models.TextField()
    requirement = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def is_deadline(self):
        return timezone.now() > self.deadline


@receiver(pre_save, sender=Job)
def slugify_title(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug