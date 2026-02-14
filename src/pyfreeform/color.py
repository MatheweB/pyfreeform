"""Color utilities for PyDraw."""

from __future__ import annotations

from typing import ClassVar


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
    NAMED_COLORS: ClassVar[set[str]] = {
        "black",
        "white",
        "red",
        "green",
        "blue",
        "yellow",
        "cyan",
        "magenta",
        "orange",
        "purple",
        "pink",
        "brown",
        "gray",
        "grey",
        "coral",
        "crimson",
        "gold",
        "indigo",
        "lime",
        "maroon",
        "navy",
        "olive",
        "silver",
        "teal",
        "turquoise",
        "violet",
    }

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
