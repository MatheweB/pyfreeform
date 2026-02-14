"""Color utilities for PyFreeform."""

from __future__ import annotations

import colorsys
from typing import ClassVar


# Standard SVG/CSS named color → RGB mapping.
NAMED_COLOR_RGB: dict[str, tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "coral": (255, 127, 80),
    "crimson": (220, 20, 60),
    "gold": (255, 215, 0),
    "indigo": (75, 0, 130),
    "lime": (0, 255, 0),
    "maroon": (128, 0, 0),
    "navy": (0, 0, 128),
    "olive": (128, 128, 0),
    "silver": (192, 192, 192),
    "teal": (0, 128, 128),
    "turquoise": (64, 224, 208),
    "violet": (238, 130, 238),
}


class Color:
    """
    Represents a color that can be specified in multiple formats.

    Supported formats:
        - Named colors: "red", "blue", "black"
        - Hex codes: "#ff0000", "#f00"
        - RGB tuples: (255, 0, 0)

    Example:
        ```python
        Color("red").to_hex()         # 'red'
        Color("#ff0000").to_hex()      # '#ff0000'
        Color((255, 0, 0)).to_hex()   # '#ff0000'
        ```
    """

    # Common named colors - keep it simple
    NAMED_COLORS: ClassVar[set[str]] = set(NAMED_COLOR_RGB.keys())

    def __init__(self, value: str | tuple[int, int, int]) -> None:
        """
        Create a color from a string or RGB tuple.

        Args:
            value: Color as a named color, hex code, or RGB tuple.
        """
        self._original = value
        self._hex = self._normalize(value)

    def _normalize(self, value: str | tuple[int, int, int]) -> str:
        """Convert any color format to a usable string."""
        if isinstance(value, tuple):
            if len(value) != 3:
                raise ValueError(f"RGB tuple must have 3 values, got {len(value)}")
            r, g, b = value
            if not all(0 <= c <= 255 for c in (r, g, b)):
                raise ValueError("RGB values must be between 0 and 255")
            return f"#{r:02x}{g:02x}{b:02x}"

        if isinstance(value, str):
            value = value.strip().lower()

            # Named color
            if value in self.NAMED_COLORS:
                return value

            # Hex color
            if value.startswith("#"):
                hex_part = value[1:]
                if len(hex_part) == 3:
                    # Expand shorthand: #f00 -> #ff0000
                    hex_part = "".join(c * 2 for c in hex_part)
                if len(hex_part) != 6:
                    raise ValueError(f"Invalid hex color: {value}")
                # Validate hex characters
                try:
                    int(hex_part, 16)
                except ValueError as e:
                    raise ValueError(f"Invalid hex color: {value}") from e
                return f"#{hex_part}"

            # Might be a named color we don't recognize - allow it
            # (browsers support many more named colors)
            return value

        raise TypeError(f"Color must be a string or RGB tuple, got {type(value)}")

    def to_hex(self) -> str:
        """Return the color as a string suitable for SVG."""
        return self._hex

    def to_rgb(self) -> tuple[int, int, int]:
        """Convert this color to an RGB tuple.

        Returns:
            (r, g, b) tuple with values 0-255.

        Raises:
            ValueError: If the color is an unrecognized named color that
                cannot be converted to RGB.
        """
        h = self._hex
        if h.startswith("#"):
            return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
        if h in NAMED_COLOR_RGB:
            return NAMED_COLOR_RGB[h]
        raise ValueError(
            f"Cannot convert '{h}' to RGB — unknown named color. "
            f"Use a hex code or RGB tuple instead."
        )

    def to_hsl(self) -> tuple[float, float, float]:
        """Convert this color to an HSL tuple.

        Returns:
            (h, s, l) tuple where h is 0-360, s and l are 0.0-1.0.

        Raises:
            ValueError: If the color is an unrecognized named color that
                cannot be converted to RGB.

        Example:
            ```python
            Color("red").to_hsl()     # (0.0, 1.0, 0.5)
            Color("#00ff00").to_hsl()  # (120.0, 1.0, 0.5)
            Color("white").to_hsl()   # (0.0, 0.0, 1.0)
            ```
        """
        r, g, b = self.to_rgb()
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        return (round(h * 360, 2), round(s, 4), round(l, 4))

    def __str__(self) -> str:
        return self._hex

    def __repr__(self) -> str:
        return f"Color({self._original!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return self._hex == other._hex
        return False


