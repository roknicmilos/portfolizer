from django.test import TestCase
from django.conf import settings
from apps.common.context_processors import settings_variables


class TestContextProcessors(TestCase):
    def test_settings_variables_context_processor(self):
        request = self.client.get("/").wsgi_request
        context = settings_variables(request)
        self.assertEqual(
            context["GOOGLE_ANALYTICS_TRACKING_ID"],
            settings.GOOGLE_ANALYTICS_TRACKING_ID,
        )
