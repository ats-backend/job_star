from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Cohort, Courses, Job
from .serializers import CohortSerializers

from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
# request = factory.post('/notes/', {'title': 'new idea'})
request = factory.get('jobs:/cohorts/')
# print(request)

COHORTS_URL = reverse('job:cohorts')
COHORT_CREATE_URL = reverse('job:cohort-create')

class CohortsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # print(self.client)

    def test_retrieve_cohorts_list(self):

        res = self.client.get(COHORTS_URL)
        cohorts = Cohort.objects.all().order_by('-name')
        serializer = CohortSerializers(cohorts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
