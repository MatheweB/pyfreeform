"""Text - A text label entity."""

from __future__ import annotations

from ..color import Color
from ..core.entity import Entity
from ..core.point import Point


class Text(Entity):
    """
    A text label at a specific position.

    Text can be used for labels, annotations, data visualization,
    and typographic art. It supports:
    - Multiple font families (serif, sans-serif, monospace)
    - Alignment control (horizontal and vertical)
    - Rotation around the text position
    - Color and size customization

    Attributes:
        position: The anchor point for the text
        content: The text string to display
        font_size: Font size in pixels
        font_family: Font family name
        font_style: normal | italic | oblique
        font_weight: normal | bold | 100–900
        color: Text color
        anchor: Horizontal alignment (start, middle, end)
        baseline: Vertical alignment (auto, middle, hanging, etc.)
        rotation: Rotation angle in degrees

    Anchors:
        - "center": The text position (same as position)

    Examples:
        >>> text = Text(100, 100, "Hello")
        >>> text = Text(100, 100, "Label", font_size=16, color="coral")
        >>> text.rotate(45)
    """

    DEFAULT_FONT_SIZE = 16
    DEFAULT_FONT_FAMILY = "sans-serif"
    DEFAULT_COLOR = "black"
    DEFAULT_ANCHOR = "middle"
    DEFAULT_BASELINE = "middle"
    DEFAULT_FONT_STYLE = "normal"
    DEFAULT_FONT_WEIGHT = "normal"

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        content: str = "",
        font_size: float = DEFAULT_FONT_SIZE,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        font_family: str = DEFAULT_FONT_FAMILY,
        font_style: str = DEFAULT_FONT_STYLE,
        font_weight: str | int = DEFAULT_FONT_WEIGHT,
        bold: bool = False,      # NEW (sugar)
        italic: bool = False,    # NEW (sugar)
        text_anchor: str = DEFAULT_ANCHOR,
        baseline: str = DEFAULT_BASELINE,
        rotation: float = 0,
        z_index: int = 0,
    ) -> None:
        """
        Create text at the specified position.

        Args:
            x: Horizontal position.
            y: Vertical position.
            content: The text string to display.
            font_size: Font size in pixels.
            color: Text color (name, hex, or RGB tuple).
            font_family: Font family - "serif", "sans-serif", "monospace",
                        or a specific font name.
            text_anchor: Horizontal alignment: "start" (left), "middle", "end" (right).
            baseline: Vertical alignment: "auto", "middle", "hanging" (top),
                     "alphabetic", "ideographic", "text-before-edge", "text-after-edge".
            rotation: Rotation angle in degrees (counterclockwise).
            z_index: Layer ordering (higher = on top).
        """
        super().__init__(x, y, z_index)
        self.content = content
        self.font_size = float(font_size)
        self._color = Color(color)
        self.font_family = font_family

        if bold and font_weight == self.DEFAULT_FONT_WEIGHT:
            font_weight = "bold"

        if italic and font_style == self.DEFAULT_FONT_STYLE:
            font_style = "italic"

        self.font_style = font_style
        self.font_weight = font_weight


        self.text_anchor = text_anchor
        self.baseline = baseline
        self.rotation = float(rotation)

    @property
    def color(self) -> str:
        """The text color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def bold(self) -> bool:
        return self.font_weight in ("bold", 700, 800, 900)

    @bold.setter
    def bold(self, value: bool) -> None:
        self.font_weight = "bold" if value else "normal"


    @property
    def italic(self) -> bool:
        return self.font_style == "italic"

    @italic.setter
    def italic(self, value: bool) -> None:
        self.font_style = "italic" if value else "normal"

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors: just 'center' for text."""
        return ["center"]

    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        raise ValueError(f"Text has no anchor '{name}'. Available: {self.anchor_names}")

    def bounds(self) -> tuple[float, float, float, float]:
        """
        Get approximate bounding box.

        Note: This is an approximation since we don't have access to
        actual text metrics. Assumes roughly 0.6 * font_size per character
        width and font_size for height.
        """
        # Rough approximation of text dimensions
        char_width = self.font_size * 0.6
        text_width = len(self.content) * char_width
        text_height = self.font_size

        # Adjust based on text_anchor
        if self.text_anchor == "start":
            x_offset = 0
        elif self.text_anchor == "middle":
            x_offset = -text_width / 2
        else:  # end
            x_offset = -text_width

        # Adjust based on baseline
        if self.baseline in ("middle", "central"):
            y_offset = -text_height / 2
        elif self.baseline == "hanging":
            y_offset = 0
        else:  # alphabetic, auto, etc.
            y_offset = -text_height * 0.75

        return (
            self.x + x_offset,
            self.y + y_offset,
            self.x + x_offset + text_width,
            self.y + y_offset + text_height,
        )

    def rotate(self, angle: float, origin: Point | tuple[float, float] | None = None) -> Text:
        """
        Rotate the text around a point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: text position).

        Returns:
            self, for method chaining.
        """
        # Update the rotation angle
        self.rotation += angle

        # If origin is specified and different from position, also move the position
        if origin is not None:
            if isinstance(origin, tuple):
                origin = Point(*origin)
            if origin != self.position:
                super().rotate(angle, origin)

        return self

    def scale(self, factor: float, origin: Point | tuple[float, float] | None = None) -> Text:
        """
        Scale the text (changes font size and optionally position).

        Args:
            factor: Scale factor (2.0 = double the font size).
            origin: If provided, also moves position away from origin.

        Returns:
            self, for method chaining.
        """
        self.font_size *= factor

        if origin is not None:
            # Also scale position relative to origin
            super().scale(factor, origin)

        return self

    def to_svg(self) -> str:
        """Render to SVG text element."""
        # Build transform attribute if rotation is applied
        transform = ""
        if self.rotation != 0:
            transform = f' transform="rotate({self.rotation} {self.x} {self.y})"'

        # Escape special XML characters in content
        escaped_content = (
            self.content
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

        return (
            f'<text x="{self.x}" y="{self.y}" '
            f'font-size="{self.font_size}" '
            f'font-family="{self.font_family}" '
            f'font-style="{self.font_style}" '
            f'font-weight="{self.font_weight}" '
            f'fill="{self.color}" '
            f'text-anchor="{self.text_anchor}" '
            f'dominant-baseline="{self.baseline}"'
            f'{transform}>'
            f'{escaped_content}'
            f'</text>'
        )

    def __repr__(self) -> str:
        return (
            f"Text({self.x}, {self.y}, {self.content!r}, "
            f"font_size={self.font_size}, color={self.color!r})"
        )
