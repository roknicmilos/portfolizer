from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from portfolizer.views import IndexView
from apps.user.views import RegistrationView, LoginView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("<slug:slug>/", include("apps.portfolio.urls", namespace="portfolio")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if not settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
