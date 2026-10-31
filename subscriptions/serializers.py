from rest_framework import serializers
from .models import Subscription, Payment, PaymentHistory
from django.db import transaction

from .services import activate_subscription, subscription_price


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'start_date', 'end_date', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'created_at']
        read_only_fields = ['amount', 'status', 'created_at']

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        subscription = activate_subscription(user)

        # Simulated payment: no payment gateway is contacted.
        return Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=subscription_price(),
            status='success',
        )


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'amount', 'transaction_date', 'status']


class MessageResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    end_date = serializers.DateTimeField(required=False, allow_null=True)