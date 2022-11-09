
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone


class Courses(models.Model):
    title = models.CharField(max_length=250, verbose_name='Course Title')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='course/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Cohort(models.Model):
    name = models.CharField(max_length=250, verbose_name='Batch')
    courses = models.ManyToManyField('Courses')
    slug = models.SlugField(null=True, blank=True)
    application_start_date = models.DateTimeField()
    application_end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-start_date',)

    def __str__(self):
        return self.name

    def get_courses(self):
        return self.courses.all()


@receiver(pre_save, sender=Cohort)
def slugify_title(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug


class JobManager(models.Manager):
    def get_queryset(self):
        return super(JobManager, self).get_queryset(
        ).filter(is_delete=False)


class Job(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    course = models.OneToOneField(Courses,
                                on_delete=models.CASCADE,
                                null=True, blank=True, related_name='jobs')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE,
                               related_name='jobs')
    requirement = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_jobs = JobManager()

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


@receiver(post_save, sender=Job)
def job_title(sender, created, instance, **kwargs):
    if created:
        course_title = instance.course.title
        cohort_title = instance.cohort.name
        job_title = f"{course_title} for {cohort_title}"
        instance.title = job_title
        instance.save()
