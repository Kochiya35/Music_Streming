import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    def __str__(self):
        return self.username or f"User#{self.pk}"

class Track(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=120)
    genre = models.CharField(max_length=80, blank=True)
    thumbnail_url = models.URLField(blank=True)
    audio_s3_key = models.CharField(max_length=255, help_text="S3 object key (e.g., audio/uuid.mp3)")
    duration_sec = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.title} - {self.artist}"
