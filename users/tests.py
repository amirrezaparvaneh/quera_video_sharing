from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/v1/users/register/'
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

    def test_user_registration_returns_token(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertIn('token', response.data)

    def test_user_registration_rejects_weak_password(self):
        for password in ('1', '12345678', 'password'):
            data = {**self.user_data, 'password': password}
            response = self.client.post(self.register_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, password)
            self.assertIn('password', response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_login_returns_token(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post('/api/v1/users/login/', {
            'username': 'testuser', 'password': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_rejects_wrong_password(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post('/api/v1/users/login/', {
            'username': 'testuser', 'password': 'wrong'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
