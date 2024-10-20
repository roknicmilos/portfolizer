from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.views import ButtonLink
from apps.common.utils import get_model_admin_details_url
from apps.user.context_processors import user_variables
from apps.user.tests.factories import UserFactory


class TestContextProcessors(TestCase):
    def setUp(self):
        super().setUp()
        self.request = self.client.get("/").wsgi_request

    def test_user_variables_with_anonymous_user(self):
        actual_context = user_variables(self.request)
        login_button = ButtonLink(label=_("Login"), url=reverse("login"))
        register_button = ButtonLink(
            label=_("Register"), url=reverse("register")
        )
        expected_context = {
            "user_menu": {
                "login": login_button,
                "register": register_button,
            }
        }
        self.assertEqual(actual_context, expected_context)

    def test_user_variables_with_authenticated(self):
        user = UserFactory()
        self.request.user = user

        actual_context = user_variables(self.request)

        edit_user_button = ButtonLink(
            label=_("Account Settings"),
            url=get_model_admin_details_url(obj=user),
        )
        logout_button = ButtonLink(
            label=_("Logout"), url=reverse("admin:logout")
        )
        expected_context = {
            "user_menu": {"edit": edit_user_button, "logout": logout_button}
        }
        self.assertEqual(actual_context, expected_context)
