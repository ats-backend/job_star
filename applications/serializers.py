from django.utils.baseconv import base64
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from drf_extra_fields.fields import Base64FileField

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


# APPLICATION_STATUS = (
#         ('pending', 'Pending'),
#         ('shortlisted', 'Shortlisted'),
#         ('passed', 'Passed Assessment'),
#         ('invited', 'Invited for Interview'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     )
