from django.conf import settings
from django.core import signing
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Favorite, PlayHistory, Playlist, PlaylistTrack, Track, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "nickname")

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        # 이메일 인증 전까지는 비활성 계정으로 생성
        user = User(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()

        # 이메일 인증 토큰 생성 후 (개발 모드) 콘솔에 인증 URL 출력
        try:
            token = signing.dumps({"uid": user.pk}, salt="email-verify")
            base = getattr(settings, "SITE_URL", "http://127.0.0.1:8001")
            verify_url = f"{base}/api/auth/verify/?token={token}"
            print(f"[EMAIL VERIFY] {user.email} → {verify_url}")
        except Exception as _:
            # settings 미설정 등으로 실패해도 회원 생성은 그대로 진행
            pass

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "nickname", "avatar")


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = (
            "id",
            "title",
            "artist",
            "genre",
            "thumbnail_url",
            "audio_s3_key",
            "duration_sec",
            "is_published",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class FavoriteSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    track_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "track", "track_id", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        track_id = validated_data.pop("track_id")
        track = Track.objects.get(pk=track_id)
        return Favorite.objects.create(user=self.context["request"].user, track=track)


class PlayHistorySerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)

    class Meta:
        model = PlayHistory
        fields = ("id", "track", "played_at")


class PlaylistItemSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    track_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ("id", "track", "track_id", "order", "added_at")
        read_only_fields = ("id", "added_at")


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ("id", "name", "is_public", "created_at", "updated_at", "tracks")
        read_only_fields = ("id", "created_at", "updated_at")

    def get_tracks(self, obj):
        items = obj.items.select_related("track").all()
        return TrackSerializer([it.track for it in items], many=True).data
