from django.urls import path

from .views import (JobListCreateAPIView, JobDetailAPIView,
                    JobUpdateAPIView, JobDestroyAPIView)

app_name = 'job'

urlpatterns = [
    path('job-list-create', JobListCreateAPIView.as_view(), name='jobs'),
    # path('create/', JobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/detail', JobDetailAPIView.as_view(), name='job-detail'),
    path('<int:pk>/update', JobUpdateAPIView.as_view(), name='job-update'),
    path('<int:pk>/delete', JobDestroyAPIView.as_view(), name='job-delete')
]
