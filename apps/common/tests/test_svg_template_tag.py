from django.test import SimpleTestCase
from unittest.mock import patch

from apps.common.templatetags.svg import svg


class TestSvgTemplateTag(SimpleTestCase):
    @patch("apps.common.templatetags.svg.base_svg")
    def test_svg_without_color(self, mock_base_svg):
        """
        Test that the original SVG is returned when no color is provided.
        """
        mock_base_svg.return_value = '<svg><path fill="red" /></svg>'
        svg_path = "path/to/icon.svg"

        svg_html = svg(svg_path)

        self.assertEqual(svg_html, mock_base_svg.return_value)
        mock_base_svg.assert_called_once_with(svg_path)

    @patch("apps.common.templatetags.svg.base_svg")
    def test_svg_with_color_and_dynamic_attribute(self, mock_base_svg):
        """
        Test that the `fill` attribute of elements with
        `data-dynamic-color="true"` is updated with the provided color.
        """
        mock_base_svg.return_value = """
            <svg>
                <path fill="red" data-dynamic-color="true" />
                <circle data-dynamic-color="true" fill="blue" />
                <circle fill="green" />
            </svg>
        """
        svg_path = "path/to/icon.svg"

        actual_svg_html = svg(svg_path, "#00ff00")

        expected_svg_html = """
            <svg>
                <path data-dynamic-color="true" fill="#00ff00" />
                <circle data-dynamic-color="true" fill="#00ff00" />
                <circle fill="green" />
            </svg>
        """
        self.assertEqual(actual_svg_html, expected_svg_html)
        mock_base_svg.assert_called_once_with(svg_path)
