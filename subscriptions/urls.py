from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionViewSet,
    PaymentViewSet,
    PaymentHistoryListView,
    CancelSubscriptionView,
    RenewSubscriptionView
)

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),

    path('payments-history/', PaymentHistoryListView.as_view(), name='payment-history'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('renew/', RenewSubscriptionView.as_view(), name='renew-subscription'),
]