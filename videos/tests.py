from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from .models import Video
from subscriptions.models import Subscription

User = get_user_model()


class VideoPermissionTests(APITestCase):
    def setUp(self):
        # ۱. ساخت دو نوع کاربر با ایمیل‌های متفاوت و یکتا: عادی و پرمیوم
        self.normal_user = User.objects.create_user(
            username='normal_user',
            email='normal@example.com',
            password='password123'
        )
        self.premium_user = User.objects.create_user(
            username='premium_user',
            email='premium@example.com',
            password='password123'
        )

        # محاسبه تاریخ ۳۰ روز آینده برای انقضای اشتراک
        future_date = timezone.now() + timedelta(days=30)

        # اختصاص اشتراک فعال به کاربر پرمیوم به همراه تاریخ پایان
        Subscription.objects.create(
            user=self.premium_user,
            is_active=True,
            end_date=future_date
        )

        # ۲. ساخت یک فایل ویدیویی شبیه‌سازی‌شده (Fake File) برای تست
        fake_video = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        # ۳. ساخت دو نوع ویدیو: رایگان و پرمیوم
        self.free_video = Video.objects.create(
            title="ویدیوی رایگان",
            description="همه می‌توانند ببینند",
            video_file=fake_video,
            is_premium=False
        )

        self.premium_video = Video.objects.create(
            title="ویدیوی پرمیوم",
            description="فقط برای مشترکین",
            video_file=fake_video,
            is_premium=True
        )

    def test_access_free_video(self):
        """ کاربر عادی باید بتواند ویدیوی رایگان را ببیند """
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'/api/videos/videos/{self.free_video.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_premium_video_without_subscription(self):
        """ کاربر عادی نباید بتواند ویدیوی پرمیوم را ببیند (خطای 403) """
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'/api/videos/videos/{self.premium_video.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_premium_video_with_subscription(self):
        """ کاربر دارای اشتراک باید بتواند ویدیوی پرمیوم را ببیند """
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.get(f'/api/videos/videos/{self.premium_video.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)