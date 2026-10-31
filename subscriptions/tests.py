from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Payment, PaymentHistory, Subscription
from .services import has_active_subscription

User = get_user_model()


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='sub_user', email='sub@example.com', password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_endpoints_require_login(self):
        self.client.force_authenticate(user=None)
        for method, url in [
            ('get', '/api/finance/subscriptions/'),
            ('get', '/api/finance/payments/'),
            ('post', '/api/finance/payments/'),
            ('get', '/api/finance/payments-history/'),
            ('post', '/api/finance/renew/'),
            ('post', '/api/finance/cancel/'),
        ]:
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, url)

    def test_payment_activates_subscription_at_fixed_price(self):
        response = self.client.post('/api/finance/payments/', {'amount': '-5'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment = Payment.objects.get()
        self.assertEqual(payment.status, 'success')
        self.assertEqual(payment.amount, 50000)
        self.assertTrue(has_active_subscription(self.user))

    def test_second_payment_extends_instead_of_creating_another_subscription(self):
        self.client.post('/api/finance/payments/')
        first_end = Subscription.objects.get().end_date
        self.client.post('/api/finance/payments/')
        subscription = Subscription.objects.get()
        self.assertEqual(subscription.end_date, first_end + timedelta(days=30))

    def test_payments_are_read_only_after_creation(self):
        self.client.post('/api/finance/payments/')
        payment = Payment.objects.get()
        detail = f'/api/finance/payments/{payment.id}/'
        self.assertEqual(self.client.get(detail).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.patch(detail, {'amount': '1'}).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(detail).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_payments_are_per_user(self):
        other = User.objects.create_user(username='other', email='o@example.com', password='password123')
        self.client.force_authenticate(user=other)
        self.client.post('/api/finance/payments/')
        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.get('/api/finance/payments/').data, [])

    def test_renew_without_subscription_creates_one(self):
        response = self.client.post('/api/finance/renew/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(has_active_subscription(self.user))
        self.assertEqual(PaymentHistory.objects.filter(user=self.user).count(), 1)

    def test_renew_extends_active_subscription(self):
        self.client.post('/api/finance/renew/')
        first_end = Subscription.objects.get().end_date
        self.client.post('/api/finance/renew/')
        self.assertEqual(Subscription.objects.get().end_date, first_end + timedelta(days=30))

    def test_renew_reactivates_expired_subscription(self):
        Subscription.objects.create(
            user=self.user, is_active=True, end_date=timezone.now() - timedelta(days=3)
        )
        self.assertFalse(has_active_subscription(self.user))
        self.client.post('/api/finance/renew/')
        self.assertTrue(has_active_subscription(self.user))
        self.assertEqual(Subscription.objects.count(), 1)

    def test_cancel_without_subscription_returns_404(self):
        response = self.client.post('/api/finance/cancel/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_works_with_multiple_subscriptions(self):
        end = timezone.now() + timedelta(days=10)
        Subscription.objects.create(user=self.user, is_active=True, end_date=end)
        Subscription.objects.create(user=self.user, is_active=True, end_date=end)
        response = self.client.post('/api/finance/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(has_active_subscription(self.user))

    def test_cancel_already_inactive_returns_400(self):
        Subscription.objects.create(
            user=self.user, is_active=False, end_date=timezone.now() + timedelta(days=10)
        )
        response = self.client.post('/api/finance/cancel/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
