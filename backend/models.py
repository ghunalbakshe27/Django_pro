from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class customuser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.username

class Song(models.Model):
    CATEGORY_CHOICES = [
        ('new_releases', 'New Release'),
        ('top', 'Top Hits'),
        ('trend', 'Trending'),
        ('bhajan', 'Bhajan'),
        ('punjabi_hits', 'Punjabi'),
        ('topeng', 'English'),
        ('indianhits', 'Indian'),
        ('phonk', 'Phonk'),
        ('arjit','Arjit'),
        ('drivelist','DriveList'),
        ('genres','Genres'),
        ('honeys','Honeys'),
        ('mixlist','MixList'),
        ('subh1','Subh'),
    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True, null=True)
    cover_image = models.ImageField(upload_to='song_covers/', blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    duration = models.CharField(max_length=10, blank=True, null=True)  # e.g., "3:45"
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"

# 🔥 NEW MODEL: Track Recently Played Songs
class RecentlyPlayed(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, related_name='recently_played')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    played_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-played_at']
        unique_together = ['user', 'song']  # Prevent duplicate entries
    
    def __str__(self):
        return f"{self.user.username} - {self.song.title}"


# 🔥 NEW MODEL: Track Liked Songs
class LikedSong(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, related_name='liked_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-liked_at']
        unique_together = ['user', 'song']  # One like per song per user
    
    def __str__(self):
        return f"{self.user.username} likes {self.song.title}"