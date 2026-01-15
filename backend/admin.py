from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'category', 'release_date', 'created_at']
    list_filter = ['category', 'release_date']
    search_fields = ['title', 'artist', 'album']
    ordering = ['-created_at']