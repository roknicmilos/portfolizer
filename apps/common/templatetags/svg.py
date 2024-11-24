from django import template
from django.utils.safestring import mark_safe
import re
from django_pdf_view.templatetags.svg import svg as base_svg

register = template.Library()


@register.simple_tag
def svg(filepath: str, color: str = None) -> str:
    """
    Returns the content of an SVG file with an optional fill color.
    In order to change the color of an SVG, the SVG file must have
    the `data-dynamic-color="true"` attribute in the element that
    should change color.
    """

    original_svg = base_svg(filepath)

    if not color:
        return original_svg

    # Match elements with `data-dynamic-color="true"` and `fill="..."` after it,
    # and replace the `fill` attribute with the new color:
    painted_svg = re.sub(
        r'(<[^>]+data-dynamic-color="true"[^>]*?)\s*fill="[^"]*"',
        lambda match: f'{match.group(1)} fill="{color}"',
        original_svg,
    )

    # Match elements with `fill="..."` and `data-dynamic-color="true"`
    # after it, and replace the `fill` attribute with the new color:
    painted_svg = re.sub(
        r'fill="[^"]*"\s*([^>]*\bdata-dynamic-color="true")',
        lambda match: f'{match.group(1)} fill="{color}"',
        painted_svg,
    )

    return mark_safe(painted_svg)
