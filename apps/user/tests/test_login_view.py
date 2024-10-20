from django.test import TestCase
from django.urls import reverse_lazy, reverse

from apps.user.tests.factories import UserFactory


class TestLoginView(TestCase):
    url_path = reverse_lazy("login")

    def test_renders_page(self):
        response = self.client.get(path=self.url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_successful_login(self):
        form_data = {
            "username": "test@example.com",
            "password": "pass4user",
        }
        user = UserFactory(email=form_data["username"])
        user.set_password(form_data["password"])
        user.save()

        response = self.client.post(path=self.url_path, data=form_data)

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, user)
        self.assertRedirects(response, reverse("index"))
