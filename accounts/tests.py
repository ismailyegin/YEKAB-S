from rest_framework.test import APITestCase
from django.urls import reverse


class UserRegistrationTestCare(APITestCase):
    url = reverse('accounts:login')

    def test_user_registration(self):
        data = {

            'username': 'admin',
            'password': 'kobil2013'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
