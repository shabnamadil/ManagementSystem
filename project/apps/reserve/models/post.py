from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialMediaPlatform(models.Model):
    """
    Represents a social media platform (e.g., Instagram, Facebook).
    """

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        # Add more platforms as needed
    ]

    name = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Represents a social media post to be scheduled and published.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True) 
    content = models.TextField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Post by {self.user} - {self.created_at}" 


class PlatformSpecificSchedule(models.Model):
    """
    Represents the schedule for publishing a post on a specific platform.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='platform_schedules')
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    published_date = models.DateTimeField(null=True, blank=True)  # Actual publishing date
    status = models.CharField(
        max_length=10,
        choices=[
            ('scheduled', 'Scheduled'),
            ('published', 'Published'),
            ('failed', 'Failed'),
        ],
        default='scheduled',
    )  # Status of the scheduled post

    def __str__(self):
        return f"Schedule for {self.post} on {self.platform} - {self.scheduled_date}"

class PostMedia(models.Model):
    """
    Represents a media file (image or video) associated with a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='medias', null = True)
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    file = models.FileField(upload_to='post_media/')

    def __str__(self):
        return f"{self.media_type} for {self.post}"
    
class FetchedPost(models.Model):
    schedule = models.ForeignKey(PlatformSpecificSchedule, on_delete=models.CASCADE) 
    post_id = models.CharField(max_length=255) 
    caption = models.TextField(blank=True, null=True) 
    media_urls = models.JSONField(default=list) 
    fetched_date = models.DateTimeField(auto_now_add=True) 
