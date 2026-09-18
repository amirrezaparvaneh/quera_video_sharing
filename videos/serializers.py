from rest_framework import serializers
from .models import Video, Comment, Rating
from .models import WatchHistory


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'is_premium', 'views_count', 'created_at']
        read_only_fields = ['views_count']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'video', 'user', 'score']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WatchHistorySerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.title', read_only=True)

    class Meta:
        model = WatchHistory
        fields = ['id', 'video', 'video_title', 'watched_at']