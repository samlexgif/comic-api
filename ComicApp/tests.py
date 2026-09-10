from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import CustomUser


class RegisterUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_creator_registration_creates_user_with_role(self):
        payload = {
            'username': 'newcreator',
            'email': 'creator@example.com',
            'password': 'Secret123!',
            'role': 'creator',
        }

        response = self.client.post(reverse('register'), payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(username='newcreator').exists())
        self.assertEqual(CustomUser.objects.get(username='newcreator').role, 'creator')
        self.assertIn('role', response.data)


class ApiHealthTests(SimpleTestCase):
    def test_home_page_shows_api_is_working(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ComicVerse API')
        self.assertContains(response, 'API is working')

    def test_api_health_endpoint_returns_ok(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'ok',
            'message': 'ComicVerse API is working',
            'app': 'ComicApp'
        })
