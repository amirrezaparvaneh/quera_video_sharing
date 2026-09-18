from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Video
from .serializers import VideoSerializer
from .permissions import IsPremiumOrOwner

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # اعمال همزمان احراز هویت عمومی و پرمیشن سفارشی پرمیوم
    permission_classes = [IsAuthenticatedOrReadOnly, IsPremiumOrOwner]