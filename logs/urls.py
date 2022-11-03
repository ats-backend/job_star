from django.urls import path

from .views import LogListAPIView

app_name = 'logs'

urlpatterns = [
    path('', LogListAPIView.as_view(), name='logs'),

]
