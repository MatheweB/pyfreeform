"""Text - A text label entity."""

from __future__ import annotations

import functools

from PIL import ImageFont

from ..color import Color, apply_brightness
from ..core.relcoord import RelCoordLike
from ..core.coord import Coord
from ..core.entity import Entity
from ..core.svg_utils import opacity_attr, xml_escape

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
        isinstance(weight, int | float) and weight >= 700
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

    concrete_names = [family, *_GENERIC_FAMILIES.get(family, [])]

    for name in concrete_names:
        for suffix in suffixes:
            font = _try_truetype(name + suffix)
            if font is not None:
                return font

    return None


def _try_truetype(full_name: str) -> ImageFont.FreeTypeFont | None:
    """Try loading a TrueType font, returning None on failure."""
    try:
        return ImageFont.truetype(full_name, _REFERENCE_FONT_SIZE)
    except OSError:
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
        font_weight: normal | bold | 100-900
        color: Text color
        anchor: Horizontal alignment (start, middle, end)
        baseline: Vertical alignment (auto, middle, hanging, etc.)
        rotation: Rotation angle in degrees

    Anchors:
        - "center": The text position (same as position)

    Example:
        ```python
        text = Text(100, 100, "Hello")
        text = Text(100, 100, "Label", font_size=16, color="coral")
        text.rotate(45)
        ```
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
        bold: bool = False,
        italic: bool = False,
        text_anchor: str = DEFAULT_ANCHOR,
        baseline: str = DEFAULT_BASELINE,
        rotation: float = 0,
        z_index: int = 0,
        opacity: float = 1.0,
        color_brightness: float | None = None,
    ) -> None:
        """
        Create text at the specified position.

        Args:
            x: Horizontal position.
            y: Vertical position.
            content: The text string to display.
            font_size: Font size in pixels.
            color: Text color (name, hex, or RGB tuple).
            font_family: Font family — "serif", "sans-serif", "monospace",
                        or a specific font name.
            bold: If True, use bold weight.
            italic: If True, use italic style.
            text_anchor: Horizontal alignment: "start" (left), "middle", "end" (right).
            baseline: Vertical alignment: "auto", "middle", "hanging" (top).
            rotation: Rotation angle in degrees (counterclockwise).
            z_index: Layer ordering (higher = on top).
            opacity: Opacity (0.0 transparent to 1.0 opaque).
            color_brightness: Brightness multiplier 0.0 (black) to 1.0 (unchanged).
        """
        super().__init__(x, y, z_index)
        self.content = content
        self._pixel_font_size = float(font_size)
        self._relative_font_size: float | None = None
        if color_brightness is not None:
            color = apply_brightness(color, color_brightness)
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
    def relative_font_size(self) -> float | None:
        """Relative font size (fraction of surface height), or None."""
        return self._relative_font_size

    @relative_font_size.setter
    def relative_font_size(self, value: float | None) -> None:
        self._relative_font_size = value

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

    def _has_relative_properties(self) -> bool:
        return super()._has_relative_properties() or self._relative_font_size is not None

    def _resolve_to_absolute(self) -> None:
        """Resolve relative font size and position to absolute values."""
        if self._relative_font_size is not None:
            self._pixel_font_size = self.font_size
            self._relative_font_size = None
        super()._resolve_to_absolute()

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

    def _named_anchor(self, name: str) -> Coord:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        raise ValueError(f"Text has no anchor '{name}'. Available: {self.anchor_names}")

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """
        Get bounding box using Pillow font metrics for width
        and font_size for height (accounts for scale).
        """
        s = self._scale_factor
        text_width = (
            _measure_text_width(
                self.content,
                self.font_size,
                self.font_family,
                self.font_weight,
                self.font_style,
            )
            * s
        )
        text_height = self.font_size * s

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

    def fit_to_cell(
        self,
        scale: float = 1.0,
        recenter: bool = True,
        *,
        at: RelCoordLike | None = None,
        visual: bool = True,
        rotate: bool = False,
        match_aspect: bool = False,
    ) -> Text:
        """
        Scale font size so text fills its cell at *scale*.

        Unlike ``fit=True`` on ``add_text()`` (which only shrinks),
        this method scales the font **up or down** to fill the
        available space.

        Args:
            scale:  How much of the cell to fill (0.0-1.0).
                    1.0 = fill entire cell, 0.8 = use 80%.
            recenter: If True, center text in cell after scaling.
            at: Optional cell-relative position (rx, ry).
            visual: Unused for text (kept for signature compatibility).
            rotate: If True, rotate to maximize fill before scaling.
            match_aspect: If True, rotate to match cell aspect ratio.

        Returns:
            self, for method chaining.

        Raises:
            ValueError: If entity has no cell.
        """
        if self._cell is None:
            raise ValueError("Cannot fit to cell: text has no cell")

        if rotate and match_aspect:
            raise ValueError("rotate and match_aspect are mutually exclusive")

        # Apply fitting rotation if requested
        if rotate or match_aspect:
            b = self.bounds(visual=True)
            w, h = b[2] - b[0], b[3] - b[1]
            cell = self._cell
            if w > 1e-9 and h > 1e-9:
                avail_w = cell.width * scale
                avail_h = cell.height * scale
                angle = (
                    Entity._compute_optimal_angle(w, h, avail_w, avail_h)
                    if rotate
                    else Entity._compute_aspect_match_angle(w, h, avail_w, avail_h)
                )
                self.rotate(angle)

        cell = self._cell
        cell_w, cell_h = cell.width * scale, cell.height * scale

        # Compute the font size that fits both dimensions
        width_at_1px = _measure_text_width(
            self.content,
            1.0,
            self.font_family,
            self.font_weight,
            self.font_style,
        )
        max_from_height = cell_h
        max_from_width = cell_w / width_at_1px if width_at_1px > 0 else max_from_height
        new_font_size = min(max_from_width, max_from_height)

        self._pixel_font_size = new_font_size
        if cell_h > 0:
            self._relative_font_size = new_font_size / cell_h * scale
        return self

    @property
    def has_textpath(self) -> bool:
        """Whether this text renders along a path (textPath mode)."""
        return self._textpath_info is not None

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
            return self._to_svg_textpath(self._textpath_info)

        escaped = xml_escape(self.content)

        return (
            f'<text x="{self.x}" y="{self.y}" '
            f'font-size="{self.font_size}" '
            f'font-family="{self.font_family}" '
            f'font-style="{self.font_style}" '
            f'font-weight="{self.font_weight}" '
            f'fill="{self.color}" '
            f'text-anchor="{self.text_anchor}" '
            f'dominant-baseline="{self.baseline}"'
            f"{opacity_attr(self.opacity)}"
            f"{self._build_svg_transform()}>"
            f"{escaped}"
            f"</text>"
        )

    def _to_svg_textpath(self, info: dict[str, object]) -> str:
        """Render to SVG text element with textPath warping."""
        escaped = xml_escape(self.content)

        offset = info["start_offset"]
        offset_attr = f' startOffset="{offset}"' if offset not in ("0%", "0.0%") else ""

        text_len = info.get("text_length")
        textlen_attr = f' textLength="{text_len:.1f}" lengthAdjust="spacing"' if text_len else ""

        return (
            f'<text font-size="{self.font_size}" '
            f'font-family="{self.font_family}" '
            f'font-style="{self.font_style}" '
            f'font-weight="{self.font_weight}" '
            f'fill="{self.color}" '
            f'text-anchor="{self.text_anchor}" '
            f'dominant-baseline="{self.baseline}"'
            f"{opacity_attr(self.opacity)}>"
            f'<textPath href="#{info["path_id"]}"'
            f"{offset_attr}{textlen_attr}>"
            f"{escaped}"
            f"</textPath></text>"
        )

    def __repr__(self) -> str:
        return (
            f"Text({self.x}, {self.y}, {self.content!r}, "
            f"font_size={self.font_size}, color={self.color!r})"
        )
