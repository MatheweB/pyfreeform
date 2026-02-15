"""Style classes - Typed configuration for visual elements."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..color import Color, ColorLike
from .caps import CapName


@dataclass
class FillStyle:
    """
    Configuration for simple color fills (dots, backgrounds).

    Use with cell.add_dot() or cell.add_fill():

        style = FillStyle(color="coral")
        cell.add_dot(radius=0.05, style=style)
        cell.add_fill(style=style)

    Attributes:
        color: Fill color as hex, name, or RGB tuple (default: "black")
        z_index: Layer order - higher renders on top (default: 0)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    color: ColorLike = "black"
    z_index: int = 0
    opacity: float = 1.0
    color_brightness: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.color, tuple):
            self.color = Color(self.color).to_hex()

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_dot() / add_fill()."""
        d: dict[str, Any] = {"color": self.color, "z_index": self.z_index, "opacity": self.opacity}
        if self.color_brightness is not None:
            d["color_brightness"] = self.color_brightness
        return d


@dataclass
class PathStyle:
    """
    Configuration for lines, curves, connections, and paths.

    Use with cell.add_line(), cell.add_curve(), entity.connect(), etc.:

        style = PathStyle(width=2, color="navy")
        cell.add_diagonal(style=style)

        # Arrow cap on one end
        style = PathStyle(width=2, end_cap="arrow")
        cell.add_line(start="left", end="right", style=style)

        # Connections
        dot1.connect(dot2, style=PathStyle(width=2, color="red", end_cap="arrow"))

    Attributes:
        width: Stroke width in pixels (default: 1)
        color: Stroke color (default: "black")
        z_index: Layer order (default: 0)
        cap: Line cap style applied to both ends (default: "round")
        start_cap: Override cap for the start end (default: None, uses cap)
        end_cap: Override cap for the end end (default: None, uses cap)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    width: float = 1
    color: ColorLike = "black"
    z_index: int = 0
    cap: CapName = "round"
    start_cap: CapName | None = None
    end_cap: CapName | None = None
    opacity: float = 1.0
    color_brightness: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.color, tuple):
            self.color = Color(self.color).to_hex()

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_line() / add_curve() / Connection()."""
        d: dict[str, Any] = {
            "width": self.width,
            "color": self.color,
            "z_index": self.z_index,
            "cap": self.cap,
            "opacity": self.opacity,
        }
        if self.start_cap is not None:
            d["start_cap"] = self.start_cap
        if self.end_cap is not None:
            d["end_cap"] = self.end_cap
        if self.color_brightness is not None:
            d["color_brightness"] = self.color_brightness
        return d


@dataclass
class BorderStyle:
    """
    Configuration for borders and outlines.

    Use with cell.add_border():

        style = BorderStyle(width=1, color="gray")
        cell.add_border(style=style)

    Attributes:
        width: Stroke width in pixels (default: 0.5)
        color: Stroke color (default: "#cccccc")
        z_index: Layer order (default: 0)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    width: float = 0.5
    color: ColorLike = "#cccccc"
    z_index: int = 0
    opacity: float = 1.0
    color_brightness: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.color, tuple):
            self.color = Color(self.color).to_hex()

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_border()."""
        d: dict[str, Any] = {
            "width": self.width,
            "color": self.color,
            "z_index": self.z_index,
            "opacity": self.opacity,
        }
        if self.color_brightness is not None:
            d["color_brightness"] = self.color_brightness
        return d


@dataclass
class ShapeStyle:
    """
    Configuration for filled shapes (Rect, Ellipse, Polygon).

    Use with cell.add_ellipse() or cell.add_polygon():

        style = ShapeStyle(color="coral", stroke="navy", stroke_width=2)
        cell.add_ellipse(style=style)
        cell.add_polygon(Polygon.hexagon(), style=style)

    Note: ``color`` maps to ``fill`` at the entity level.

    Attributes:
        color: Fill color (default: "black")
        stroke: Stroke color (default: None for no stroke)
        stroke_width: Stroke width in pixels (default: 1)
        z_index: Layer order (default: 0)
        opacity: Opacity for both fill and stroke 0.0-1.0 (default: 1.0)
        fill_opacity: Override opacity for fill only (default: None, uses opacity)
        stroke_opacity: Override opacity for stroke only (default: None, uses opacity)
    """

    color: ColorLike = "black"
    stroke: ColorLike | None = None
    stroke_width: float = 1
    z_index: int = 0
    opacity: float = 1.0
    fill_opacity: float | None = None
    stroke_opacity: float | None = None
    fill_brightness: float | None = None
    stroke_brightness: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.color, tuple):
            self.color = Color(self.color).to_hex()
        if isinstance(self.stroke, tuple):
            self.stroke = Color(self.stroke).to_hex()

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_ellipse() / add_polygon() / add_rect()."""
        d: dict[str, Any] = {
            "fill": self.color,
            "stroke": self.stroke,
            "stroke_width": self.stroke_width,
            "z_index": self.z_index,
            "opacity": self.opacity,
        }
        if self.fill_opacity is not None:
            d["fill_opacity"] = self.fill_opacity
        if self.stroke_opacity is not None:
            d["stroke_opacity"] = self.stroke_opacity
        if self.fill_brightness is not None:
            d["fill_brightness"] = self.fill_brightness
        if self.stroke_brightness is not None:
            d["stroke_brightness"] = self.stroke_brightness
        return d


@dataclass
class TextStyle:
    """
    Configuration for text appearance.

    Use with cell.add_text():

        style = TextStyle(color="navy", bold=True)
        cell.add_text("Hello", font_size=0.20, style=style)

    Attributes:
        color: Text color (default: "black")
        font_family: Font family (default: "sans-serif")
        bold: Bold text (default: False)
        italic: Italic text (default: False)
        text_anchor: Horizontal alignment (default: "middle")
        baseline: Vertical alignment (default: "middle")
        rotation: Rotation in degrees (default: 0)
        z_index: Layer order (default: 0)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    color: ColorLike = "black"
    font_family: str = "sans-serif"
    bold: bool = False
    italic: bool = False
    text_anchor: str = "middle"
    baseline: str = "middle"
    rotation: float = 0
    z_index: int = 0
    opacity: float = 1.0
    color_brightness: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.color, tuple):
            self.color = Color(self.color).to_hex()

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_text()."""
        d: dict[str, Any] = {
            "color": self.color,
            "font_family": self.font_family,
            "bold": self.bold,
            "italic": self.italic,
            "text_anchor": self.text_anchor,
            "baseline": self.baseline,
            "rotation": self.rotation,
            "z_index": self.z_index,
            "opacity": self.opacity,
        }
        if self.color_brightness is not None:
            d["color_brightness"] = self.color_brightness
        return d


# Type alias for any style
AnyStyle = FillStyle | PathStyle | BorderStyle | ShapeStyle | TextStyle
