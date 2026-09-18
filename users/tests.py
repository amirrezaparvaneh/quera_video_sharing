from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/register/'
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'StrongPassword123!'
        }

    def test_user_registration_success(self):
        """
        Register a new user successfully.
        """
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_duplicate_username(self):
        """
        Reject registration with a duplicate username.
        """
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)