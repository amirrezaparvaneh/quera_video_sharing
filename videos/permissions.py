from rest_framework import permissions
from subscriptions.models import Subscription


class IsPremiumOrOwner(permissions.BasePermission):
    """
    اجازه تماشای ویدیوهای پرمیوم فقط به کاربران دارای اشتراک فعال یا ادمین داده می‌شود.
    """

    def has_object_permission(self, request, view, obj):
        # اگر ویدیو پرمیوم نیست، همه می‌توانند آن را ببینند
        if not obj.is_premium:
            return True

        # اگر کاربر لاگین نکرده باشد، اجازه دسترسی ندارد
        if not request.user or not request.user.is_authenticated:
            return False

        # اگر کاربر ادمین یا استاف باشد، دسترسی کامل دارد
        if request.user.is_staff:
            return True

        # بررسی اینکه آیا کاربر اشتراک فعال دارد یا خیر
        return Subscription.objects.filter(user=request.user, is_active=True).exists()