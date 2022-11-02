from django.urls import path

from .views import (JobListAPIView, JobDetailAPIView,
                    JobUpdateAPIView)

app_name = 'job'

urlpatterns = [
    path('', JobListAPIView.as_view(), name='jobs'),
    # path('create/', JobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),
    path('<int:pk>/', JobUpdateAPIView.as_view(), name='job-update'),
]
