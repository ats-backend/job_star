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
        applicant_data = validated_data.pop('applicant')
        applicant = Applicant.objects.create(**applicant_data)
        application = Application.objects.create(
            applicant=applicant,
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
