from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import Subscription

SUBSCRIPTION_DAYS = 30


def has_active_subscription(user):
    """True when the user has an active subscription that has not expired."""
    if not user or not user.is_authenticated:
        return False
    return Subscription.objects.filter(
        user=user, is_active=True, end_date__gt=timezone.now()
    ).exists()


def activate_subscription(user):
    """
    Start or extend the user's subscription by 30 days and return it.

    An unexpired active subscription is extended from its current end date;
    otherwise the latest subscription is reactivated from now, and a new one
    is created if the user has none.
    """
    now = timezone.now()
    subscription = Subscription.objects.filter(user=user).order_by('-end_date').first()

    if subscription is None:
        return Subscription.objects.create(
            user=user, is_active=True, end_date=now + timedelta(days=SUBSCRIPTION_DAYS)
        )

    if subscription.is_active and subscription.end_date > now:
        subscription.end_date += timedelta(days=SUBSCRIPTION_DAYS)
    else:
        subscription.is_active = True
        subscription.end_date = now + timedelta(days=SUBSCRIPTION_DAYS)
    subscription.save()
    return subscription


def subscription_price():
    return settings.SUBSCRIPTION_PRICE
