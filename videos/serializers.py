from rest_framework import serializers

from .models import Comment, Rating, Video, WatchHistory
from .permissions import can_access_premium


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'is_premium', 'views_count', 'created_at']
        read_only_fields = ['views_count']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.is_premium and not can_access_premium(getattr(request, 'user', None)):
            data['video_file'] = None
        return data


class VideoRelatedMixin:
    """Comments and ratings on premium videos need premium access."""

    def validate_video(self, video):
        request = self.context['request']
        if video.is_premium and not can_access_premium(request.user):
            raise serializers.ValidationError('A subscription is required for this video.')
        if self.instance is not None and video != self.instance.video:
            raise serializers.ValidationError('The video cannot be changed.')
        return video


class CommentSerializer(VideoRelatedMixin, serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']


class RatingSerializer(VideoRelatedMixin, serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'video', 'user', 'score']
        read_only_fields = ['user']

    def validate(self, attrs):
        if self.instance is None:
            user = self.context['request'].user
            if Rating.objects.filter(user=user, video=attrs['video']).exists():
                raise serializers.ValidationError('You have already rated this video.')
        return attrs


class WatchHistorySerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.title', read_only=True)

    class Meta:
        model = WatchHistory
        fields = ['id', 'video', 'video_title', 'watched_at']
