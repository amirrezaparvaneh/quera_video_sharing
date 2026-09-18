from rest_framework import serializers
from .models import Subscription, Payment, PaymentHistory
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

        end_date = timezone.now() + timedelta(days=30)
        subscription = Subscription.objects.create(
            user=user,
            end_date=end_date,
            is_active=False
        )

        payment = Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=amount,
            status='success'  # Simulate a successful payment without contacting a payment gateway.
        )

        subscription.is_active = True
        subscription.save()

        return payment


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'amount', 'transaction_date', 'status']


class MessageResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    end_date = serializers.DateTimeField(required=False, allow_null=True)