ColorLike = str | tuple[int, int, int]
"""Type alias for color values: named color, hex string, or RGB tuple."""


# =========================================================================
# Color Transforms
# =========================================================================


def apply_brightness(color: ColorLike, brightness: float) -> str:
    """Apply a brightness multiplier to a color.

    Scales each RGB channel by *brightness* (0.0 = black, 1.0 = unchanged).

    Args:
        color: Any supported color format (name, hex, or RGB tuple).
        brightness: Multiplier from 0.0 (black) to 1.0 (unchanged).

    Returns:
        Hex color string with brightness applied.

    Example:
        ```python
        apply_brightness("coral", 0.5)   # half-bright coral
        apply_brightness("white", 0.0)   # '#000000'
        apply_brightness((255, 0, 0), 1) # '#ff0000'
        ```
    """
    brightness = max(0.0, min(1.0, brightness))
    r, g, b = Color(color).to_rgb()
    r = round(r * brightness)
    g = round(g * brightness)
    b = round(b * brightness)
    return f"#{r:02x}{g:02x}{b:02x}"


def gray(brightness: float) -> str:
    """Create a grayscale color from a brightness value.

    Shorthand for ``apply_brightness("white", brightness)``.

    Args:
        brightness: 0.0 (black) to 1.0 (white).

    Returns:
        Hex color string.

    Example:
        ```python
        gray(0.0)   # '#000000'
        gray(0.5)   # '#808080'
        gray(1.0)   # '#ffffff'
        ```
    """
    return apply_brightness("white", brightness)


def hsl(h: float, s: float = 1.0, lightness: float = 0.5) -> str:
    """Create a color from hue, saturation, and lightness.

    Args:
        h: Hue in degrees (0-360). 0 = red, 120 = green, 240 = blue.
            Values outside 0-360 wrap automatically.
        s: Saturation from 0.0 (gray) to 1.0 (vivid). Default 1.0.
        lightness: Lightness from 0.0 (black) through 0.5 (pure color)
            to 1.0 (white). Default 0.5.

    Returns:
        Hex color string.

    Example:
        ```python
        hsl(0)               # '#ff0000' — pure red
        hsl(120, 0.8, 0.5)   # saturated green
        hsl(240, 1.0, 0.3)   # dark blue
        hsl(50, 0.9, 0.55)   # warm gold
        ```
    """
    s = max(0.0, min(1.0, s))
    lightness = max(0.0, min(1.0, lightness))
    r, g, b = colorsys.hls_to_rgb(h / 360 % 1.0, lightness, s)
    return f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"


def average_color(*colors: ColorLike) -> str:
    """Return the average of one or more colors.

    Computes the mean of each RGB channel across all input colors.

    Args:
        *colors: One or more colors in any supported format
            (named, hex, or RGB tuple).

    Returns:
        Hex color string.

    Raises:
        ValueError: If no colors are provided.

    Example:
        ```python
        average_color("red", "blue")           # '#800080' — purple
        average_color("#ff0000", "green", "blue")
        average_color((255, 0, 0), (0, 255, 0))  # '#808000'
        ```
    """
    if not colors:
        raise ValueError("average_color requires at least one color")
    n = len(colors)
    total_r = total_g = total_b = 0
    for c in colors:
        r, g, b = Color(c).to_rgb()
        total_r += r
        total_g += g
        total_b += b
    return f"#{total_r // n:02x}{total_g // n:02x}{total_b // n:02x}"


def color_mix(
    color_a: ColorLike,
    color_b: ColorLike,
    t: float = 0.5,
) -> str:
    """Blend two colors together.

    Linearly interpolates each RGB channel. At *t* = 0 you get
    *color_a*, at *t* = 1 you get *color_b*, and at 0.5 an equal mix.

    Args:
        color_a: Starting color (any supported format).
        color_b: Ending color (any supported format).
        t: Blend factor from 0.0 (pure *color_a*) to 1.0 (pure *color_b*).
            Default 0.5 (equal mix).

    Returns:
        Hex color string.

    Example:
        ```python
        color_mix("red", "blue")        # '#800080' — purple
        color_mix("red", "blue", 0.0)   # '#ff0000' — pure red
        color_mix("red", "blue", 0.25)  # red-leaning purple
        color_mix("#ff8800", "navy", 0.6)
        ```
    """
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = Color(color_a).to_rgb()
    r2, g2, b2 = Color(color_b).to_rgb()
    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"
