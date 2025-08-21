from django.contrib import admin
from .models import User, Track

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username","email","is_staff")

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("id","title","artist","genre","is_published","created_at")
    search_fields = ("title","artist","genre","audio_s3_key")
    list_filter = ("genre","is_published")
