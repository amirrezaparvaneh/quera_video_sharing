from rest_framework import serializers
from .models import Video, Comment, Rating

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # نام کاربر به صورت خواندنی نمایش داده شود

    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # کاربر ارسال‌کننده کامنت به صورت خودکار از روی درخواست تنظیم می‌شود
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