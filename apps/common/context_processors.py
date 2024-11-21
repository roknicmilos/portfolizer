from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest


def settings_variables(request: WSGIRequest) -> dict:
    return {
        "GOOGLE_ANALYTICS_TRACKING_ID": settings.GOOGLE_ANALYTICS_TRACKING_ID,
    }
