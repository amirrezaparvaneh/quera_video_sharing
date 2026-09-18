from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Video, Comment, Rating, WatchHistory
from .serializers import VideoSerializer, CommentSerializer, RatingSerializer, WatchHistorySerializer
from .permissions import IsPremiumOrOwner

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsPremiumOrOwner]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a video, increment its view count, and log to watch history.
        """
        instance = self.get_object()

        # 1. Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])

        # 2. Log to user's watch history (if authenticated)
        if request.user.is_authenticated:
            WatchHistory.objects.create(user=request.user, video=instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WatchHistoryListView(generics.ListAPIView):
    serializer_class = WatchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user)