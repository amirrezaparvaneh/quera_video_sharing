from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # دسترسی: دیدن لیست برای همه آزاد، اما ساخت/ویرایش/حذف فقط برای کاربران لاگین شده
    permission_classes = [IsAuthenticatedOrReadOnly]