"""Style classes - Typed configuration for visual elements."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any


@dataclass
class DotStyle:
    """
    Configuration for dot appearance.

    Use with cell.add_dot():

        style = DotStyle(color="coral")
        cell.add_dot(radius=0.05, style=style)

    Attributes:
        color: Fill color as hex, name, or RGB tuple (default: "black")
        z_index: Layer order - higher renders on top (default: 0)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    color: str = "black"
    z_index: int = 0
    opacity: float = 1.0

    def with_color(self, color: str) -> DotStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_z_index(self, z_index: int) -> DotStyle:
        """Return new style with different z_index."""
        return replace(self, z_index=z_index)

    def with_opacity(self, opacity: float) -> DotStyle:
        """Return new style with different opacity."""
        return replace(self, opacity=opacity)

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_dot()."""
        return {"color": self.color, "z_index": self.z_index, "opacity": self.opacity}


@dataclass
class LineStyle:
    """
    Configuration for line appearance.

    Use with Line entities, connections, or cell.add_line():

        style = LineStyle(width=2, color="navy")
        cell.add_diagonal(style=style)

        # Arrow cap on one end
        style = LineStyle(width=2, end_cap="arrow")
        cell.add_line(start="left", end="right", style=style)

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
    color: str = "black"
    z_index: int = 0
    cap: str = "round"
    start_cap: str | None = None
    end_cap: str | None = None
    opacity: float = 1.0

    def with_width(self, width: float) -> LineStyle:
        """Return new style with different width."""
        return replace(self, width=width)

    def with_color(self, color: str) -> LineStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_z_index(self, z_index: int) -> LineStyle:
        """Return new style with different z_index."""
        return replace(self, z_index=z_index)

    def with_start_cap(self, start_cap: str | None) -> LineStyle:
        """Return new style with different start cap."""
        return replace(self, start_cap=start_cap)

    def with_end_cap(self, end_cap: str | None) -> LineStyle:
        """Return new style with different end cap."""
        return replace(self, end_cap=end_cap)

    def with_opacity(self, opacity: float) -> LineStyle:
        """Return new style with different opacity."""
        return replace(self, opacity=opacity)

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_line() / add_curve()."""
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
        return d


@dataclass
class FillStyle:
    """
    Configuration for filled shapes (rectangles, backgrounds).

    Use with Rect entities or cell.add_fill():

        style = FillStyle(color="blue", opacity=0.5)
        cell.add_fill(style=style)

    Attributes:
        color: Fill color (default: "black")
        opacity: Transparency 0.0-1.0 (default: 1.0, fully opaque)
        z_index: Layer order (default: 0)
    """

    color: str = "black"
    opacity: float = 1.0
    z_index: int = 0

    def with_color(self, color: str) -> FillStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_opacity(self, opacity: float) -> FillStyle:
        """Return new style with different opacity."""
        return replace(self, opacity=opacity)

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_fill()."""
        return {"color": self.color, "opacity": self.opacity, "z_index": self.z_index}


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
    color: str = "#cccccc"
    z_index: int = 0
    opacity: float = 1.0

    def with_width(self, width: float) -> BorderStyle:
        """Return new style with different width."""
        return replace(self, width=width)

    def with_color(self, color: str) -> BorderStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_opacity(self, opacity: float) -> BorderStyle:
        """Return new style with different opacity."""
        return replace(self, opacity=opacity)

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_border()."""
        return {
            "width": self.width,
            "color": self.color,
            "z_index": self.z_index,
            "opacity": self.opacity,
        }


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

    color: str = "black"
    stroke: str | None = None
    stroke_width: float = 1
    z_index: int = 0
    opacity: float = 1.0
    fill_opacity: float | None = None
    stroke_opacity: float | None = None

    def with_color(self, color: str) -> ShapeStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_stroke(self, stroke: str | None) -> ShapeStyle:
        """Return new style with different stroke."""
        return replace(self, stroke=stroke)

    def with_stroke_width(self, stroke_width: float) -> ShapeStyle:
        """Return new style with different stroke width."""
        return replace(self, stroke_width=stroke_width)

    def with_z_index(self, z_index: int) -> ShapeStyle:
        """Return new style with different z_index."""
        return replace(self, z_index=z_index)

    def with_opacity(self, opacity: float) -> ShapeStyle:
        """Return new style with different opacity (affects both fill and stroke)."""
        return replace(self, opacity=opacity)

    def with_fill_opacity(self, fill_opacity: float | None) -> ShapeStyle:
        """Return new style with different fill opacity override."""
        return replace(self, fill_opacity=fill_opacity)

    def with_stroke_opacity(self, stroke_opacity: float | None) -> ShapeStyle:
        """Return new style with different stroke opacity override."""
        return replace(self, stroke_opacity=stroke_opacity)

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

    color: str = "black"
    font_family: str = "sans-serif"
    bold: bool = False
    italic: bool = False
    text_anchor: str = "middle"
    baseline: str = "middle"
    rotation: float = 0
    z_index: int = 0
    opacity: float = 1.0

    def with_color(self, color: str) -> TextStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_font_family(self, font_family: str) -> TextStyle:
        """Return new style with different font family."""
        return replace(self, font_family=font_family)

    def with_bold(self, bold: bool = True) -> TextStyle:
        """Return new style with bold enabled/disabled."""
        return replace(self, bold=bold)

    def with_italic(self, italic: bool = True) -> TextStyle:
        """Return new style with italic enabled/disabled."""
        return replace(self, italic=italic)

    def with_z_index(self, z_index: int) -> TextStyle:
        """Return new style with different z_index."""
        return replace(self, z_index=z_index)

    def with_opacity(self, opacity: float) -> TextStyle:
        """Return new style with different opacity."""
        return replace(self, opacity=opacity)

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for add_text()."""
        return {
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


@dataclass
class ConnectionStyle:
    """
    Configuration for connections between entities.

    Use with entity.connect() or Connection():

        style = ConnectionStyle(width=2, color="red")
        dot1.connect(dot2, style=style)

        # Arrow on the end
        style = ConnectionStyle(width=2, color="red", end_cap="arrow")

    Attributes:
        width: Line width in pixels (default: 1)
        color: Line color (default: "black")
        z_index: Layer order (default: 0)
        cap: Cap style for both ends (default: "round")
        start_cap: Override cap for start end (default: None, uses cap)
        end_cap: Override cap for end end (default: None, uses cap)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    width: float = 1
    color: str = "black"
    z_index: int = 0
    cap: str = "round"
    start_cap: str | None = None
    end_cap: str | None = None
    opacity: float = 1.0

    def with_width(self, width: float) -> ConnectionStyle:
        """Return new style with different width."""
        return replace(self, width=width)

    def with_color(self, color: str) -> ConnectionStyle:
        """Return new style with different color."""
        return replace(self, color=color)

    def with_z_index(self, z_index: int) -> ConnectionStyle:
        """Return new style with different z_index."""
        return replace(self, z_index=z_index)

    def with_start_cap(self, start_cap: str | None) -> ConnectionStyle:
        """Return new style with different start cap."""
        return replace(self, start_cap=start_cap)

    def with_end_cap(self, end_cap: str | None) -> ConnectionStyle:
        """Return new style with different end cap."""
        return replace(self, end_cap=end_cap)

    def with_opacity(self, opacity: float) -> ConnectionStyle:
        """Return new style with different opacity."""
        return replace(self, opacity=opacity)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for backward compatibility with Connection internals."""
        d = {"width": self.width, "color": self.color, "z_index": self.z_index, "cap": self.cap}
        if self.start_cap is not None:
            d["start_cap"] = self.start_cap
        if self.end_cap is not None:
            d["end_cap"] = self.end_cap
        if self.opacity < 1.0:
            d["opacity"] = self.opacity
        return d

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to keyword arguments for Connection()."""
        return self.to_dict()


# Type alias for any style
AnyStyle = DotStyle | LineStyle | FillStyle | BorderStyle | ShapeStyle | TextStyle | ConnectionStyle
