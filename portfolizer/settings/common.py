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

if HTTPS:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True  # Redirects all non-HTTPS requests to HTTPS
    SESSION_COOKIE_SECURE = True  # session cookie is only sent over HTTPS
    CSRF_COOKIE_SECURE = True  # CSRF token cookie is only sent over HTTPS

# Application definition

INSTALLED_APPS = [
    "admin_interface",  # (third-party) must come before "django.contrib.admin"
    "colorfield",  # (third-party) must come before "django.contrib.admin"
    "smart_fixtures",  # (third-party) must come before "modeltranslation"
    "modeltranslation",  # (third-party) must come before "django.contrib.admin"
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps:
    "django_pdf_view",
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
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolizer.urls"

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
                "apps.portfolio.context_processors.portfolio_variables",
                "apps.user.context_processors.user_variables",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolizer.wsgi.application"

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

# Enable internationalization
USE_I18N = True

# Enable localization
USE_L10N = True

# Enable timezone handling
USE_TZ = True
TIME_ZONE = "UTC"

# Set the default language
LANGUAGE_CODE = "en"

# Define the available languages
LANGUAGES = [
    ("en", "English"),
    ("sr", "Serbian"),
]

# Set the path for translation files
LOCALE_PATHS = [
    BASE_DIR / "run" / "locale/",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "run" / "static"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "run" / "media"

AUTH_USER_MODEL = "user.User"

LOGOUT_REDIRECT_URL = "index"

FIXTURES = {
    "labels": [
        "user",
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
