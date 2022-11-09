from datetime import timedelta, datetime

from django.utils.baseconv import base64
from rest_framework import serializers
from rest_framework.parsers import JSONParser

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
    applicant = ApplicantSerializer(write_only=True)

    class Meta:
        model = Application
        fields = (
            'applicant',
            'applicant_name',
            'applicant_email',
            'status',
        )

    def create(self, validated_data):

        # create an application with the applicant's details
        application = Application.objects.create(
            **validated_data
        )
        application_status = ApplicationStatus.objects.create(
            application=application,
            activity="Completed Application",
            details="You have completed your application and will receive a mail when there is an update"
        )
        # print(application)
        return application


class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer(read_only=True)

    class Meta:
        model = Application
        fields = (
            'applicant',
            'specification',
            'applicant_name',
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
