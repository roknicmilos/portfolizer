from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.views import ButtonLink
from apps.portfolio.models import Portfolio
from apps.common.utils import (
    get_model_admin_list_url,
    get_model_admin_details_url,
)
from apps.portfolio.context_processors import portfolio_variables
from apps.portfolio.tests.factories import PortfolioFactory
from apps.user.tests.factories import UserFactory


class TestContextProcessors(TestCase):
    def setUp(self):
        super().setUp()
        self.request = self.client.get("/").wsgi_request

    def test_portfolio_variables_with_anonymous_user(self):
        actual_context = portfolio_variables(self.request)
        expected_context = {"menu": {"portfolio": {}}}
        self.assertEqual(actual_context, expected_context)

    def test_portfolio_variables_with_authenticated(self):
        user = UserFactory()

        # When user doesn't have a portfolio:
        self.assertIsNone(user.portfolio)
        self.request.user = user

        actual_context = portfolio_variables(self.request)

        create_portfolio_button = ButtonLink(
            label=_("Create Portfolio"), url=get_model_admin_list_url(Portfolio)
        )
        expected_profile_menu = {
            "create": create_portfolio_button,
            "view": None,
            "edit": None,
        }
        expected_context = {"menu": {"portfolio": expected_profile_menu}}
        self.assertEqual(actual_context, expected_context)

        # When user has a portfolio:
        portfolio = PortfolioFactory(user=user)
        view_portfolio_button = ButtonLink(
            label=_("View Portfolio"),
            url=reverse("portfolio:index", kwargs={"slug": portfolio.slug}),
        )
        edit_portfolio_button = ButtonLink(
            label=_("Edit Portfolio"),
            url=get_model_admin_details_url(obj=portfolio),
        )

        actual_context = portfolio_variables(self.request)

        expected_profile_menu = {
            "create": create_portfolio_button,
            "view": view_portfolio_button,
            "edit": edit_portfolio_button,
        }
        expected_context = {"menu": {"portfolio": expected_profile_menu}}
        self.assertEqual(actual_context, expected_context)