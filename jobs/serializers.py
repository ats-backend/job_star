import datetime
import pytz
from django.utils import timezone

from rest_framework.reverse import reverse

utc = pytz.UTC

from rest_framework import serializers
from .models import Job, Cohort, Courses
from applications.models import Application


class CoursesNextedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = (
            'title',
        )

class TotalCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = (
            'number_of_course'
        )


class NextedCohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = (
            'name',
            'start_date',
            'end_date',
        )

class CourseOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = (
            'id', 'title'
        )
        extra_kwargs = {
            "title": {"read_only":True}
        }


class CohortOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Cohort
        fields = (
            'id', 'name'
        )
        extra_kwargs = {
            'name': {"read_only": True}
        }


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
            'image',
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
            'image',
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


class CohortCountDownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cohort
        fields = ('application_end_date',)


class CohortSerializers(serializers.ModelSerializer):
    courses = CoursesNextedSerializers(many=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cohort
        fields = (
            'url',
            'name', 'start_date', 'end_date',
            'application_start_date',
            'application_end_date', 'courses',
            'number_of_courses'
        )

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('job:cohort-detail',
                       kwargs={'pk': obj.pk},
                       request=request
                       )

    def validate_application_start_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Cohort's application start date must be a current or future time"
            )
        return value

    def validate_application_end_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Cohort's application end date must be a future time"
            )
        cohort = Cohort.objects.filter(
            application_end_date__gte=timezone.now()
        ).exists()
        if cohort:
            raise serializers.ValidationError(
                "A cohort with an active application already exists"
            )
        return value


    def validate(self, attrs):
        cohort_start_date = attrs['start_date']
        cohort_end_date = attrs['end_date']
        cohort_application_start_date = attrs['application_start_date']
        cohort_application_end_date = attrs['application_end_date']

        if cohort_end_date <= cohort_start_date:
            raise serializers.ValidationError(
                'Cohort end date must be greater than start date'
            )

        if cohort_application_end_date <= cohort_application_start_date:
            raise serializers.ValidationError(
                'Cohort application end date must be greater than start date'
            )
        return attrs

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
                    print(courses_id)
                    instance.courses.add(courses_id[d])
            instance.save()
            return instance
        except:
            raise Exception({
                'An error occurred'
            })

class CohortUpdateSerializer(serializers.ModelSerializer):
    courses = CoursesNextedSerializers(many=True)

    class Meta:
        model = Cohort
        fields = (
            'name', 'start_date', 'end_date',
            'application_start_date',
            'application_end_date', 'courses',
        )

    def validate(self, attrs):
        cohort_start_date = attrs['start_date']
        cohort_end_date = attrs['end_date']
        cohort_application_start_date = attrs['application_start_date']
        cohort_application_end_date = attrs['application_end_date']

        if cohort_end_date <= cohort_start_date:
            raise serializers.ValidationError(
                'Cohort end date must be greater than start date'
            )

        if cohort_application_end_date <= cohort_application_start_date:
            raise serializers.ValidationError(
                'Cohort application end date must be greater than start date'
            )
        return attrs

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

        try:
            for course in courses:
                for d in course:
                    course_id = Courses.objects.get(title=(course[d]))
                    print(d)
                    courses_id.append(course_id.pk)
                    instance.courses.add(courses_id[0])
            instance.save()
            return instance
        except:
            raise Exception({
                'An error occurred'
            })

class JobListSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = (
            'url',
            'id',
            'title',
            'date_posted',
            # 'application',
            'application_url'
                  )

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('job:job-detail',
                       kwargs={'pk': obj.pk},
                       request=request
                       )


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

class CohortNextedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cohort
        fields = (
            'name',
        )


class JobSerializers(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'course', 'cohort',
            'requirement', 'date_posted', 'created_by'
        )
        extra_kwargs = {
            'created_by': {'required': True}
        }



