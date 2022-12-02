import json
from decouple import config

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from jobs.models import Courses, Cohort, Job


class TestCourseCRUDAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        course = Courses.objects.bulk_create([
            Courses(title='Mobile Development with dart',
                    description='for mobile only'),
            Courses(title='Product Management',
                    description='for pm only'),
            Courses(title='Frontend Web development',
                    description='for frontend  only')
        ])

        for cohort_number in range(1, 6):
            cohort = Cohort.objects.create(
                name=f"Ats {cohort_number}",
                start_date="2022-11-30",
                end_date=f"2022-12-1{cohort_number}",
                application_start_date=f"2022-{cohort_number}-07T12:52:59+01:00",
                application_end_date=f"2022-{cohort_number}-25T12:53:10+01:00",
            )
            cohort.courses.set(course)
            cohort.save()

    @property
    def request_headers(self):
        headers = {
            'HTTP_API_KEY': config('API_KEY'),
            'HTTP_REQUEST_TS': config('REQUEST_TS'),
            'HTTP_HASH_KEY': config('HASH_KEY')
        }
        return headers

    # def test_create_courses(self):
    #     previous_course_count = Courses.objects.all()
    #     payload = {'title': 'Programming is easy', 'description': 'The best way to programming'}
    #     response = self.client.post(reverse('job:course-create'), data=payload)
    #     self.assertEqual(Courses.objects.all().count(), previous_course_count + 1)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['title'], 'Programming is easy')
    #
    # def test_list_of_courses(self):
    #     response = self.client.get(reverse('job:course-detail'))
    #     pass

    def test_create_cohort(self):
        payload = {
            "name": "ats 1.1", "courses": [
                    {
                        "title": "Mobile Development with dart"
                    },
                    {
                        "title": "Product Management"
                    },
                    {
                        "title": "Frontend Web development"
                    },
                ], "cohort": 4,
            "application_start_date": "2022-12-07T12:52:59+01:00",
            "application_end_date": "2023-01-07T12:52:59+01:00",
            "start_date": "2022-01-02", "end_date": "2022-11-09"
        }
        self.client.credentials(**self.request_headers)
        res = self.client.post(reverse('job:cohort-create'), data=payload, format='json')
        response = json.loads(res.content)
        print(response)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_all_cohorts(self):

        response = self.client.get(reverse('job:cohorts'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreater(len(response.data['results']), 0)

    # def test_retrieve_one_cohort(self):
    #     self.client.credentials(**self.request_headers)
    #     response = self.client.get(reverse('job:cohort-detail', args=[4]), format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response.data['results'], list)
