from django.contrib import admin
from .models import Video, WatchHistory, Comment, Rating

admin.site.register(Video)
admin.site.register(WatchHistory)
admin.site.register(Comment)
admin.site.register(Rating)