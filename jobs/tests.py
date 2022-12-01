from django.test import TestCase
from django.urls import reverse

from rest_framework import APITestCase



class TestListCreateAPIView(APITestCase):

    def test_list_of_courses(self):
        response = self.client.get(reverse('job:course-detail'))
