from django.urls import path

from .views import ApplicationListAPIView

app_name = 'applications'

urlpatterns = [
    path('', ApplicationListAPIView.as_view(), name='applications'),
]
