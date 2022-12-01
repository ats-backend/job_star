import json

from decouple import config
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from applications.models import Application, Applicant
from jobs.models import Job, Cohort, Courses


class ApplicationListAPIViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_items = 15
        applicant_detail = {
            'phone_number': '08024918221',
            'gender': 'male',
            'date_of_birth': '2000-01-03',
            'country_of_origin': 'Nigeria',
            'current_location': 'Ibadan',
            'cover_letter': 'This is my cover letter of 400 characters',
            'qualification': 'B.Tech',
            'graduation_school': 'LAUTECH',
            'course_of_study': 'Computer Engineering',
            'graduation_grade': 'First Class',
            'years_of_experience': 1,
            'is_willing_to_relocate': 1
        }
        cohort = Cohort.objects.create(
            name='ATS 1',
            start_date="2023-01-05", end_date= "2023-06-30",
            application_start_date="2022-11-28T12:53:23+01:00",
            application_end_date="2022-12-21T12:53:23+01:00",
        )
        course = Courses.objects.create(title="Frontend")
        job = Job.objects.create(cohort=cohort, course=course)
        for num in range(1, number_of_items+1):
            applicant = Applicant.objects.create(
                first_name=f'First name {num}',
                last_name=f"Last name {num}",
                email=f"email{num}@gmail.com",
                **applicant_detail
            )
            Application.objects.create(
                job=job, applicant=applicant
            )
    @property
    def request_headers(self):
        headers = {
            'HTTP_API_KEY': config('API_KEY'),
            'HTTP_REQUEST_TS': config('REQUEST_TS'),
            'HTTP_HASH_KEY': config('HASH_KEY')
        }
        return headers

    def test_authorization(self):
        url = reverse('applications:applications')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_applications(self):
        url = reverse('applications:applications')
        self.client.credentials(**self.request_headers)
        res = self.client.get(url, format='json')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(response['success'], True)
        self.assertTrue(bool(response['data']['next']), True)



