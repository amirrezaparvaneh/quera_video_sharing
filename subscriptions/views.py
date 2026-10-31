from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .models import Subscription, Payment, PaymentHistory
from .services import activate_subscription, subscription_price
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
        if getattr(self, 'swagger_fake_view', False):
            return Subscription.objects.none()
        return Subscription.objects.filter(user=self.request.user)

class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Payment.objects.none()
        return Payment.objects.filter(user=self.request.user)


class PaymentHistoryListView(generics.ListAPIView):
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentHistory.objects.filter(user=self.request.user)


@extend_schema(request=None, responses={200: MessageResponseSerializer})
class CancelSubscriptionView(APIView):
    serializer_class = MessageResponseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        if not subscriptions.exists():
            return Response({"detail": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)

        if not subscriptions.filter(is_active=True).update(is_active=False):
            return Response({"detail": "Your subscription is already inactive."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Subscription cancelled successfully."}, status=status.HTTP_200_OK)


@extend_schema(request=None, responses={200: MessageResponseSerializer})
class RenewSubscriptionView(APIView):
    serializer_class = MessageResponseSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        subscription = activate_subscription(request.user)

        PaymentHistory.objects.create(
            user=request.user,
            amount=subscription_price(),
            status='Success'
        )

        return Response({
            "detail": "Subscription renewed successfully.",
            "end_date": subscription.end_date
        }, status=status.HTTP_200_OK)
