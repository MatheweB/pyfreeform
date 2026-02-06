"""Rect - A rectangle entity."""

from __future__ import annotations

from ..color import Color
from ..core.entity import Entity
from ..core.point import Point


class Rect(Entity):
    """
    A rectangle entity.
    
    Rectangles can be used for backgrounds, cells, frames, and more.
    When placed in a cell, they can automatically fill the cell.
    
    Attributes:
        position: Top-left corner of the rectangle
        width: Rectangle width
        height: Rectangle height
        fill: Fill color (or None for no fill)
        stroke: Stroke color (or None for no stroke)
        stroke_width: Stroke width
    
    Anchors:
        - "center": Center point
        - "top_left", "top_right", "bottom_left", "bottom_right": Corners
        - "top", "bottom", "left", "right": Edge centers
    
    Examples:
        >>> rect = Rect(0, 0, 100, 50, fill="blue")
        >>> rect = Rect(0, 0, 100, 50, fill=None, stroke="black", stroke_width=2)
    """
    
    DEFAULT_FILL = "black"
    
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        fill: str | tuple[int, int, int] | None = DEFAULT_FILL,
        stroke: str | tuple[int, int, int] | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
    ) -> None:
        """
        Create a rectangle.

        Args:
            x, y: Top-left corner position.
            width: Rectangle width.
            height: Rectangle height.
            fill: Fill color (None for transparent).
            stroke: Stroke color (None for no stroke).
            stroke_width: Stroke width in pixels.
            z_index: Layer ordering (higher = on top).
            opacity: Fill opacity (0.0 transparent to 1.0 opaque).
        """
        super().__init__(x, y, z_index)
        self.width = float(width)
        self.height = float(height)
        self._fill = Color(fill) if fill else None
        self._stroke = Color(stroke) if stroke else None
        self.stroke_width = float(stroke_width)
        self.opacity = float(opacity)
    
    @property
    def fill(self) -> str | None:
        """The fill color as a string, or None."""
        return self._fill.to_hex() if self._fill else None
    
    @fill.setter
    def fill(self, value: str | tuple[int, int, int] | None) -> None:
        self._fill = Color(value) if value else None
    
    @property
    def stroke(self) -> str | None:
        """The stroke color as a string, or None."""
        return self._stroke.to_hex() if self._stroke else None
    
    @stroke.setter
    def stroke(self, value: str | tuple[int, int, int] | None) -> None:
        self._stroke = Color(value) if value else None
    
    @property
    def anchor_names(self) -> list[str]:
        """Available anchor names."""
        return [
            "center",
            "top_left", "top_right", "bottom_left", "bottom_right",
            "top", "bottom", "left", "right",
        ]
    
    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        x, y = self.x, self.y
        w, h = self.width, self.height
        
        anchors = {
            "center": Point(x + w / 2, y + h / 2),
            "top_left": Point(x, y),
            "top_right": Point(x + w, y),
            "bottom_left": Point(x, y + h),
            "bottom_right": Point(x + w, y + h),
            "top": Point(x + w / 2, y),
            "bottom": Point(x + w / 2, y + h),
            "left": Point(x, y + h / 2),
            "right": Point(x + w, y + h / 2),
        }
        
        if name not in anchors:
            raise ValueError(f"Rect has no anchor '{name}'. Available: {self.anchor_names}")
        
        return anchors[name]
    
    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def to_svg(self) -> str:
        """Render to SVG rect element."""
        parts = [
            f'<rect x="{self.x}" y="{self.y}" '
            f'width="{self.width}" height="{self.height}"'
        ]
        
        if self._fill:
            parts.append(f' fill="{self.fill}"')
            if self.opacity < 1.0:
                parts.append(f' fill-opacity="{self.opacity}"')
        else:
            parts.append(' fill="none"')

        if self._stroke:
            parts.append(f' stroke="{self.stroke}" stroke-width="{self.stroke_width}"')
        
        parts.append(' />')
        return ''.join(parts)
    
    def __repr__(self) -> str:
        return (
            f"Rect({self.x}, {self.y}, {self.width}x{self.height}, "
            f"fill={self.fill!r}, stroke={self.stroke!r})"
        )
