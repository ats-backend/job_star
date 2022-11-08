import base64
import hashlib
import json

from decouple import config
from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import (
    CreateAPIView, GenericAPIView, ListCreateAPIView,
    ListAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from job_star.encryption import encrypt_data, decrypt_data
from jobs.models import Job
from permissions.permissions import IsAuthenticated
from .models import Applicant, Application, ApplicationStatus
from .serializers import (
    ApplicantSerializer, ApplicationDetailSerializer,
    ApplicationSerializer, TrackApplicationSerializer, ApplicationStatusSerializer
)
from renderers.renderers import CustomRender

# Create your views here.


class ObjectMixin:

    def get_object(self):
        obj = self.queryset.filter(application_id==self.kwargs['pk']).first()
        return obj


class ApplicationListAPIView(ListAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class CreateApplicationAPIView(CreateAPIView):
    serializer_class = ApplicationSerializer
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        job = Job.objects.filter(id=kwargs['job_id']).first()
        try:
            applicant_email = request.data.get('applicant').get('email')
        except:
            return Response(
                data="No applicant details provided or invalid key",
                status=status.HTTP_400_BAD_REQUEST
            )
        if job:
            application = Application.objects.filter(
                    job__deadline=job.deadline,
                    applicant__email=applicant_email
                ).first()
            if application:
                return Response(
                    data="Applicant already applied",
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(data=request.data)
            # print(serializer)
            if serializer.is_valid():
                application = serializer.save(job=job)
                data = {
                    'job': str(application.job),
                    'applicant': str(application.applicant),
                    'status': application.status
                }
                return Response(
                    data=data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ApplicationDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationDetailSerializer
    queryset = Application.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class ApplicantListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class ApplicantDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class SetShortlistedApplicationAPIView(ObjectMixin, GenericAPIView):
    queryset = Application.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            application.status = 'shortlisted'
            application.save()
            data = {
                'application_status': application.status
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data="No such application exists!",
            status=status.HTTP_404_NOT_FOUND
        )


class SetInvitedApplicationAPIView(ObjectMixin, GenericAPIView):
    queryset = Application.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            application.status = 'invited'
            application.save()
            data = {
                'application_status': application.status
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data="No such application exists!",
            status=status.HTTP_404_NOT_FOUND
        )


class SetAcceptedApplicationAPIView(ObjectMixin, GenericAPIView):
    queryset = Application.objects.all()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            application.status = 'accepted'
            application.save()
            data = {
                'application_status': application.status
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data="No such application exists!",
            status=status.HTTP_404_NOT_FOUND
        )


class SetRejectedApplicationAPIView(ObjectMixin, GenericAPIView):
    queryset = Application.objects.all()
    ApplicationStatus.objects.filter()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            application.status = 'rejected'
            application.save()
            data = {
                'application_status': application.status
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data="No such application exists!",
            status=status.HTTP_404_NOT_FOUND
        )


class PendingApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(
        application_status__status='pending'
    )
    serializer_class = ApplicationSerializer
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class ShortlistedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(
        application_status__status='shortlisted'
    )
    serializer_class = ApplicationSerializer
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class InvitedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(
        application_status__status='invited'
    )
    serializer_class = ApplicationSerializer
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class AcceptedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(
        application_status__status='accepted'
    )
    serializer_class = ApplicationSerializer
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class RejectedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(
        application_status__status='rejected'
    )
    serializer_class = ApplicationSerializer
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)


class TrackApplicationAPIView(GenericAPIView):
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        decrypted_data = decrypt_data(request.data)
        serializer = TrackApplicationSerializer(data=decrypted_data)
        if serializer.is_valid():
            application_id = serializer.data['application_id']
            application = Application.objects.filter(
                application_id=application_id
            ).first()
            if application:
                # application_status = json.dumps(list(application.application_status.all()))
                application_status = ApplicationStatusSerializer(
                    data=application.application_status.all(),
                    many=True
                )
                data = {
                    'applicant_name': application.applicant.fullname(),
                    'application_id': application.application_id,
                    'application_status': application_status.initial_data
                }
                return Response(
                    # data=encrypt_data(data=data),
                    data=data,
                    status=status.HTTP_200_OK
                )
            return Response(
                data="No such application exists",
                status=status.HTTP_404_NOT_FOUND)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

