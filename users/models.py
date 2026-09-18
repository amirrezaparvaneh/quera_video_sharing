from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # ما از ایمیل به عنوان یک فیلد یکتا و اجباری استفاده می‌کنیم
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username