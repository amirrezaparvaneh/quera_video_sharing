from rest_framework import permissions
from subscriptions.models import Subscription


class IsPremiumOrOwner(permissions.BasePermission):
    """
    Premium access requires staff status or an active subscription; expiry is not checked.
    """

    def has_object_permission(self, request, view, obj):
        if not obj.is_premium:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return Subscription.objects.filter(user=request.user, is_active=True).exists()