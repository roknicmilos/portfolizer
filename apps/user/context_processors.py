from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.utils import get_model_admin_details_url
from apps.common.views import ButtonLink
from apps.user.models import User


def user_variables(request: WSGIRequest) -> dict:
    if request.user.is_anonymous:
        user_menu = {
            "login": _init_login_button(),
            "register": _init_register_button(),
        }
    else:
        user_menu = {
            "edit": _init_edit_user_button(request.user),
            "logout": _init_logout_button(),
        }

    return {"user_menu": user_menu}


def _init_login_button() -> ButtonLink:
    return ButtonLink(label=_("Login"), url=reverse("login"))


def _init_register_button() -> ButtonLink:
    return ButtonLink(label=_("Register"), url=reverse("register"))


def _init_edit_user_button(user: User) -> ButtonLink:
    url = get_model_admin_details_url(user)
    return ButtonLink(label=_("Account Settings"), url=url)


def _init_logout_button() -> ButtonLink:
    return ButtonLink(label=_("Logout"), url=reverse("admin:logout"))
