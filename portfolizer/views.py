from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from apps.common.utils import get_model_admin_change_list_url
from apps.common.views import ButtonLink
from apps.portfolio.models import Portfolio


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["portfolio_button"] = self._create_portfolio_button()
        return context

    def _create_portfolio_button(self) -> ButtonLink:
        if portfolio := self.request.user.portfolio:
            url = reverse("portfolio:index", kwargs={"slug": portfolio.slug})
            return ButtonLink(label=_("My Portfolio"), url=url)

        url = get_model_admin_change_list_url(model_class=Portfolio)
        return ButtonLink(label=_("Create Portfolio"), url=url)
