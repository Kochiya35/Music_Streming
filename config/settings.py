import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------------------
# 기본 경로 & 환경변수 로드
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------------------------
# 보안/디버그/호스트
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = [h for h in os.getenv("ALLOWED_HOSTS", "*").split(",") if h]

# -------------------------------------------------------------------
# 앱 설정
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "rest_framework",
    "django_filters",

    # local
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# -------------------------------------------------------------------
# 데이터베이스 (dev=SQLite / prod=MySQL)
#   .env 예시:
#   DB_ENGINE=mysql
#   MYSQL_DATABASE=music
#   MYSQL_USER=admin
#   MYSQL_PASSWORD=xxxxx
#   MYSQL_HOST=your-rds.amazonaws.com
#   MYSQL_PORT=3306
# -------------------------------------------------------------------
if os.getenv("DB_ENGINE", "sqlite").lower() == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DATABASE"),
            "USER": os.getenv("MYSQL_USER"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD"),
            "HOST": os.getenv("MYSQL_HOST", "localhost"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# 커스텀 유저 모델
AUTH_USER_MODEL = "core.User"

# -------------------------------------------------------------------
# 패스워드 정책
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------------------------
# 로케일/타임존
# -------------------------------------------------------------------
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# 정적/미디어
# -------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # 배포 시 collectstatic 용

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"         # 아바타 등 업로드 파일 저장 경로

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------
# DRF / JWT
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# -------------------------------------------------------------------
# AWS S3 (presigned URL)
# -------------------------------------------------------------------
AWS_REGION = os.getenv("AWS_REGION", "")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_PRESIGNED_EXPIRE_SECONDS = int(os.getenv("AWS_PRESIGNED_EXPIRE_SECONDS", "600"))
AWS_S3_AUDIO_PREFIX = os.getenv("AWS_S3_AUDIO_PREFIX", "audio/")

# -------------------------------------------------------------------
# 이메일(개발: 콘솔 출력 / 배포: SMTP로 전환)
# -------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # 개발용
DEFAULT_FROM_EMAIL = "no-reply@example.com"

# 이메일 인증 링크에 사용할 베이스 URL
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8001")

# 배포 예시 (주석 해제하여 사용)
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -------------------------------------------------------------------
# (배포 시 권장) CSRF / CORS 예시
# -------------------------------------------------------------------
# CSRF_TRUSTED_ORIGINS = ["https://your-domain.com", "https://www.your-domain.com"]
# INSTALLED_APPS += ["corsheaders"]
# MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")
# CORS_ALLOWED_ORIGINS = ["https://your-frontend.com"]
# CORS_ALLOW_CREDENTIALS = True
