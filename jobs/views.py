from django.shortcuts import get_object_or_404, Http404
from django.contrib import messages

from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, GenericAPIView, )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobSerializers
from logs.models import Log


class JobListCreateAPIView(APIView):

    def get(self, request):
        jobs = Job.objects.filter(is_deleted=False).all()
        serializer = JobSerializers(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializers(data=request.data)
        if serializer.is_valid():
            # serializer.save(commit=False)
            # Log.info(event=serializer)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        job = self.get_object(pk)
        serializer = JobSerializers(job)
        return Response(serializer.data)


class JobUpdateAPIView(APIView):

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


class JobDestroyAPIView(GenericAPIView):
    serializer_class = JobSerializers

    def post(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        job.is_deleted = not job.is_deleted
        job.save()
        return Response(status=status.HTTP_200_OK)

