from django.shortcuts import render
from django.contrib import messages

from rest_framework.generics import ListAPIView

from .serializers import LogSerializer
from .models import Log

messages.info()

class LogListAPIView(ListAPIView):
    serializer_class = LogSerializer
    queryset = Log.objects.all()
