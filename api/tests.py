from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIClient


class ApiTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.admin = User.objects.create_superuser(username='admin', password='admin')
        cls.data_admin = {
            'username': 'admin',
            'password': 'admin'
        }

    def test_get_token(self):
        client = APIClient()
        response = client.post('/api/v1/get-token/', self.data_admin, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue('token' in response.json().keys())

        data = {
            'username': 'user',
            'password': 'user'
        }
        response = client.post('/api/v1/get-token/', data, format='json')

        self.assertEqual(response.status_code, 404)

    def test_register(self):
        client = APIClient()
        response = client.post('/api/v1/get-token/', self.data_admin, format='json')
        token = response.json().get('token')

        user_data = {
            'username': 'new_user',
            'password': 'new_user'
        }

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post('/api/v1/register/', user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue('token' in response.json().keys())

        user2_data = {
            'username': 'user2',
            'password': 'user2'
        }
        user_token = response.json().get('token')
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post('/api/v1/register/', user2_data, format='json')

        self.assertEqual(response.status_code, 403)

    def test_get_logs(self):
        call_command('load_fixtures')

        client = APIClient()
        response = client.post('/api/v1/get-token/', self.data_admin, format='json')
        token = response.json().get('token')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        data = {
            "date_from": "2022-02-12",
            "date_to": "2022-02-12",
            "group_by": ""
        }
        response = client.post('/api/v1/get-logs/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(response.json()['data']), 1)

        data = {
            "date_from": "2022-02-12",
            "date_to": "2022-02-12",
            "group_by": "ip"
        }
        response = client.post('/api/v1/get-logs/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(response.json()['data']['157.55.39.215']), 1)

        data = {
            "date_from": "2022-02-12",
            "date_to": "2022-02-12",
            "group_by": "date"
        }
        response = client.post('/api/v1/get-logs/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(response.json()['data']['2022-02-12']), 1)
