from email.policy import default
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default=None)
HTTPS = config("HTTPS", cast=bool, default=False)
HTTP_SCHEMA = "https" if HTTPS else "http"
CSRF_TRUSTED_ORIGINS = [f"{HTTP_SCHEMA}://{host}" for host in ALLOWED_HOSTS]
CSRF_COOKIE_SECURE = HTTPS
SESSION_COOKIE_SECURE = HTTPS

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps:
    "django_pdf_view",
    "smart_fixtures",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "analytical",
    # First party apps:
    "apps.common",
    "apps.user",
    "apps.portfolio",
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

ROOT_URLCONF = "rokis_corner.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.common.context_processors.settings_variables",
            ],
        },
    },
]

WSGI_APPLICATION = "rokis_corner.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default=None),
        "USER": config("DB_USER", default=None),
        "PASSWORD": config("DB_PASSWORD", default=None),
        "HOST": config("DB_HOST", default=None),
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATOR_CLASSES = [
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
    "django.contrib.auth.password_validation.NumericPasswordValidator",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": cls} for cls in AUTH_PASSWORD_VALIDATOR_CLASSES
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media/"

AUTH_USER_MODEL = "user.User"

FIXTURES = {
    "labels": [
        "portfolio",
        "link",
        "skill",
        "language",
        "employment",
        "internship",
        "education",
        "project",
    ],
    "media": [
        {
            "src": BASE_DIR / "apps" / "portfolio" / "fixtures" / "images",
            "dest": MEDIA_ROOT / "portfolio" / "images",
        }
    ],
}

GOOGLE_ANALYTICS_TRACKING_ID = config(
    "GOOGLE_ANALYTICS_TRACKING_ID", default=None
)
