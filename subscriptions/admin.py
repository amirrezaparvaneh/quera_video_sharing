from django.contrib import admin
from .models import Subscription, Payment

admin.site.register(Subscription)
admin.site.register(Payment)