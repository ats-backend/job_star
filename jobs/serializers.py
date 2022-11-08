import datetime
import pytz

utc = pytz.UTC

from rest_framework import serializers
from .models import Job, Cohort, Courses


class CoursesNextedSerializers(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = (
            'title',
        )


class CoursesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = (
            'title', 'description'
        )

    def validate(self, attrs):
        courses = Courses.objects.values_list('title')

        if any(attrs['title'] in title for title in courses):
            raise serializers.ValidationError({
                "course: A course with this title already exist"
            })
        return attrs


class CohortSerializers(serializers.ModelSerializer):
    courses = CoursesNextedSerializers(many=True)

    class Meta:
        model = Cohort
        fields = (
            'name', 'start_date', 'end_date',
            'application_start_date',
            'application_end_date','courses',
        )

    def create(self, validated_data):
        courses = validated_data.pop('courses')
        cohort_instance = Cohort.objects.create(**validated_data)
        print(courses)
        for course in courses:
            course_title = Courses.objects.filter(
                title__iexact=course.get('title')
             ).first()
            print(course_title)
            cohort_instance.courses.add(course_title)
        cohort_instance.save()
        return cohort_instance

    def update(self, instance, validated_data):
        courses = validated_data.pop('courses')
        instance.title = validated_data.get('title', instance.title)
        instance.application_start_date = validated_data.get(
            'application_start_date', instance.application_start_date)
        instance.application_start_end = validated_data.get(
            'application_start_end', instance.application_start_end)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.end_date = validated_data.get(
            'end_date', instance.end_date)
        instance.courses.add(courses)
        instance.save()
        return instance

    def validate(self, attrs):
        cohort = Cohort.objects.values_list('name')
        if any(attrs['name'] in title for title in cohort):
            raise serializers.ValidationError({
                'Name: A Cohort with that name is already exist'
            })

        return attrs


class JobListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('id', 'title', 'date_posted', 'deadline')


class JobSerializers(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'course', 'cohort',
            'requirement', 'date_posted', 'deadline'
        )

    def validate(self, attrs):
        jobs = Job.objects.values_list('title')
        if any(attrs['title'] in title for title in jobs):
            raise serializers.ValidationError({
                'title: A job with that title is already exist'
            })

        if attrs['deadline'] < utc.localize(datetime.datetime.now()):
            raise serializers.ValidationError({
                'date_posted': "creation date and deadline can not be greater than"
                               "today's date",
            })
        return attrs