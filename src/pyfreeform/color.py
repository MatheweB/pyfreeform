"""Color utilities for PyFreeform."""

from __future__ import annotations

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
