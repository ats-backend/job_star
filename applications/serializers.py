from datetime import timedelta, datetime

from django.utils.baseconv import base64
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.validators import UniqueTogetherValidator

from jobs.models import Job
from .models import Applicant, Application, ApplicationStatus


class ApplicantSerializer(serializers.ModelSerializer):
    # resume = Base64FileField()
    # attachments = Base64FileField()

    class Meta:
        model = Applicant
        exclude = ('id',)

    def validate_gender(self, value):
        # check if the applicant's gender is either male or female
        if value.lower() not in ('male', 'female'):
            raise serializers.ValidationError(
                "Gender can either be male or female"
            )
        return value

    def validate_date_of_birth(self, value):
        # minimum age of an applicant is 16
        # get the minimum age in days
        min_age_in_days = timedelta(days=16*365)

        # get today's date
        today = datetime.today().date()

        # check if difference of today's date and the applicant date of birth
        # is more than minimum age
        if (today-value) < min_age_in_days:
            raise serializers.ValidationError(
                "Minimum age for an applicant is 16, kindly enter a valid date of birth."
            )
        return value


class ApplicationSerializer(serializers.ModelSerializer):
    # applicant = ApplicantSerializer(write_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='applications:application_detail',
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Application
        fields = (
            'job',
            'applicant',
            'applicant_name',
            'applicant_email',
            'applicant_phone',
            'application_id',
            'course',
            'status',
            'url',
        )

        extra_kwargs = {
            'application': {'write_only': True}
        }

    def validate(self, attrs):
        job = attrs.get('job')
        applicant = attrs.get('applicant')
        application = Application.objects.filter(
            job=job,
            applicant=applicant
        ).exists()
        if application:
            raise serializers.ValidationError(
                "Applicant already applied for the job"
            )
        # print(attrs)
        return attrs

    def create(self, validated_data):
        application = Application.objects.create(
            **validated_data
        )
        application_status = ApplicationStatus.objects.create(
            application=application,
            activity="Completed Application",
            details="You have completed your application and "
                    "will receive a mail when there is an update"
        )
        return application


class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer(read_only=True)

    class Meta:
        model = Application
        fields = (
            'applicant',
            'application_id',
            'course',
            'status',
        )

    def create(self, validated_data):
        print("Got called")
        applicant_data = validated_data.pop('applicant')
        applicant = Applicant.objects.create(**applicant_data)
        application = Application.objects.create(
            applicant=applicant,
            **validated_data
        )
        # print(application)
        return application


class TrackApplicationSerializer(serializers.Serializer):
    application_id = serializers.CharField()


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationStatus
        fields = (
            'status',
            'application',
            'activity',
            'details',
            'timestamp',
        )
        extra_kwargs = {
            'application': {'write_only': True}
        }
