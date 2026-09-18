from rest_framework import serializers
from .models import Subscription, Payment
from datetime import timedelta
from django.utils import timezone


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'start_date', 'end_date', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data.get('amount')

        # ۱. ابتدا یک اشتراک ۳۰ روزه جدید برای کاربر می‌سازیم (به صورت پیش‌فرض غیرفعال تا پرداخت انجام شود)
        end_date = timezone.now() + timedelta(days=30)
        subscription = Subscription.objects.create(
            user=user,
            end_date=end_date,
            is_active=False
        )

        # ۲. رکورد پرداخت را به این اشتراک متصل می‌کنیم
        payment = Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=amount,
            status='success'  # در محیط تمرینی پرداخت را مستقیماً موفق در نظر می‌گیریم
        )

        # ۳. حالا که پرداخت موفق شد، اشتراک را فعال می‌کنیم
        subscription.is_active = True
        subscription.save()

        return payment