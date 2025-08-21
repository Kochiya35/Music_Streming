import os
import mimetypes
import uuid

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Favorite, PlayHistory, Playlist, PlaylistTrack, Track, User
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .s3 import create_presigned_get_url, create_presigned_put_url
from .serializers import (
    FavoriteSerializer,
    PlayHistorySerializer,
    PlaylistItemSerializer,
    PlaylistSerializer,
    RegisterSerializer,
    TrackSerializer,
    UserSerializer,
)

# --- Auth / Profile ---
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

# --- Tracks ---
class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["genre", "artist", "is_published"]
    search_fields = ["title", "artist", "genre"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    @action(methods=["post"], detail=False, permission_classes=[IsAdminUser])
    def presigned_upload(self, request):
        filename = request.data.get("filename")
        if not filename:
            return Response({"detail": "filename required"}, status=400)
        content_type = request.data.get("content_type") or mimetypes.guess_type(filename)[0] or "audio/mpeg"
        prefix = os.getenv("AWS_S3_AUDIO_PREFIX", "audio/")
        key = f"{prefix}{uuid.uuid4().hex}{os.path.splitext(filename)[1]}"
        url = create_presigned_put_url(key, content_type, int(os.getenv("AWS_PRESIGNED_EXPIRE_SECONDS", "600")))
        return Response({"key": key, "url": url, "content_type": content_type})

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def stream(self, request, pk=None):
        """GET presigned URL 발급 + 재생기록 저장"""
        track = self.get_object()
        expires = int(os.getenv("AWS_PRESIGNED_EXPIRE_SECONDS", "600"))
        url = create_presigned_get_url(track.audio_s3_key, expires)
        PlayHistory.objects.create(user=request.user, track=track)
        return Response({"url": url, "expires_in": expires})

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        track = self.get_object()
        fav, created = Favorite.objects.get_or_create(user=request.user, track=track)
        if not created:
            fav.delete()
            return Response({"favorited": False})
        return Response({"favorited": True})

# --- Favorites ---
class FavoriteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("track")

# --- Play History ---
class PlayHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayHistorySerializer
    def get_queryset(self):
        return PlayHistory.objects.filter(user=self.request.user).select_related("track")

# --- Playlists ---
class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Playlist.objects.all().prefetch_related("items__track")
        user = self.request.user
        if self.action in ["list", "create"]:
            return qs.filter(user=user)
        return qs.filter(Q(user=user) | Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def add(self, request, pk=None):
        playlist = self.get_object()
        if playlist.user != request.user and not request.user.is_staff:
            return Response({"detail": "권한이 없습니다."}, status=403)
        serializer = PlaylistItemSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        track = Track.objects.get(pk=serializer.validated_data["track_id"])
        order = serializer.validated_data.get("order", 0)
        item, created = PlaylistTrack.objects.get_or_create(
            playlist=playlist, track=track, defaults={"order": order}
        )
        if not created:
            item.order = order
            item.save(update_fields=["order"])
        return Response(PlaylistSerializer(playlist).data)

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def remove(self, request, pk=None):
        playlist = self.get_object()
        if playlist.user != request.user and not request.user.is_staff:
            return Response({"detail": "권한이 없습니다."}, status=403)
        track_id = request.data.get("track_id")
        if not track_id:
            return Response({"detail": "track_id required"}, status=400)
        PlaylistTrack.objects.filter(playlist=playlist, track_id=track_id).delete()
        return Response(PlaylistSerializer(playlist).data)
