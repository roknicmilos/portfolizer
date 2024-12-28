from django.test import TestCase
from django.urls import reverse, reverse_lazy
from apps.portfolio import service as portfolio_service
from apps.user import service as user_service

from apps.user.models import User
from apps.user.tests.factories import UserFactory


class TestRegistrationView(TestCase):
    url_path = reverse_lazy("register")

    def test_get_response(self):
        response = self.client.get(path=self.url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/registration.html")

    def test_post_success_response(self):
        self.assertFalse(User.objects.exists())
        data = {
            "email": "example@example.com",
            "password1": "pass4user",
            "password2": "pass4user",
            "has_accepted_terms_and_policy": True,
        }

        response = self.client.post(path=self.url_path, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin:index"))
        new_user = User.objects.first()
        self.assertEqual(new_user.email, data["email"])
        self.assertTrue(new_user.check_password(data["password1"]))
        self.assertTrue(new_user.is_active)
        self.assertTrue(new_user.is_staff)
        self.assertFalse(new_user.is_superuser)
        actual_permissions = set(new_user.user_permissions.all())
        expected_permissions = {
            *portfolio_service.get_default_portfolio_permission(),
            *user_service.get_default_user_permissions(),
        }
        self.assertEqual(actual_permissions, expected_permissions)

    def test_post_error_response(self):
        """
        When the user submits invalid data, the user should be
        redirected back to the registration page and should be
        shown the error message.
        """
        existing_user = UserFactory()
        self.assertEqual(User.objects.count(), 1)
        data = {
            "email": existing_user.email,
            "password1": "pass4user",
            "password2": "pass4user",
            "has_accepted_terms_and_policy": True,
        }
        self.client.post(path=self.url_path, data=data)

        response = self.client.post(path=self.url_path, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/registration.html")
        self.assertContains(
            response, "User with this Email address already exists."
        )
        self.assertEqual(User.objects.count(), 1)

    def test_should_redirect_to_index_page(self):
        """
        When a user is authenticated and tries to access the
        registration page, the user should be redirected to the
        index page.
        """
        self.client.force_login(UserFactory())
        response = self.client.get(path=self.url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))
