from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# SECURITY
# -----------------------------------------------------------------------------

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="").split(",")
    if host.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -----------------------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "apps.accounts",
    "apps.tasks",
    "apps.annotation",
]

# -----------------------------------------------------------------------------
# CLOUDINARY (OPTIONAL)
# -----------------------------------------------------------------------------

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")

if CLOUDINARY_CLOUD_NAME:
    INSTALLED_APPS += [
        "cloudinary",
        "cloudinary_storage",
    ]

# -----------------------------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# -----------------------------------------------------------------------------
# TEMPLATES
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# -----------------------------------------------------------------------------
# DATABASE
# -----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# -----------------------------------------------------------------------------
# STATIC FILES
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# -----------------------------------------------------------------------------
# MEDIA FILES
# -----------------------------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# STORAGES
# -----------------------------------------------------------------------------

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# If Cloudinary credentials exist, use Cloudinary only for media files.
if CLOUDINARY_CLOUD_NAME:
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
        "API_KEY": config("CLOUDINARY_API_KEY"),
        "API_SECRET": config("CLOUDINARY_API_SECRET"),
    }

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config("CORS_ALLOWED_ORIGINS").split(",")
    if origin.strip()
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config("CSRF_TRUSTED_ORIGINS").split(",")
    if origin.strip()
]

# -----------------------------------------------------------------------------
# DRF
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# -----------------------------------------------------------------------------
# JWT
# -----------------------------------------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# -----------------------------------------------------------------------------
# AUTH USER
# -----------------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"