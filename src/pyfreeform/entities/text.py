"""Text - A text label entity."""

from __future__ import annotations

import functools

from PIL import ImageFont

from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike

# ---------------------------------------------------------------------------
# Font measurement via Pillow
# ---------------------------------------------------------------------------

_HEURISTIC_CHAR_WIDTH = 0.6
_REFERENCE_FONT_SIZE = 100

# Map generic CSS families → concrete font names to try
_GENERIC_FAMILIES: dict[str, list[str]] = {
    "sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "serif": ["Times", "Times New Roman", "DejaVu Serif"],
    "monospace": ["Menlo", "Courier New", "DejaVu Sans Mono", "Courier"],
}


@functools.lru_cache(maxsize=64)
def _load_font(
    family: str,
    weight: str | int = "normal",
    style: str = "normal",
) -> ImageFont.FreeTypeFont | None:
    """Load font at reference size. Advance widths scale linearly with size."""
    is_bold = weight in ("bold", 700, 800, 900) or (
        isinstance(weight, (int, float)) and weight >= 700
    )
    is_italic = style in ("italic", "oblique")

    if is_bold and is_italic:
        suffixes = [" Bold Italic", " Bold Oblique", ""]
    elif is_bold:
        suffixes = [" Bold", ""]
    elif is_italic:
        suffixes = [" Italic", " Oblique", ""]
    else:
        suffixes = [""]

    concrete_names = [family] + _GENERIC_FAMILIES.get(family, [])

    for name in concrete_names:
        for suffix in suffixes:
            try:
                return ImageFont.truetype(name + suffix, _REFERENCE_FONT_SIZE)
            except (OSError, IOError):
                continue

    return None


