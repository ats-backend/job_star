from django.utils.baseconv import base64
from rest_framework import serializers
from rest_framework.parsers import JSONParser

from .models import Applicant, Application


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
        fields = ('applicant', 'specification', 'applicant_name', 'status',)

    def create(self, validated_data):
        applicant_data = validated_data.pop('applicant')
        applicant = Applicant.objects.create(**applicant_data)
        application = Application.objects.create(
            applicant=applicant,
            **validated_data
        )
        # print(application)
        return application


class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ('applicant', 'specification', 'applicant_name', 'status',)

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
