from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from portfolizer.views import IndexView, PageNotFoundView
from apps.user.views import RegistrationView, LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
]

urlpatterns += i18n_patterns(
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("404/", PageNotFoundView.as_view(), name="404"),
    path("<slug:slug>/", include("apps.portfolio.urls", namespace="portfolio")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if not settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
