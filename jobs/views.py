import requests
from uuid import uuid4

from django.forms import model_to_dict
from django.utils import timezone
from django.shortcuts import get_object_or_404, Http404
from django.db.models.functions import Substr

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Job, Cohort, Courses
from .serializers import (
            JobSerializers, JobListSerializers,
            CoursesSerializers, CohortSerializers,
            CourseDetailSerializer, CohortCountDownSerializer,
            CohortUpdateSerializer, CourseOnlySerializer,
            CohortOnlySerializer, CoursesCreateSerializers,
            JobEditSerializers
            )

from renderers.renderers import CustomRender
from permissions.permissions import IsAuthenticated
from utils.helpers import (
    course_create_assessment_server,
    course_update_assessment_server,
    course_delete_assessment_server
)


class CoursesCreationAPIView(generics.CreateAPIView):
    serializer_class = CoursesCreateSerializers
    queryset = Courses.objects.all()

    def perform_create(self, serializer):

        course_type = serializer.validated_data.get('title')
        course_desc = serializer.validated_data.get('description')
        course_uid = self.get_uid()
        course_create_assessment_server(course_type, course_desc, course_uid)
        return super(CoursesCreationAPIView, self).perform_create(serializer)


class AdminCourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()


class CoursesListAPIView(generics.ListAPIView):
    serializer_class = CoursesSerializers
    endpoint = f"https://assessbk.afexats.com/api/assessment/application-type"

    def get_queryset(self):
        return Courses.active_courses.all()


class CourseListOnlyAPIView(generics.ListAPIView):
    serializer_class = CourseOnlySerializer

    def get_queryset(self):
        try:
            cohort_id = self.kwargs['cohort_id']
            cohort = Cohort.objects.get(id=cohort_id)
            return cohort.courses.all()
        except:
            return None


class CohortListOnlyAPIView(generics.ListAPIView):
    serializer_class = CohortOnlySerializer
    queryset = Cohort.objects.all()


class CourseDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Courses.objects.get(pk=pk)
        except Courses.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseDetailSerializer(course)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()
    lookup_field = 'uid'

    def perform_update(self, serializer):
        course_uid = self.kwargs['uid']
        course_title = serializer.validated_data.get('title')
        course_desc = serializer.validated_data.get('description')
        course_update_assessment_server(course_uid, course_title, course_desc)
        return super(CourseUpdateAPIView, self).perform_update(serializer)


class CourseDeleteAPIView(GenericAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()
    lookup_field = 'uid'

    def post(self, request, *args, **kwargs):
        course_uid = self.kwargs.get('uid')
        course = self.get_object()
        course.is_deleted = not course.is_deleted
        course.save()
        is_deleted = course.is_deleted
        course_delete_assessment_server(is_deleted, course_uid)
        if course.is_deleted:
            return Response(
                data=f"{course.title} is Inactive",
                status=status.HTTP_200_OK
            )
        return Response(
            data=f'{course.title} is Active',
            status=status.HTTP_200_OK
        )


class CohortListAPIView(generics.ListAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()


class CohortCreationAPIView(generics.CreateAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()


class CohortDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()



class CohortUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CohortUpdateSerializer
    queryset = Cohort.objects.all()


class CohortCountDownAPIView(GenericAPIView):

    def get(self, request):
        latest_cohort = Cohort.objects.filter(
            application_end_date__gt=timezone.now(),
            is_deleted=False
        )
        serializer = CohortCountDownSerializer(latest_cohort, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class CohortDestroyAPIView(GenericAPIView):
    serializer_class = CohortSerializers

    def post(self, request, pk):
        cohort = get_object_or_404(Cohort, id=pk)
        cohort.is_deleted = not cohort.is_deleted
        cohort.save()

        if cohort.is_deleted:
            return Response(
                data="Cohort is inactive",
                status=status.HTTP_200_OK
            )
        return Response(
            data="Cohort is active",
            status=status.HTTP_200_OK
        )


class JobListCreateAPIView(generics.ListAPIView):
    queryset = Job.active_jobs.filter(
            cohort__application_end_date__gt=timezone.now()
        )
    serializer_class = JobSerializers

    def post(self, request):
        serializer = JobSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED
                            )
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                        )


class JobDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        job = self.get_object(pk)
        serializer = JobSerializers(job)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK
                        )


class JobUpdateAPIView(APIView):

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        job = self.get_object(pk)
        serializer = JobEditSerializers(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK
                            )
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                        )


class JobDestroyAPIView(GenericAPIView):
    serializer_class = JobSerializers

    def post(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        job.is_deleted = not job.is_deleted
        job.save()

        if not job.is_deleted:
            return Response(
                data="Job is active",
                status=status.HTTP_200_OK
            )
        return Response(
            data="Job is inactive",
            status=status.HTTP_200_OK
        )

