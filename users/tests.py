from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        # این متد قبل از هر تست اجرا می‌شود تا داده‌های اولیه را آماده کند
        self.register_url = '/api/users/register/'
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'StrongPassword123!'
        }

    def test_user_registration_success(self):
        """
        تست ثبت‌نام موفق یک کاربر جدید
        """
        response = self.client.post(self.register_url, self.user_data)

        # بررسی اینکه آیا وضعیت پاسخ 201 Created است
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # بررسی اینکه آیا کاربر واقعاً در دیتابیس ذخیره شده است
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_duplicate_username(self):
        """
        تست جلوگیری از ثبت‌نام کاربری که نام کاربری تکراری دارد
        """
        # ابتدا یک کاربر می‌سازیم
        User.objects.create_user(**self.user_data)

        # تلاش برای ثبت‌نام مجدد با همان اطلاعات
        response = self.client.post(self.register_url, self.user_data)

        # باید خطای 400 Bad Request دریافت کنیم
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)