from django import template

register = template.Library()


@register.filter(name="color")
def color(hex_color: str, brightness_factor: float = 1) -> str:
    """
    Adjust the brightness of a HEX color.

    Args:
        hex_color (str): The HEX color value (e.g., "#686868").
        brightness_factor (float): Factor to adjust brightness.
           >1 makes it lighter, <1 makes it darker.

    Returns:
        str: The adjusted color in HEX format.
    """
    # Remove the '#' if present
    hex_color = hex_color.lstrip("#")

    # Convert HEX to RGB
    r, g, b = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]

    # Apply brightness adjustment
    r = min(255, max(0, int(r * brightness_factor)))
    g = min(255, max(0, int(g * brightness_factor)))
    b = min(255, max(0, int(b * brightness_factor)))

    # Convert RGB back to HEX
    return f"#{r:02x}{g:02x}{b:02x}"
