from django.contrib import admin
from .models import Favorite, PlayHistory, Playlist, PlaylistTrack, Track, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff")

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "genre", "is_published", "created_at")
    search_fields = ("title", "artist", "genre", "audio_s3_key")
    list_filter = ("genre", "is_published")

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "track", "created_at")
    search_fields = ("user__username", "track__title")

@admin.register(PlayHistory)
class PlayHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "track", "played_at")
    search_fields = ("user__username", "track__title")
    list_filter = ("played_at",)

class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 0

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "is_public", "created_at")
    search_fields = ("name", "user__username")
    inlines = [PlaylistTrackInline]
