from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.portfolio.validators import SlugBlacklistValidator


class TestSlugBlacklistValidator(TestCase):
    def setUp(self):
        super().setUp()
        self.validator = SlugBlacklistValidator()

    def test_allowed_slugs(self):
        for slug in ["allowed", "another-allowed"]:
            try:
                self.validator(slug)
            except ValidationError:
                self.fail(
                    "SlugBlacklistValidator raised ValidationError "
                    "for an allowed slug."
                )

    def test_blacklisted_slugs(self):
        for slug in SlugBlacklistValidator.root_url_paths:
            with self.assertRaises(ValidationError) as context:
                self.validator(slug)
            self.assertEqual(
                context.exception.message,
                "The slug '%(value)s' is reserved and cannot be used.",
            )
