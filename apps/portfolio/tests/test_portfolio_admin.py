from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.admin.sites import AdminSite

from apps.portfolio.admin import PortfolioAdmin
from apps.portfolio.models import Portfolio
from apps.portfolio.tests.factories import PortfolioFactory
from apps.user.tests.factories import UserFactory


class PortfolioAdminTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.site = AdminSite()
        self.admin = PortfolioAdmin(Portfolio, self.site)
        self.request = self.client.get("/").wsgi_request
        self.staff_user = UserFactory.create_staff_user()
        self.superuser = UserFactory.create_superuser()

    def test_portfolio_link_without_pk(self):
        portfolio = Portfolio(slug="test-portfolio")
        result = self.admin.portfolio_link(portfolio)
        expected = _("Save the Portfolio first to generate the link.")
        self.assertEqual(result, expected)

    def test_portfolio_link_with_pk(self):
        portfolio = Portfolio.objects.create(slug="test-portfolio")
        result = self.admin.portfolio_link(portfolio)
        expected_href = reverse(
            viewname="portfolio:index", kwargs={"slug": portfolio.slug}
        )
        expected_label = _("Show portfolio page")
        expected_html = mark_safe(
            f'<a href="{expected_href}">{expected_label}</a>'
        )
        self.assertEqual(result, expected_html)

    def test_get_queryset(self):
        """
        When the current user is not a superuser, the queryset
        should return only the portfolios that belong to the user.
        When the current user is a superuser, the queryset should
        return all the portfolios.
        """
        portfolios = PortfolioFactory.create_batch(3)
        portfolios[0].update(user=self.staff_user)

        # Test when the current user is not a superuser
        self.request.user = self.staff_user
        queryset = self.admin.get_queryset(self.request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), portfolios[0])

        # Test when the current user is a superuser
        self.request.user = self.superuser
        queryset = self.admin.get_queryset(self.request)
        self.assertEqual(queryset.count(), 3)
        self.assertEqual(set(queryset), set(portfolios))

    def test_get_list_filter(self):
        """
        When the current user is not a superuser, the list filter
        should be empty.
        When the current user is a superuser, the list filter
        should include all the filters.
        """
        # Test when the current user is not a superuser
        self.request.user = self.superuser
        list_filter = self.admin.get_list_filter(self.request)
        self.assertEqual(list_filter, self.admin.list_filter)

        # Test when the current user is a superuser
        self.request.user = self.staff_user
        list_filter = self.admin.get_list_filter(self.request)
        self.assertEqual(list_filter, ())

    def test_get_search_fields(self):
        """
        When the current user is not a superuser, the search fields
        should be empty.
        When the current user is a superuser, the search fields
        should include all the fields.
        """
        # Test when the current user is not a superuser
        self.request.user = self.superuser
        search_fields = self.admin.get_search_fields(self.request)
        self.assertEqual(search_fields, self.admin.search_fields)

        # Test when the current user is a superuser
        self.request.user = self.staff_user
        search_fields = self.admin.get_search_fields(self.request)
        self.assertEqual(search_fields, ())

    def test_has_add_permission(self):
        """
        When the current user is not a superuser, the user should
        be able to add a portfolio only if the user does not have
        any portfolios yet.
        When the current user is a superuser, the user should be
        able to add a portfolio.
        """
        # Test when the current user is not a superuser
        self.request.user = self.staff_user
        self.assertEqual(self.staff_user.portfolio_count, 0)
        self.assertTrue(self.admin.has_add_permission(self.request))

        PortfolioFactory(user=self.staff_user)
        self.assertFalse(self.admin.has_add_permission(self.request))

        # Test when the current user is a superuser
        self.request.user = self.superuser
        self.assertTrue(self.admin.has_add_permission(self.request))

    def test_formfield_for_foreignkey(self):
        """
        When the current user is not a superuser, the queryset
        should be filtered to show only the current user.
        When the current user is a superuser, the queryset should
        show all the users.
        """
        # Test when the current user is a superuser
        self.request.user = self.staff_user
        db_field = Portfolio._meta.get_field("user")
        kwargs = {}
        user_field = self.admin.formfield_for_foreignkey(
            db_field, self.request, **kwargs
        )
        self.assertEqual(user_field.queryset.count(), 1)
        self.assertEqual(user_field.queryset.first(), self.staff_user)

        # Test when the current user is a superuser
        self.request.user = self.superuser
        user_field = self.admin.formfield_for_foreignkey(
            db_field, self.request, **kwargs
        )
        self.assertEqual(user_field.queryset.count(), 2)
        self.assertEqual(
            set(user_field.queryset), {self.staff_user, self.superuser}
        )

    def test_get_changeform_initial_data(self):
        """
        The initial data should include the current user.
        """
        self.request.user = self.staff_user
        initial = self.admin.get_changeform_initial_data(self.request)
        self.assertEqual(initial["user"], self.staff_user)

    def test_get_fieldsets(self):
        """
        When the current user is not a superuser, the user field
        should be removed from the fieldsets.
        When the current user is a superuser, all the fields should
        be included in the fieldsets.
        """
        # Test when the current user is a superuser
        self.request.user = self.staff_user
        actual_fieldsets = self.admin.get_fieldsets(self.request)
        main_fields = list(self.admin.main_fields)
        main_fields.remove("user")
        expected_fieldsets = list(self.admin.fieldsets)
        expected_fieldsets[0][1]["fields"] = tuple(main_fields)
        self.assertEqual(actual_fieldsets, expected_fieldsets)

        # Test when the current user is a superuser
        self.request.user = self.superuser
        actual_fieldsets = self.admin.get_fieldsets(self.request)
        self.assertEqual(actual_fieldsets, list(self.admin.fieldsets))

    def test_save_model(self):
        """
        When the current user is not a superuser, the portfolio
        should be assigned to the current user.
        When the current user is a superuser, the portfolio should
        be assigned to the user selected in the form.
        """
        # Test when the current user is a superuser
        self.request.user = self.staff_user
        portfolio = PortfolioFactory()
        self.admin.save_model(self.request, portfolio, None, False)
        self.assertEqual(portfolio.user, self.staff_user)

        # Test when the current user is a superuser,
        # and the user isn't selected in the form
        self.request.user = self.superuser
        portfolio = PortfolioFactory()
        self.admin.save_model(self.request, portfolio, None, False)
        self.assertIsNone(portfolio.user)

    def test_get_actions(self):
        """
        When the current user is not a superuser, the actions
        should be empty.
        """
        # Test when the current user is not a superuser
        self.request.user = self.staff_user
        actual_list_filter = self.admin.get_actions(self.request)
        self.assertEqual(actual_list_filter, ())

        # Test when the current user is a superuser
        self.request.user = self.superuser
        actual_list_filter = self.admin.get_actions(self.request)
        self.assertEqual(len(actual_list_filter), 1)
