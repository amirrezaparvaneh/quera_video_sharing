import shutil
import tempfile
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from subscriptions.models import Subscription
from .models import Comment, Rating, Video, WatchHistory

User = get_user_model()

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class BaseVideoTestCase(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.normal_user = User.objects.create_user(
            username='normal_user', email='normal@example.com', password='password123'
        )
        self.premium_user = User.objects.create_user(
            username='premium_user', email='premium@example.com', password='password123'
        )
        self.staff_user = User.objects.create_user(
            username='staff_user', email='staff@example.com', password='password123', is_staff=True
        )
        Subscription.objects.create(
            user=self.premium_user, is_active=True, end_date=timezone.now() + timedelta(days=30)
        )

        def fake_file():
            return SimpleUploadedFile('test_video.mp4', b'file_content', content_type='video/mp4')

        self.free_video = Video.objects.create(
            title='ویدیوی رایگان', description='همه می‌توانند ببینند',
            video_file=fake_file(), is_premium=False,
        )
        self.premium_video = Video.objects.create(
            title='ویدیوی پرمیوم', description='فقط برای مشترکین',
            video_file=fake_file(), is_premium=True,
        )

    def video_url(self, video):
        return f'/api/videos/videos/{video.id}/'


class VideoPermissionTests(BaseVideoTestCase):
    def test_access_free_video(self):
        """ Users without a subscription can retrieve free videos. """
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.video_url(self.free_video))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_retrieve_free_video(self):
        response = self.client.get(self.video_url(self.free_video))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_premium_video_without_subscription(self):
        """ Users without a subscription receive HTTP 403 for premium videos. """
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.video_url(self.premium_video))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_retrieve_premium_video(self):
        response = self.client.get(self.video_url(self.premium_video))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_premium_video_with_subscription(self):
        """ Users with an active subscription can retrieve premium videos. """
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.get(self.video_url(self.premium_video))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['video_file'])

    def test_expired_subscription_cannot_access_premium_video(self):
        Subscription.objects.filter(user=self.premium_user).update(
            end_date=timezone.now() - timedelta(days=1)
        )
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.get(self.video_url(self.premium_video))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_access_premium_video(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.video_url(self.premium_video))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_hides_premium_file_from_non_subscribers(self):
        for user in (None, self.normal_user):
            self.client.force_authenticate(user=user)
            response = self.client.get('/api/videos/videos/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            by_id = {item['id']: item for item in response.data}
            self.assertIsNone(by_id[self.premium_video.id]['video_file'])
            self.assertIsNotNone(by_id[self.free_video.id]['video_file'])

    def test_list_shows_premium_file_to_subscribers(self):
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.get('/api/videos/videos/')
        by_id = {item['id']: item for item in response.data}
        self.assertIsNotNone(by_id[self.premium_video.id]['video_file'])


class VideoWriteTests(BaseVideoTestCase):
    def payload(self):
        return {
            'title': 'new', 'description': 'd', 'is_premium': False,
            'video_file': SimpleUploadedFile('n.mp4', b'x', content_type='video/mp4'),
        }

    def test_anonymous_cannot_create_video(self):
        response = self.client.post('/api/videos/videos/', self.payload(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_cannot_create_update_or_delete_video(self):
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.post('/api/videos/videos/', self.payload(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(self.video_url(self.free_video), {'title': 'x'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.video_url(self.premium_video))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Video.objects.count(), 2)

    def test_staff_can_create_update_and_delete_video(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post('/api/videos/videos/', self.payload(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.patch(self.video_url(self.free_video), {'title': 'renamed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.video_url(self.free_video))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WatchHistoryTests(BaseVideoTestCase):
    def test_retrieve_counts_view_and_logs_history(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.video_url(self.free_video))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views_count'], 1)
        self.assertEqual(WatchHistory.objects.filter(user=self.normal_user).count(), 1)

        response = self.client.get('/api/videos/watch-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['video'], self.free_video.id)

    def test_anonymous_view_counts_without_history(self):
        self.client.get(self.video_url(self.free_video))
        self.free_video.refresh_from_db()
        self.assertEqual(self.free_video.views_count, 1)
        self.assertEqual(WatchHistory.objects.count(), 0)

    def test_history_requires_login_and_is_per_user(self):
        self.assertEqual(
            self.client.get('/api/videos/watch-history/').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        WatchHistory.objects.create(user=self.premium_user, video=self.free_video)
        self.client.force_authenticate(user=self.normal_user)
        self.assertEqual(self.client.get('/api/videos/watch-history/').data, [])


class CommentTests(BaseVideoTestCase):
    url = '/api/videos/comments/'

    def test_create_comment_sets_current_user(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.url, {'video': self.free_video.id, 'content': 'hi'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.get().user, self.normal_user)

    def test_anonymous_cannot_comment(self):
        response = self.client.post(self.url, {'video': self.free_video.id, 'content': 'hi'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_comment_on_premium_video_without_subscription(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.url, {'video': self.premium_video.id, 'content': 'hi'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscriber_can_comment_on_premium_video(self):
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.post(self.url, {'video': self.premium_video.id, 'content': 'hi'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_owner_or_staff_can_change_comment(self):
        comment = Comment.objects.create(user=self.premium_user, video=self.free_video, content='mine')
        detail = f'{self.url}{comment.id}/'

        self.client.force_authenticate(user=self.normal_user)
        self.assertEqual(self.client.patch(detail, {'content': 'x'}).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(detail).status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.premium_user)
        self.assertEqual(self.client.patch(detail, {'content': 'edited'}).status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.staff_user)
        self.assertEqual(self.client.delete(detail).status_code, status.HTTP_204_NO_CONTENT)


class RatingTests(BaseVideoTestCase):
    url = '/api/videos/ratings/'

    def test_score_must_be_between_one_and_five(self):
        self.client.force_authenticate(user=self.normal_user)
        for score in (0, 6, 999):
            response = self.client.post(self.url, {'video': self.free_video.id, 'score': score})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, score)
        response = self.client.post(self.url, {'video': self.free_video.id, 'score': 5})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_one_rating_per_user_and_video(self):
        self.client.force_authenticate(user=self.normal_user)
        self.client.post(self.url, {'video': self.free_video.id, 'score': 4})
        response = self.client.post(self.url, {'video': self.free_video.id, 'score': 5})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 1)

    def test_cannot_rate_premium_video_without_subscription(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.url, {'video': self.premium_video.id, 'score': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_owner_or_staff_can_change_rating(self):
        rating = Rating.objects.create(user=self.premium_user, video=self.free_video, score=3)
        detail = f'{self.url}{rating.id}/'

        self.client.force_authenticate(user=self.normal_user)
        self.assertEqual(self.client.patch(detail, {'score': 1}).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(detail).status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.premium_user)
        self.assertEqual(self.client.patch(detail, {'score': 5}).status_code, status.HTTP_200_OK)
