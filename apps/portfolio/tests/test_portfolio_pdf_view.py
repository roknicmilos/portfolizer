from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from apps.common.tests.utils import (
    create_sample_image,
    create_media_absolute_url,
)
from apps.portfolio.tests.factories import PortfolioFactory
from apps.user.tests.factories import UserFactory


class TestPortfolioPDFView(TestCase):
    def setUp(self):
        super().setUp()
        self.portfolio = PortfolioFactory(
            is_published=True,
            user=UserFactory(),
        )
        self.left_segments_patch = patch(
            target="apps.portfolio.service.get_left_column_segments",
            return_value=[],
        )
        self.mock_left_segments = self.left_segments_patch.start()

        self.right_segments_patch = patch(
            target="apps.portfolio.service.get_right_column_segments",
            return_value=[],
        )
        self.mock_right_segments = self.right_segments_patch.start()

    def assertResponseContext(
        self, response, with_avatar: bool = False
    ) -> None:
        self.assertEqual(response.context.get("portfolio"), self.portfolio)
        if with_avatar:
            expected_avatar_url = create_media_absolute_url(
                request=response.wsgi_request, file_field=self.portfolio.avatar
            )
        else:
            expected_avatar_url = ""
        self.assertEqual(
            response.context.get("avatar_url"), expected_avatar_url
        )

        # Assert that the left and right column segments:
        self.mock_left_segments.assert_called_once_with(
            portfolio=self.portfolio
        )
        self.mock_right_segments.assert_called_once_with(
            portfolio=self.portfolio
        )
        self.assertEqual(response.context.get("left_column"), [])
        self.assertEqual(response.context.get("right_column"), [])

        # Reset the mock calls:
        self.mock_left_segments.reset_mock()
        self.mock_right_segments.reset_mock()

        self.assertEqual(
            response.context.get("portfolio_pdf_url"),
            reverse(
                viewname="portfolio:pdf", kwargs={"slug": self.portfolio.slug}
            ),
        )

    def test_get_html_response(self):
        url_path = reverse(
            viewname="portfolio:index", kwargs={"slug": self.portfolio.slug}
        )
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/html")
        self.assertResponseContext(response)

        # When portfolio is not published, but it belongs to the user:
        self.portfolio.update(is_published=False)
        self.client.force_login(user=self.portfolio.user)
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/html")
        self.assertResponseContext(response)

    def test_get_pdf_response(self):
        url_path = reverse(
            viewname="portfolio:pdf", kwargs={"slug": self.portfolio.slug}
        )
        # Test with avatar image:
        self.portfolio.update(avatar=create_sample_image())
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(
            response["Content-Disposition"],
            f'inline; filename="{self.portfolio.filename}"',
        )
        self.assertResponseContext(response, with_avatar=True)

        # When portfolio is not published, but it belongs to the user:
        self.portfolio.update(is_published=False)
        self.client.force_login(user=self.portfolio.user)
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(
            response["Content-Disposition"],
            f'inline; filename="{self.portfolio.filename}"',
        )

    def test_get_download_response(self):
        url_path = reverse(
            viewname="portfolio:download", kwargs={"slug": self.portfolio.slug}
        )
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="{self.portfolio.filename}"',
        )
        self.assertResponseContext(response)

        # When portfolio is not published, but it belongs to the user:
        self.portfolio.update(is_published=False)
        self.client.force_login(user=self.portfolio.user)
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="{self.portfolio.filename}"',
        )
        self.assertResponseContext(response)

    def test_404_response(self):
        # When the slug does not exist:
        url_path = reverse(
            viewname="portfolio:index", kwargs={"slug": "non-existing-slug"}
        )
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 404)

        # When use is anonymous and portfolio is not published:
        self.portfolio.update(is_published=False)
        url_path = reverse(
            viewname="portfolio:index", kwargs={"slug": self.portfolio.slug}
        )
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 404)

        # When user is authenticated and unpublished portfolio
        # does not belong to user:
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        super().tearDown()
        self.left_segments_patch.stop()
        self.right_segments_patch.stop()
