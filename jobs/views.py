import logging

from django.utils import timezone
from django.shortcuts import get_object_or_404, Http404

from rest_framework.generics import (GenericAPIView)
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Job, Cohort, Courses
from .serializers import (JobSerializers, JobListSerializers,
                          CoursesSerializers, CohortSerializers)
from logs.logs import log_writter
from renderers.renderers import CustomRender


class CoursesCreationAPIView(generics.CreateAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()
    renderer_classes = (CustomRender,)


class CoursesListAPIView(generics.ListAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()
    renderer_classes = (CustomRender,)


class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()
    renderer_classes = (CustomRender,)


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CoursesSerializers
    queryset = Courses.objects.all()
    renderer_classes = (CustomRender,)


class CourseDeleteAPIView(GenericAPIView):
    serializer_class = CoursesSerializers
    renderer_classes = (CustomRender,)

    def post(self, request, pk):
        course = get_object_or_404(Courses, id=pk)
        course.is_delete = not course.is_delete
        course.save()

        if course.is_delete:
            return Response(
                data=f"{course.title} is dis-active",
                status=status.HTTP_200_OK
            )
        return Response(
            data=f'{course.title} is Active',
            status=status.HTTP_200_OK
        )


class CohortListAPIView(generics.ListAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()
    renderer_classes = (CustomRender,)


class CohortCreationAPIView(generics.CreateAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()


class CohortDetailAPIView(CustomRender, generics.RetrieveAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()


class CohortUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CohortSerializers
    queryset = Cohort.objects.all()
    renderer_classes = (CustomRender,)


class CohortDestroyAPIView(GenericAPIView):
    serializer_class = CohortSerializers
    renderer_classes = (CustomRender,)

    def post(self, request, pk):
        cohort = get_object_or_404(Cohort, id=pk)
        cohort.is_deleted = not cohort.is_deleted
        cohort.save()

        if cohort.is_deleted:
            return Response(
                data="Job is dis-active",
                status=status.HTTP_200_OK
            )
        return Response(
            data="Job is active",
            status=status.HTTP_200_OK
        )


class JobListCreateAPIView(CustomRender, APIView):

    today = timezone.now()

    def get(self, request, *args, **kwargs):
        active_jobs = Job.objects.filter(
            is_deleted=False,
            deadline__gt=self.today
            ).all()
        serializer = JobListSerializers(active_jobs, many=True)
        # print(log_writter())
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailAPIView(CustomRender, APIView):

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        job = self.get_object(pk)
        serializer = JobSerializers(job)
        return Response(serializer.data)


class JobUpdateAPIView(CustomRender, APIView):

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def put(self, request, pk,):
        job = self.get_object(pk)
        serializer = JobSerializers(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDestroyAPIView(CustomRender, GenericAPIView):
    serializer_class = JobSerializers

    def post(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        job.is_deleted = not job.is_deleted
        job.save()

        if not job.is_deleted:
            return Response({
                "Job is active"
            })
        return Response({
            "Job is dis-active"
        })

