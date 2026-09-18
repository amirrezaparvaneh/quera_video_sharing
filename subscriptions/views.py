from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .models import Subscription, Payment, PaymentHistory
from .serializers import (
    SubscriptionSerializer,
    PaymentSerializer,
    PaymentHistorySerializer,
    MessageResponseSerializer
)

class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class PaymentHistoryListView(generics.ListAPIView):
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentHistory.objects.filter(user=self.request.user)


@extend_schema(responses={200: MessageResponseSerializer})
class CancelSubscriptionView(APIView):
    serializer_class = MessageResponseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            subscription = Subscription.objects.get(user=request.user)
            if not subscription.is_active:
                return Response({"detail": "Your subscription is already inactive."},
                                status=status.HTTP_400_BAD_REQUEST)

            subscription.is_active = False
            subscription.save()
            return Response({"detail": "Subscription cancelled successfully."}, status=status.HTTP_200_OK)
        except Subscription.DoesNotExist:
            return Response({"detail": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(responses={200: MessageResponseSerializer})
class RenewSubscriptionView(APIView):
    serializer_class = MessageResponseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription, created = Subscription.objects.get_or_create(user=request.user)

        if subscription.is_active and subscription.end_date and subscription.end_date > timezone.now():
            subscription.end_date += timedelta(days=30)
        else:
            subscription.is_active = True
            subscription.end_date = timezone.now() + timedelta(days=30)

        subscription.save()

        PaymentHistory.objects.create(
            user=request.user,
            amount=50000,
            status='Success'
        )

        return Response({
            "detail": "Subscription renewed successfully.",
            "end_date": subscription.end_date
        }, status=status.HTTP_200_OK)