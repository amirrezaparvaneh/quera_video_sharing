from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'  # تمام فیلدهای مدل ویدیو به JSON تبدیل شوند