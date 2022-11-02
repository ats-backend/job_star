from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class Job(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    responsibilities = models.TextField()
    requirement = models.TextField()
    experience = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job-detail', args=[self.pk])


@receiver(pre_save, sender=Job)
def slugify_title(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug