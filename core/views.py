import mimetypes, uuid, os
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Track
from .serializers import RegisterSerializer, UserSerializer, TrackSerializer
from .permissions import IsAdminOrReadOnly
from .s3 import create_presigned_put_url

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["genre","artist","is_published"]
    search_fields = ["title","artist","genre"]
    ordering_fields = ["created_at","title"]
    ordering = ["-created_at"]

    @action(methods=["post"], detail=False, permission_classes=[IsAdminUser])
    def presigned_upload(self, request):
        filename = request.data.get("filename")
        if not filename:
            return Response({"detail":"filename required"}, status=400)
        content_type = request.data.get("content_type") or mimetypes.guess_type(filename)[0] or "audio/mpeg"
        prefix = os.getenv("AWS_S3_AUDIO_PREFIX", "audio/")
        key = f"{prefix}{uuid.uuid4().hex}{os.path.splitext(filename)[1]}"
        url = create_presigned_put_url(key, content_type, int(os.getenv("AWS_PRESIGNED_EXPIRE_SECONDS","600")))
        return Response({"key": key, "url": url, "content_type": content_type})
