from django.db import IntegrityError

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, ListCreateAPIView,
    ListAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

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
        obj = self.queryset.filter(id=self.kwargs['pk']).first()
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
                data="No applicant details provided",
                status=status.HTTP_400_BAD_REQUEST
            )
        if job:
            application = Application.objects.filter(
                    job=job,
                    applicant__email=applicant_email
                ).first()
            if application:
                return Response(
                    data="Applicant with that email already applied for this job",
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif Applicant.objects.filter(email=applicant_email).exists():
                applicant = Applicant.objects.filter(email=applicant_email).first()

            else:
                # extract the applicant details from the application data
                applicant_data = request.data.pop('applicant')
                print(applicant_data)
                # serialize, validate and create applicant data with ApplicantSerializer
                applicant_serializer = ApplicantSerializer(data=applicant_data)
                if applicant_serializer.is_valid():
                    applicant = applicant_serializer.save()
                else:
                    return Response(
                        data=applicant_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            serializer = self.get_serializer(data=request.data)
            # print(serializer)
            if serializer.is_valid():
                application = serializer.save(applicant=applicant,job=job)
                data = {
                    'job': str(application.job),
                    'applicant': str(application.applicant),
                    'application_id': application.application_id,
                    'status': application.status,
                    'course': str(application.course)
                }
                return Response(
                    data=data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data="Reference job for application does not exist",
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

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            try:
                application_status = ApplicationStatus.objects.create(
                    application=application,
                    status="shortlisted",
                    activity="Shortlisted For Assessment",
                    details="You have passed the application stage and have been invited to take an assesment."
                )
            except IntegrityError:
                latest_status = ApplicationStatus.objects.filter(
                    application=application
                ).first()
                if latest_status.status != "shortlisted":
                    return Response(
                        data=f"Application status cannot be changed"
                             f" to shortlisted after {latest_status.status}",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    data="Application status is already set to shortlisted",
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'application_status': application_status.status
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

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            try:
                application_status = ApplicationStatus.objects.create(
                    application=application,
                    status="invited",
                    activity="Invited for Interview",
                    details="You have completed your application and will receive a mail when there is an update"
                )
            except IntegrityError:
                latest_status = ApplicationStatus.objects.filter(
                    application=application
                ).first()
                if latest_status.status.lower() != "invited":
                    return Response(
                        data=f"Application status cannot be changed"
                             f" to invited after {latest_status.status}",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    data="Application status is already set to invited",
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'application_status': application_status.status
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

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            try:
                application_status = ApplicationStatus.objects.create(
                    application=application,
                    status="accepted",
                    activity="Accepted Application",
                    details="We are pleased to inform you that you have "
                            "been selected for the AFEX TECH STARS. More "
                            "details on this will be sent to you by mail. "
                            "Congratulations."
                )
            except IntegrityError:
                latest_status = ApplicationStatus.objects.filter(
                    application=application
                ).first()
                if latest_status.status.lower() != "accepted":
                    number_of_accepted_time = ApplicationStatus.objects.filter(
                        application=application,
                        status='accepted'
                    ).count()
                    application_status = ApplicationStatus.objects.create(
                        application=application,
                        status="accepted",
                        activity=f"Accepted Application {number_of_accepted_time+1}",
                        details="We are pleased to inform you that you have "
                            "been selected for the AFEX TECH STARS. More "
                            "details on this will be sent to you by mail. "
                            "Congratulations."
                    )
                    data = {
                        'application_status': application_status.status
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                return Response(
                    data="Application status is already set to accepted",
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'application_status': application_status.status
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

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            try:
                application_status = ApplicationStatus.objects.create(
                    application=application,
                    status="rejected",
                    activity="Rejected Application",
                    details="After reviewing your application,"
                            " we are sorry to inform you that we will "
                            "not be proceeding with your application. "
                            "Thank you."
                )
            except IntegrityError:
                latest_status = ApplicationStatus.objects.filter(
                    application=application
                ).first()
                if latest_status.status.lower() != "rejected":
                    number_of_rejected = ApplicationStatus.objects.filter(
                        application=application,
                        status='rejected'
                    ).count()
                    application_status = ApplicationStatus.objects.create(
                        application=application,
                        status="rejected",
                        activity=f"Rejected Application {number_of_rejected+1}",
                        details="After reviewing your application,"
                                " we are sorry to inform you that we will "
                                "not be proceeding with your application. "
                                "Thank you."
                    )
                    data = {
                        'application_status': application_status.status
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                return Response(
                    data=f"Application status is already set to rejected",
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'application_status': application_status.status
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data="No such application exists!",
            status=status.HTTP_404_NOT_FOUND
        )


class SetPassedApplicationTestAPIView(ObjectMixin, GenericAPIView):
    queryset = Application.objects.all()
    ApplicationStatus.objects.filter()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            try:
                application_status = ApplicationStatus.objects.create(
                    application=application,
                    status="passed",
                    activity="Passed Assessment",
                    details="You have passed your assessment and will receive a mail when there is an update"
                )
            except IntegrityError:
                return Response(
                    data="Application status is already set to passed",
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'application_status': application_status.status
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data="No such application exists!",
            status=status.HTTP_404_NOT_FOUND
        )


class SetFailedApplicationTestAPIView(ObjectMixin, GenericAPIView):
    queryset = Application.objects.all()
    ApplicationStatus.objects.filter()
    renderer_classes = (CustomRender,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            try:
                application_status = ApplicationStatus.objects.create(
                    application=application,
                    status="failed",
                    activity="Failed Assessment",
                    details="You have failed your assessment and will receive a mail when there is an update"
                )
            except IntegrityError:
                return Response(
                    data="Application status is already set to failed",
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'application_status': application_status.status
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
        # decrypted_data = decrypt_data(request.data)
        if request.data.get('application_id'):
            try:
                application = Application.objects.get(
                    application_id__iexact=request.data['application_id']
                )
            except:
                return Response(
                    data="No such application exists",
                    status=status.HTTP_404_NOT_FOUND
                )
            queryset = ApplicationStatus.objects.filter(application=application)
            serializer = ApplicationStatusSerializer(queryset, many=True)
            data = {
                'applicant_name': application.applicant.fullname(),
                'application_id': application.application_id,
                'application_status': serializer.data,
            }
            return Response(
                # data=encrypt_data(data=data),
                data=data,
                status=status.HTTP_200_OK
            )
        data = {
            'application_id': "This field is required"
        }
        return Response(
            data=data,
            status=status.HTTP_404_NOT_FOUND
        )
