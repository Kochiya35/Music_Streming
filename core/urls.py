from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    MeView,
    TrackViewSet,
    FavoriteViewSet,
    PlayHistoryViewSet,
    PlaylistViewSet,
    SendVerificationEmailView,
    VerifyEmailView,
    PasswordChangeView,
)

router = DefaultRouter()
router.register(r"tracks", TrackViewSet, basename="track")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"history", PlayHistoryViewSet, basename="history")
router.register(r"playlists", PlaylistViewSet, basename="playlist")

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify/send/", SendVerificationEmailView.as_view(), name="verify_send"),
    path("auth/verify/", VerifyEmailView.as_view(), name="verify"),
    path("auth/password/change/", PasswordChangeView.as_view(), name="password_change"),

    # Me
    path("me/", MeView.as_view(), name="me"),

    # Routers
    path("", include(router.urls)),
]
