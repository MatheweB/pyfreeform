"""Rect - A rectangle entity."""

from __future__ import annotations

import math

from ..color import Color
from ..core.coord import Coord, CoordLike
from ..core.entity import Entity
from ..core.relcoord import RelCoord
from ..core.svg_utils import fill_stroke_attrs, shape_opacity_attrs


class Rect(Entity):
    """
    A rectangle entity.

    Rectangles can be used for backgrounds, cells, frames, and more.
    When placed in a cell, they can automatically fill the cell.

    Attributes:
        position: Top-left corner of the rectangle
        width: Rectangle width
        height: Rectangle height
        rotation: Rotation in degrees (counterclockwise)
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
        >>> rect = Rect(0, 0, 100, 50, fill="red", rotation=45)
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
        rotation: float = 0,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
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
            rotation: Rotation in degrees (counterclockwise).
            z_index: Layer ordering (higher = on top).
            opacity: Opacity for both fill and stroke (0.0-1.0).
            fill_opacity: Override opacity for fill only (None = use opacity).
            stroke_opacity: Override opacity for stroke only (None = use opacity).
        """
        super().__init__(x, y, z_index)
        self._pixel_width = float(width)
        self._pixel_height = float(height)
        self._relative_width: float | None = None
        self._relative_height: float | None = None
        self.rotation = float(rotation)
        self._fill = Color(fill) if fill else None
        self._stroke = Color(stroke) if stroke else None
        self.stroke_width = float(stroke_width)
        self.opacity = float(opacity)
        self.fill_opacity = fill_opacity
        self.stroke_opacity = stroke_opacity

    @property
    def relative_width(self) -> float | None:
        """Relative width (fraction of reference width), or None."""
        return self._relative_width

    @relative_width.setter
    def relative_width(self, value: float | None) -> None:
        self._relative_width = value

    @property
    def relative_height(self) -> float | None:
        """Relative height (fraction of reference height), or None."""
        return self._relative_height

    @relative_height.setter
    def relative_height(self, value: float | None) -> None:
        self._relative_height = value

    @classmethod
    def at_center(
        cls,
        center: CoordLike,
        width: float = 10,
        height: float = 10,
        rotation: float = 0,
        fill: str | tuple[int, int, int] | None = DEFAULT_FILL,
        stroke: str | tuple[int, int, int] | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
    ) -> Rect:
        """
        Create a rectangle positioned by its center.

        Args:
            center: Center position as Coord or (x, y) tuple.
            width: Rectangle width.
            height: Rectangle height.
            rotation: Rotation in degrees.
            fill: Fill color.
            stroke: Stroke color.
            stroke_width: Stroke width.
            z_index: Layer ordering.
            opacity: Opacity for both fill and stroke.
            fill_opacity: Override opacity for fill only.
            stroke_opacity: Override opacity for stroke only.

        Returns:
            A new Rect entity.
        """
        center = Coord.coerce(center)
        return cls(
            center.x - width / 2,
            center.y - height / 2,
            width,
            height,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            rotation=rotation,
            z_index=z_index,
            opacity=opacity,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
        )

    @property
    def width(self) -> float:
        """Width in pixels (resolved from relative fraction if set)."""
        if self._relative_width is not None:
            resolved = self._resolve_size(self._relative_width, "width")
            if resolved is not None:
                return resolved
        return self._pixel_width

    @width.setter
    def width(self, value: float) -> None:
        self._pixel_width = float(value)
        self._relative_width = None

    @property
    def height(self) -> float:
        """Height in pixels (resolved from relative fraction if set)."""
        if self._relative_height is not None:
            resolved = self._resolve_size(self._relative_height, "height")
            if resolved is not None:
                return resolved
        return self._pixel_height

    @height.setter
    def height(self, value: float) -> None:
        self._pixel_height = float(value)
        self._relative_height = None

    def _resolve_to_absolute(self) -> None:
        """Resolve relative width/height and position to absolute values."""
        if self._relative_width is not None:
            self._pixel_width = self.width
            self._relative_width = None
        if self._relative_height is not None:
            self._pixel_height = self.height
            self._relative_height = None
        super()._resolve_to_absolute()

    @property
    def _center(self) -> Coord:
        """Center of the rectangle (computed from top-left + dimensions)."""
        return Coord(self.x + self.width / 2, self.y + self.height / 2)

    @property
    def rotation_center(self) -> Coord:
        """Natural pivot for rotation/scale: rectangle center."""
        return self._center

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
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
            "top",
            "bottom",
            "left",
            "right",
        ]

    def _named_anchor(self, name: str) -> Coord:
        """Get anchor point by name (transform-aware)."""
        from ..core.positions import NAMED_POSITIONS

        if name not in NAMED_POSITIONS:
            raise ValueError(f"Rect has no anchor '{name}'. Available: {self.anchor_names}")
        return self._anchor_from_relcoord(NAMED_POSITIONS[name])

    def _anchor_from_relcoord(self, rc: RelCoord) -> Coord:
        """Resolve RelCoord in local rect space, then apply world transform."""
        local = Coord(self.x + rc.rx * self.width, self.y + rc.ry * self.height)
        return self._to_world_space(local)

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Get axis-aligned bounding box (accounts for rotation and scale).

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.
        """
        if self._rotation == 0 and self._scale_factor == 1.0:
            min_x, min_y = self.x, self.y
            max_x, max_y = self.x + self.width, self.y + self.height
        else:
            corners = [
                self.anchor("top_left"),
                self.anchor("top_right"),
                self.anchor("bottom_left"),
                self.anchor("bottom_right"),
            ]
            min_x = min(c.x for c in corners)
            min_y = min(c.y for c in corners)
            max_x = max(c.x for c in corners)
            max_y = max(c.y for c in corners)

        if visual and self.stroke_width:
            half = self.stroke_width * self._scale_factor / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def rotated_bounds(
        self,
        angle: float,
        *,
        visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this rect rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        corners = [
            self.anchor("top_left"),
            self.anchor("top_right"),
            self.anchor("bottom_left"),
            self.anchor("bottom_right"),
        ]
        rx = [c.x * cos_a - c.y * sin_a for c in corners]
        ry = [c.x * sin_a + c.y * cos_a for c in corners]
        min_x, max_x = min(rx), max(rx)
        min_y, max_y = min(ry), max(ry)
        if visual and self.stroke_width:
            half = self.stroke_width / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        """Render to SVG rect element."""
        return (
            f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}"'
            f"{fill_stroke_attrs(self.fill, self.stroke, self.stroke_width)}"
            f"{shape_opacity_attrs(self.opacity, self.fill_opacity, self.stroke_opacity)}"
            f"{self._build_svg_transform()} />"
        )

    def __repr__(self) -> str:
        rot = f", rotation={self.rotation}°" if self.rotation != 0 else ""
        return (
            f"Rect({self.x}, {self.y}, {self.width}x{self.height}, "
            f"fill={self.fill!r}, stroke={self.stroke!r}{rot})"
        )
