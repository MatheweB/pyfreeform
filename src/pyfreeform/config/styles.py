"""Style classes - Typed configuration for visual elements."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class DotStyle:
    """
    Configuration for dot appearance.

    Use with Dot entities or cell.add_dot():

        style = DotStyle(radius=5, color="coral")
        cell.add_dot(style=style)

        # Or inline
        cell.add_dot(radius=5, color="coral")

    Attributes:
        radius: Dot radius in pixels (default: 5)
        color: Fill color as hex, name, or RGB tuple (default: "black")
        z_index: Layer order - higher renders on top (default: 0)
        opacity: Opacity 0.0-1.0 (default: 1.0, fully opaque)
    """

    radius: float = 5
    color: str = "black"
    z_index: int = 0
    opacity: float = 1.0

    def with_radius(self, radius: float) -> DotStyle:
        """Return new style with different radius."""
        return DotStyle(radius=radius, color=self.color, z_index=self.z_index, opacity=self.opacity)

    def with_color(self, color: str) -> DotStyle:
        """Return new style with different color."""
        return DotStyle(radius=self.radius, color=color, z_index=self.z_index, opacity=self.opacity)

    def with_z_index(self, z_index: int) -> DotStyle:
        """Return new style with different z_index."""
        return DotStyle(radius=self.radius, color=self.color, z_index=z_index, opacity=self.opacity)

    def with_opacity(self, opacity: float) -> DotStyle:
        """Return new style with different opacity."""
        return DotStyle(radius=self.radius, color=self.color, z_index=self.z_index, opacity=opacity)


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
        return LineStyle(width=width, color=self.color, z_index=self.z_index,
                         cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                         opacity=self.opacity)

    def with_color(self, color: str) -> LineStyle:
        """Return new style with different color."""
        return LineStyle(width=self.width, color=color, z_index=self.z_index,
                         cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                         opacity=self.opacity)

    def with_z_index(self, z_index: int) -> LineStyle:
        """Return new style with different z_index."""
        return LineStyle(width=self.width, color=self.color, z_index=z_index,
                         cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                         opacity=self.opacity)

    def with_start_cap(self, start_cap: str | None) -> LineStyle:
        """Return new style with different start cap."""
        return LineStyle(width=self.width, color=self.color, z_index=self.z_index,
                         cap=self.cap, start_cap=start_cap, end_cap=self.end_cap,
                         opacity=self.opacity)

    def with_end_cap(self, end_cap: str | None) -> LineStyle:
        """Return new style with different end cap."""
        return LineStyle(width=self.width, color=self.color, z_index=self.z_index,
                         cap=self.cap, start_cap=self.start_cap, end_cap=end_cap,
                         opacity=self.opacity)

    def with_opacity(self, opacity: float) -> LineStyle:
        """Return new style with different opacity."""
        return LineStyle(width=self.width, color=self.color, z_index=self.z_index,
                         cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                         opacity=opacity)


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
        return FillStyle(color=color, opacity=self.opacity, z_index=self.z_index)

    def with_opacity(self, opacity: float) -> FillStyle:
        """Return new style with different opacity."""
        return FillStyle(color=self.color, opacity=opacity, z_index=self.z_index)


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
        return BorderStyle(width=width, color=self.color, z_index=self.z_index, opacity=self.opacity)

    def with_color(self, color: str) -> BorderStyle:
        """Return new style with different color."""
        return BorderStyle(width=self.width, color=color, z_index=self.z_index, opacity=self.opacity)

    def with_opacity(self, opacity: float) -> BorderStyle:
        """Return new style with different opacity."""
        return BorderStyle(width=self.width, color=self.color, z_index=self.z_index, opacity=opacity)


@dataclass
class ShapeStyle:
    """
    Configuration for filled shapes (Rect, Ellipse, Polygon).

    Use with cell.add_ellipse() or cell.add_polygon():

        style = ShapeStyle(color="coral", stroke="navy", stroke_width=2)
        cell.add_ellipse(style=style)
        cell.add_polygon(shapes.hexagon(), style=style)

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
        return ShapeStyle(color=color, stroke=self.stroke, stroke_width=self.stroke_width,
                          z_index=self.z_index, opacity=self.opacity,
                          fill_opacity=self.fill_opacity, stroke_opacity=self.stroke_opacity)

    def with_stroke(self, stroke: str | None) -> ShapeStyle:
        """Return new style with different stroke."""
        return ShapeStyle(color=self.color, stroke=stroke, stroke_width=self.stroke_width,
                          z_index=self.z_index, opacity=self.opacity,
                          fill_opacity=self.fill_opacity, stroke_opacity=self.stroke_opacity)

    def with_stroke_width(self, stroke_width: float) -> ShapeStyle:
        """Return new style with different stroke width."""
        return ShapeStyle(color=self.color, stroke=self.stroke, stroke_width=stroke_width,
                          z_index=self.z_index, opacity=self.opacity,
                          fill_opacity=self.fill_opacity, stroke_opacity=self.stroke_opacity)

    def with_z_index(self, z_index: int) -> ShapeStyle:
        """Return new style with different z_index."""
        return ShapeStyle(color=self.color, stroke=self.stroke, stroke_width=self.stroke_width,
                          z_index=z_index, opacity=self.opacity,
                          fill_opacity=self.fill_opacity, stroke_opacity=self.stroke_opacity)

    def with_opacity(self, opacity: float) -> ShapeStyle:
        """Return new style with different opacity (affects both fill and stroke)."""
        return ShapeStyle(color=self.color, stroke=self.stroke, stroke_width=self.stroke_width,
                          z_index=self.z_index, opacity=opacity,
                          fill_opacity=self.fill_opacity, stroke_opacity=self.stroke_opacity)

    def with_fill_opacity(self, fill_opacity: float | None) -> ShapeStyle:
        """Return new style with different fill opacity override."""
        return ShapeStyle(color=self.color, stroke=self.stroke, stroke_width=self.stroke_width,
                          z_index=self.z_index, opacity=self.opacity,
                          fill_opacity=fill_opacity, stroke_opacity=self.stroke_opacity)

    def with_stroke_opacity(self, stroke_opacity: float | None) -> ShapeStyle:
        """Return new style with different stroke opacity override."""
        return ShapeStyle(color=self.color, stroke=self.stroke, stroke_width=self.stroke_width,
                          z_index=self.z_index, opacity=self.opacity,
                          fill_opacity=self.fill_opacity, stroke_opacity=stroke_opacity)


