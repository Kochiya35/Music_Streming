from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),  # 프론트엔드 메인
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
