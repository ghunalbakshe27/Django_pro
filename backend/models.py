from django.contrib.auth.models import AbstractUser
from django.db import models

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
    release_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=10, blank=True, null=True)  # e.g., "3:45"
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"