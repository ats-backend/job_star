import base64

from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import (
    CreateAPIView, GenericAPIView, ListCreateAPIView,
    ListAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from jobs.models import Job
from .models import Applicant, Application
from .serializers import ApplicantSerializer, ApplicationDetailSerializer, ApplicationSerializer

# Create your views here.


class ApplicationListAPIView(ListAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()


class CreateApplicationAPIView(CreateAPIView):
    serializer_class = ApplicationSerializer

    def post(self, request, *args, **kwargs):
        job = Job.objects.filter(id=kwargs['job_id']).first()
        applicant_email = request.data.get('applicant').get('email')
        if job:
            application = Application.objects.filter(
                    job__deadline=job.deadline,
                    applicant__email=applicant_email
                ).first()
            if application:
                return Response({
                    'success': False,
                    'error': "Applicant already applied"
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            # print(serializer)
            if serializer.is_valid():
                application = serializer.save(job=job)
                data = {
                    'job': str(application.job),
                    'applicant': str(application.applicant),
                    'specification': application.specification,
                    'status': application.status
                }
                return Response({
                    'success': True,
                    'data': data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)


class ApplicationDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationDetailSerializer
    queryset = Application.objects.all()


class ApplicantListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()


class ApplicantDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()
    lookup_field = 'id'


class SetShortlistedApplicationAPIView(GenericAPIView):
    queryset = Application.objects.all()

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        application.status = 'shortlisted'
        return Response({
            'success': True,
            'application_status': application.status
        }, status=status.HTTP_200_OK)


class SetInvitedApplicationAPIView(GenericAPIView):
    queryset = Application.objects.all()

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        application.status = 'invited'
        return Response({
            'success': True,
            'application_status': application.status
        }, status=status.HTTP_200_OK)


class SetAcceptedApplicationAPIView(GenericAPIView):
    queryset = Application.objects.all()

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        application.status = 'accepted'
        return Response({
            'success': True,
            'application_status': application.status
        }, status=status.HTTP_200_OK)


class SetRejectedApplicationAPIView(UpdateAPIView):
    queryset = Application.objects.all()

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        application.status = 'rejected'
        return Response({
            'success': True,
            'application_status': application.status
        }, status=status.HTTP_200_OK)


class PendingApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(status='pending')
    serializer_class = ApplicationSerializer


class ShortlistedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(status='shortlisted')
    serializer_class = ApplicationSerializer


class InvitedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(status='invited')
    serializer_class = ApplicationSerializer


class AcceptedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(status='accepted')
    serializer_class = ApplicationSerializer


class RejectedApplicationListAPIView(ListAPIView):
    queryset = Application.objects.filter(status='rejected')
    serializer_class = ApplicationSerializer


class TrackApplicationAPIView(GenericAPIView):
    pass