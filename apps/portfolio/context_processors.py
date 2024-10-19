from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.utils import (
    get_model_admin_list_url,
    get_model_admin_details_url,
)
from apps.common.views import ButtonLink
from apps.portfolio.models import Portfolio


def portfolio_variables(request: WSGIRequest) -> dict:
    context = {"menu": {"portfolio": {}}}

    if request.user.is_anonymous:
        return context

    context["menu"]["portfolio"] = {
        "create": _init_create_portfolio_button(),
        "view": _init_view_portfolio_button(portfolio=request.user.portfolio),
        "edit": _init_edit_portfolio_button(portfolio=request.user.portfolio),
    }

    return context


def _init_create_portfolio_button() -> ButtonLink:
    url = get_model_admin_list_url(Portfolio)
    return ButtonLink(label=_("Create Portfolio"), url=url)


def _init_view_portfolio_button(portfolio: Portfolio) -> ButtonLink | None:
    if not portfolio:
        return None

    url = reverse(viewname="portfolio:index", kwargs={"slug": portfolio.slug})
    return ButtonLink(label=_("View Portfolio"), url=url)


def _init_edit_portfolio_button(portfolio: Portfolio) -> ButtonLink | None:
    if not portfolio:
        return None

    url = get_model_admin_details_url(obj=portfolio)
    return ButtonLink(label=_("Edit Portfolio"), url=url)
