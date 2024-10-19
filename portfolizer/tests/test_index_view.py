from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from apps.common.tests import FlashMessagesMixin
from apps.common.utils import get_model_admin_list_url
from apps.common.views import ButtonLink
from apps.portfolio.models import Portfolio
from apps.portfolio.tests.factories import PortfolioFactory
from apps.user.tests.factories import UserFactory


class TestIndexView(FlashMessagesMixin):
    url_path = reverse_lazy("index")

    def assertResponse(
        self, response, portfolio_button: ButtonLink = None
    ) -> None:
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(
            response.context.get("portfolio_button"), portfolio_button
        )

    def test_page_for_anonymous_user(self):
        response = self.client.get(self.url_path)
        self.assertResponse(response)

    def test_page_for_authenticated_user_without_portfolio(self):
        # When authenticated user doesn't have a portfolio:
        user = UserFactory.create_staff_user()
        self.client.force_login(user)

        response = self.client.get(self.url_path)

        view_portfolio_button = ButtonLink(
            label=_("Create Portfolio"),
            url=get_model_admin_list_url(model_class=Portfolio),
        )
        self.assertResponse(response, portfolio_button=view_portfolio_button)

        # When authenticated user has unpublished portfolio:
        portfolio = PortfolioFactory(user=user, is_published=False)

        response = self.client.get(self.url_path)

        view_portfolio_button = ButtonLink(
            label=_("My Portfolio"),
            url=reverse("portfolio:index", kwargs={"slug": portfolio.slug}),
        )
        self.assertResponse(response, portfolio_button=view_portfolio_button)

        # When authenticated user has published portfolio:
        portfolio.update(is_published=True)

        response = self.client.get(self.url_path)

        self.assertResponse(response, portfolio_button=view_portfolio_button)
