from decouple import config
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from applications.models import Application, Applicant


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
        # for num in range(1, number_of_items+1):
        #     applicant = Applicant.objects.create(
        #         first_name=f'First name {num}',
        #         last_name=f"Last name {num}",
        #         email=f"email{num}@gmail.com",
        #         **applicant_detail
        #     )
        #     Application.objects.create(
        #         job=1, applicant=applicant
        #     )

    def test_authorization(self):
        url = reverse('applications:applications')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_get_all_applications(self):
    #     url = reverse('applications:applications')
    #     print(url)
    #     request_headers = {
    #         'HTTP_API_KEY': config('API_KEY'),
    #         'HTTP_REQUEST_TS': config('REQUEST_TS'),
    #         'HTTP_HASH_KEY': config('HASH_KEY')
    #     }
    #     self.client.credentials(**request_headers)
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     print(response.data)
    #     self.assertEqual(response.data['success'], True)



