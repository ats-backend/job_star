from django.urls import path

from .views import JobListAPIView

app_name = 'job'

urlpatterns = [
    path('', JobListAPIView.as_view(), name='jobs'),
]
