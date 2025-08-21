from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView, MeView, TrackViewSet,
    FavoriteViewSet, PlayHistoryViewSet, PlaylistViewSet
)

router = DefaultRouter()
router.register(r"tracks", TrackViewSet, basename="track")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"history", PlayHistoryViewSet, basename="history")
router.register(r"playlists", PlaylistViewSet, basename="playlist")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