def _measure_text_width(
    content: str,
    font_size: float,
    font_family: str,
    font_weight: str | int = "normal",
    font_style: str = "normal",
) -> float:
    """Measure text width in pixels using Pillow, with heuristic fallback."""
    if not content:
        return 0.0

    font = _load_font(font_family, font_weight, font_style)
    if font is not None:
        ref_width = font.getlength(content)
        return ref_width * (font_size / _REFERENCE_FONT_SIZE)

    return len(content) * font_size * _HEURISTIC_CHAR_WIDTH


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
        opacity: float = 1.0,
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
        self._pixel_font_size = float(font_size)
        self._relative_font_size: float | None = None
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
        self.opacity = float(opacity)
        self._textpath_info: dict | None = None

    @property
    def font_size(self) -> float:
        """Font size in pixels (resolved from relative fraction if set)."""
        if self._relative_font_size is not None:
            resolved = self._resolve_size(self._relative_font_size, "height")
            if resolved is not None:
                return resolved
        return self._pixel_font_size

    @font_size.setter
    def font_size(self, value: float) -> None:
        self._pixel_font_size = float(value)
        self._relative_font_size = None

    def _to_pixel_mode(self) -> None:
        """Resolve font size and position to pixels."""
        if self._relative_font_size is not None:
            self._pixel_font_size = self.font_size
            self._relative_font_size = None
        super()._to_pixel_mode()

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

    def anchor(self, name: str = "center") -> Coord:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        raise ValueError(f"Text has no anchor '{name}'. Available: {self.anchor_names}")

    def bounds(self) -> tuple[float, float, float, float]:
        """
        Get bounding box using Pillow font metrics for width
        and font_size for height.
        """
        text_width = _measure_text_width(
            self.content, self.font_size, self.font_family,
            self.font_weight, self.font_style,
        )
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

    def fit_to_cell(self, fraction: float = 1.0) -> Text:
        """
        Scale font size so text fills its cell at *fraction*.

        Unlike ``fit=True`` on ``add_text()`` (which only shrinks),
        this method scales the font **up or down** to fill the
        available space — matching :meth:`EntityGroup.fit_to_cell`.

        Args:
            fraction: How much of the cell to fill (0.0–1.0).
                      1.0 = fill entire cell, 0.8 = use 80%.

        Returns:
            self, for method chaining.

        Raises:
            ValueError: If entity has no cell.
        """
        if self._cell is None:
            raise ValueError("Cannot fit to cell: text has no cell")

        cell = self._cell
        cell_w, cell_h = cell.width * fraction, cell.height * fraction

        # Compute the font size that fits both dimensions
        width_at_1px = _measure_text_width(
            self.content, 1.0, self.font_family,
            self.font_weight, self.font_style,
        )
        max_from_height = cell_h
        max_from_width = cell_w / width_at_1px if width_at_1px > 0 else max_from_height
        new_font_size = min(max_from_width, max_from_height)

        self._pixel_font_size = new_font_size
        if cell_h > 0:
            self._relative_font_size = new_font_size / cell_h * fraction
        return self

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Text:
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
                origin = Coord(*origin)
            if origin != self.position:
                super().rotate(angle, origin)

        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Text:
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

    def set_textpath(
        self,
        path_id: str,
        path_d: str,
        start_offset: str = "0%",
        text_length: float | None = None,
    ) -> None:
        """
        Configure this text to warp along an SVG path.

        Args:
            path_id: Unique ID for the path definition.
            path_d: SVG path ``d`` attribute string.
            start_offset: Offset along the path where text starts.
            text_length: If set, the SVG ``textLength`` attribute that
                stretches or compresses text to span this many pixels.
        """
        self._textpath_info = {
            "path_id": path_id,
            "path_d": path_d,
            "start_offset": start_offset,
            "text_length": text_length,
        }

    def get_required_paths(self) -> list[tuple[str, str]]:
        """
        Collect SVG path definitions needed by this text's textPath.

        Returns:
            List of (path_id, path_svg) tuples.
        """
        if self._textpath_info is None:
            return []
        info = self._textpath_info
        path_svg = f'<path id="{info["path_id"]}" d="{info["path_d"]}" fill="none" />'
        return [(info["path_id"], path_svg)]

    def to_svg(self) -> str:
        """Render to SVG text element."""
        if self._textpath_info is not None:
            return self._to_svg_textpath()
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

        opacity_attr = f' opacity="{self.opacity}"' if self.opacity < 1.0 else ''

        return (
            f'<text x="{self.x}" y="{self.y}" '
            f'font-size="{self.font_size}" '
            f'font-family="{self.font_family}" '
            f'font-style="{self.font_style}" '
            f'font-weight="{self.font_weight}" '
            f'fill="{self.color}" '
            f'text-anchor="{self.text_anchor}" '
            f'dominant-baseline="{self.baseline}"'
            f'{opacity_attr}'
            f'{transform}>'
            f'{escaped_content}'
            f'</text>'
        )

    def _to_svg_textpath(self) -> str:
        """Render to SVG text element with textPath warping."""
        info = self._textpath_info

        escaped_content = (
            self.content
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

        opacity_attr = f' opacity="{self.opacity}"' if self.opacity < 1.0 else ''

        offset = info["start_offset"]
        offset_attr = f' startOffset="{offset}"' if offset not in ("0%", "0.0%") else ''

        text_len = info.get("text_length")
        textlen_attr = (
            f' textLength="{text_len:.1f}"'
            f' lengthAdjust="spacing"'
            if text_len else ''
        )

        return (
            f'<text font-size="{self.font_size}" '
            f'font-family="{self.font_family}" '
            f'font-style="{self.font_style}" '
            f'font-weight="{self.font_weight}" '
            f'fill="{self.color}" '
            f'text-anchor="{self.text_anchor}" '
            f'dominant-baseline="{self.baseline}"'
            f'{opacity_attr}>'
            f'<textPath href="#{info["path_id"]}"'
            f'{offset_attr}{textlen_attr}>'
            f'{escaped_content}'
            f'</textPath></text>'
        )

    def __repr__(self) -> str:
        return (
            f"Text({self.x}, {self.y}, {self.content!r}, "
            f"font_size={self.font_size}, color={self.color!r})"
        )