@dataclass
class TextStyle:
    """
    Configuration for text appearance.

    Use with cell.add_text():

        style = TextStyle(font_size=12, color="navy", bold=True)
        cell.add_text("Hello", style=style)

    Attributes:
        font_size: Font size in pixels (default: 16)
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

    font_size: float = 16
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
        return TextStyle(font_size=self.font_size, color=color, font_family=self.font_family,
                         bold=self.bold, italic=self.italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=self.z_index,
                         opacity=self.opacity)

    def with_font_size(self, font_size: float) -> TextStyle:
        """Return new style with different font size."""
        return TextStyle(font_size=font_size, color=self.color, font_family=self.font_family,
                         bold=self.bold, italic=self.italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=self.z_index,
                         opacity=self.opacity)

    def with_font_family(self, font_family: str) -> TextStyle:
        """Return new style with different font family."""
        return TextStyle(font_size=self.font_size, color=self.color, font_family=font_family,
                         bold=self.bold, italic=self.italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=self.z_index,
                         opacity=self.opacity)

    def with_bold(self, bold: bool = True) -> TextStyle:
        """Return new style with bold enabled/disabled."""
        return TextStyle(font_size=self.font_size, color=self.color, font_family=self.font_family,
                         bold=bold, italic=self.italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=self.z_index,
                         opacity=self.opacity)

    def with_italic(self, italic: bool = True) -> TextStyle:
        """Return new style with italic enabled/disabled."""
        return TextStyle(font_size=self.font_size, color=self.color, font_family=self.font_family,
                         bold=self.bold, italic=italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=self.z_index,
                         opacity=self.opacity)

    def with_z_index(self, z_index: int) -> TextStyle:
        """Return new style with different z_index."""
        return TextStyle(font_size=self.font_size, color=self.color, font_family=self.font_family,
                         bold=self.bold, italic=self.italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=z_index,
                         opacity=self.opacity)

    def with_opacity(self, opacity: float) -> TextStyle:
        """Return new style with different opacity."""
        return TextStyle(font_size=self.font_size, color=self.color, font_family=self.font_family,
                         bold=self.bold, italic=self.italic, text_anchor=self.text_anchor,
                         baseline=self.baseline, rotation=self.rotation, z_index=self.z_index,
                         opacity=opacity)


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
        return ConnectionStyle(width=width, color=self.color, z_index=self.z_index,
                               cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                               opacity=self.opacity)

    def with_color(self, color: str) -> ConnectionStyle:
        """Return new style with different color."""
        return ConnectionStyle(width=self.width, color=color, z_index=self.z_index,
                               cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                               opacity=self.opacity)

    def with_z_index(self, z_index: int) -> ConnectionStyle:
        """Return new style with different z_index."""
        return ConnectionStyle(width=self.width, color=self.color, z_index=z_index,
                               cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                               opacity=self.opacity)

    def with_start_cap(self, start_cap: str | None) -> ConnectionStyle:
        """Return new style with different start cap."""
        return ConnectionStyle(width=self.width, color=self.color, z_index=self.z_index,
                               cap=self.cap, start_cap=start_cap, end_cap=self.end_cap,
                               opacity=self.opacity)

    def with_end_cap(self, end_cap: str | None) -> ConnectionStyle:
        """Return new style with different end cap."""
        return ConnectionStyle(width=self.width, color=self.color, z_index=self.z_index,
                               cap=self.cap, start_cap=self.start_cap, end_cap=end_cap,
                               opacity=self.opacity)

    def with_opacity(self, opacity: float) -> ConnectionStyle:
        """Return new style with different opacity."""
        return ConnectionStyle(width=self.width, color=self.color, z_index=self.z_index,
                               cap=self.cap, start_cap=self.start_cap, end_cap=self.end_cap,
                               opacity=opacity)

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


# Type alias for any style
AnyStyle = DotStyle | LineStyle | FillStyle | BorderStyle | ShapeStyle | TextStyle | ConnectionStyle
