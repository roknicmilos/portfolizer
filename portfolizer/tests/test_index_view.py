from django.test import TestCase
from django.urls import reverse


class TestIndexView(TestCase):
    def test_renders_page(self):
        response = self.client.get(path=reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
