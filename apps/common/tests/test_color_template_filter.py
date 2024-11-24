from django.test import SimpleTestCase

from apps.common.templatetags.color import color


class TestColorTemplateFilter(SimpleTestCase):
    def test_color_filter_lighten(self):
        """
        Test that the filter lightens a color correctly when
        brightness_factor > 1.
        """
        # Increase brightness by 50%
        result = color("#686868", 1.5)
        self.assertEqual(result, "#9c9c9c")  # Expected lighter color

    def test_color_filter_darken(self):
        """
        Test that the filter darkens a color correctly when
        brightness_factor < 1.
        """
        # Decrease brightness by 50%
        result = color("#686868", 0.5)
        self.assertEqual(result, "#343434")  # Expected darker color

    def test_color_filter_no_change(self):
        """
        Test that the filter returns the same color when
        brightness_factor = 1.
        """
        result = color("#686868", 1)
        self.assertEqual(result, "#686868")  # No change expected

    def test_color_filter_edge_case_min(self):
        """
        Test that the filter handles the minimum brightness correctly (black).
        """
        result = color("#686868", 0)  # Completely darken
        self.assertEqual(result, "#000000")  # Expected black

    def test_color_filter_edge_case_max(self):
        """
        Test that the filter handles the maximum brightness correctly (white).
        """
        # Brighten excessively
        result = color("#686868", 10)
        self.assertEqual(result, "#ffffff")  # Expected white

    def test_color_filter_invalid_hex(self):
        """
        Test that the filter raises an appropriate error for invalid
        HEX input.
        """
        with self.assertRaises(ValueError):
            color("invalid_hex", 1.5)

    def test_color_filter_short_hex(self):
        """
        Test that the filter raises an error for short HEX input.
        """
        with self.assertRaises(ValueError):
            color("#123", 1.5)

    def test_color_filter_no_hash(self):
        """
        Test that the filter works correctly when the '#' is omitted from
        the color.
        """
        result = color("686868", 1.5)
        self.assertEqual(result, "#9c9c9c")  # Expected lighter color
