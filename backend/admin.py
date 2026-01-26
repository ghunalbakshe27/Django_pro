from django.contrib import admin
from .models import customuser, Song, RecentlyPlayed, LikedSong

admin.site.register(customuser)
admin.site.register(Song)
admin.site.register(RecentlyPlayed)
admin.site.register(LikedSong)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'category', 'release_date', 'created_at']
    list_filter = ['category', 'release_date']
    search_fields = ['title', 'artist', 'album']
    ordering = ['-created_at']