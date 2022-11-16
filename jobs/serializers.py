import datetime
import pytz
from django.utils import timezone

from rest_framework.reverse import reverse

utc = pytz.UTC

from rest_framework import serializers
from .models import Job, Cohort, Courses


class CoursesNextedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = (
            'title',
        )


class NextedCohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = (
            'name',
            'start_date',
            'end_date',
        )


class NextedJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'cohort',
            'requirement',
            'date_posted',
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    # open_cohort = serializers.SerializerMethodField(read_only=True)
    # cohort = serializers.HyperlinkedRelatedField(queryset=Courses.objects.filter())
    active_cohort = NextedCohortSerializer(many=True)
    open_job = NextedJobSerializer(many=True)

    class Meta:
        model = Courses
        fields = (
            'title',
            'description',
            'active_cohort',
            'open_job'
        )


class CoursesSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Courses
        fields = (
            'url',
            'title',
            'description'
        )

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('job:course-detail',
                       kwargs={'pk': obj.pk},
                       request=request
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
            'application_end_date', 'courses',
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
        instance.name = validated_data.get('name', instance.name)
        instance.application_start_date = validated_data.get(
            'application_start_date', instance.application_start_date)
        instance.application_end_date = validated_data.get(
            'application_start_end', instance.application_end_date)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.end_date = validated_data.get(
            'end_date', instance.end_date)
        courses_id = []

        try:
            for course in courses:
                for d in course:
                    course_id = Courses.objects.get(title=(course[d]))
                    courses_id.append(course_id.pk)
                    print(course_id.title)
                    print(courses_id)
                    instance.courses.add(courses_id[0])
            instance.save()
            return instance
        except:
            raise Exception({
                'An error occurred'
            })

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


class NestedCohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = (
            'name', 'courses', 'application_start_date',
            'application_end_date', 'start_date', 'end_date'
        )


class NestedCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title', 'description', 'image',
            'created_at', 'is_delete'
        )


class JobSerializers(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id', 'title', 'course', 'cohort',
            'requirement', 'date_posted'
        )

    def validate(self, attrs):
        if attrs['deadline'] < utc.localize(datetime.datetime.now()):
            raise serializers.ValidationError({
                'date_posted': "creation date and deadline can not be greater than"
                               "today's date",
            })
        return attrs
