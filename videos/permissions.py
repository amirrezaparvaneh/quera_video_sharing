from rest_framework import permissions

from subscriptions.services import has_active_subscription


def can_access_premium(user):
    """Staff and users with an active, unexpired subscription can use premium videos."""
    if not user or not user.is_authenticated:
        return False
    return user.is_staff or has_active_subscription(user)


class IsStaffOrReadOnly(permissions.BasePermission):
    """Anyone can read; only staff can create, change or delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can read; only the owner (or staff) can change or delete an object."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id or request.user.is_staff


class PremiumVideoAccess(permissions.BasePermission):
    """
    Object-level rule: a premium video can be opened only by staff or by a user
    with an active, unexpired subscription. Free videos are open to everyone.
    """

    def has_object_permission(self, request, view, obj):
        if not obj.is_premium:
            return True
        return can_access_premium(request.user)
