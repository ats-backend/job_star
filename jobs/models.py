import uuid

from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone


from rest_framework.reverse import reverse


class GeneralManager(models.Manager):
    def get_queryset(self):
        return super(GeneralManager, self).get_queryset(
        ).filter(is_deleted=False,)


class Courses(models.Model):
    title = models.CharField(
        max_length=250, verbose_name='Course Title',
        unique=True
    )
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='course/',
        null=True,
        blank=True
    )
    uid = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    active_courses = GeneralManager()
    objects = models.Manager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def active_cohort(self):
        # print(self.cohort_set.all())
        return self.cohort_set.filter(
            end_date__gt=timezone.now(),
        )

    def open_job(self):
        active_cohort = self.cohort_set.filter(
            end_date__gt=timezone.now(),
        ).first()
        if active_cohort:
            return active_cohort.jobs.all()
        return


class Cohort(models.Model):
    name = models.CharField(max_length=250, unique=True)
    courses = models.ManyToManyField('Courses')
    slug = models.SlugField(null=True, blank=True)
    application_start_date = models.DateTimeField()
    application_end_date = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-application_start_date',)

    def __str__(self):
        return self.name

    def number_of_courses(self):
        return self.courses.count()


@receiver(pre_save, sender=Cohort)
def slugify_title(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug


class Job(models.Model):
    title = models.CharField(
        max_length=200,
        null=True, blank=True,
        unique=True
    )
    slug = models.SlugField(null=True, blank=True)
    course = models.ForeignKey(
        'Courses',
        on_delete=models.CASCADE,
        null=True, blank=True, related_name='jobs'
    )
    cohort = models.ForeignKey(
        'Cohort', on_delete=models.CASCADE,
        related_name='jobs'
    )
    requirement = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_jobs = GeneralManager()

    class Meta:
        ordering = ('-date_posted',)
        unique_together = ('course', 'cohort')

    def __str__(self):
        return self.title

    def ongoing_cohort(self):
        return self.cohort

    def application_url(self):
        return reverse('job:applications', args=[self.id])


@receiver(pre_save, sender=Job)
def slugify_title(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


@receiver(post_save, sender=Job)
def job_title(sender, created, instance, **kwargs):
    if created:
        course_title = instance.course.title
        cohort_title = instance.cohort.name
        job_title = f"{course_title} for {cohort_title}"
        instance.title = job_title
        instance.save()
