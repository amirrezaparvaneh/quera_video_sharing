from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, CommentViewSet, RatingViewSet, WatchHistoryListView

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('watch-history/', WatchHistoryListView.as_view(), name='watch-history'),
]