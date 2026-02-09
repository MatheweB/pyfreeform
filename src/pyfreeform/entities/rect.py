"""Rect - A rectangle entity."""

from __future__ import annotations

import math

from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike


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
        if isinstance(center, tuple):
            center = Coord(*center)
        return cls(
            center.x - width / 2, center.y - height / 2,
            width, height, fill=fill, stroke=stroke,
            stroke_width=stroke_width, rotation=rotation,
            z_index=z_index, opacity=opacity,
            fill_opacity=fill_opacity, stroke_opacity=stroke_opacity,
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

    def _to_pixel_mode(self) -> None:
        """Resolve dimensions and position to pixels."""
        if self._relative_width is not None:
            self._pixel_width = self.width
            self._relative_width = None
        if self._relative_height is not None:
            self._pixel_height = self.height
            self._relative_height = None
        super()._to_pixel_mode()

    @property
    def _center(self) -> Coord:
        """Center of the rectangle (computed from top-left + dimensions)."""
        return Coord(self.x + self.width / 2, self.y + self.height / 2)

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

    def anchor(self, name: str = "center") -> Coord:
        """Get anchor point by name (rotation-aware)."""
        x, y = self.x, self.y
        w, h = self.width, self.height

        anchors = {
            "center": Coord(x + w / 2, y + h / 2),
            "top_left": Coord(x, y),
            "top_right": Coord(x + w, y),
            "bottom_left": Coord(x, y + h),
            "bottom_right": Coord(x + w, y + h),
            "top": Coord(x + w / 2, y),
            "bottom": Coord(x + w / 2, y + h),
            "left": Coord(x, y + h / 2),
            "right": Coord(x + w, y + h / 2),
        }

        if name not in anchors:
            raise ValueError(f"Rect has no anchor '{name}'. Available: {self.anchor_names}")

        point = anchors[name]

        # Rotate anchor around center if rotated
        if self.rotation != 0 and name != "center":
            center = anchors["center"]
            angle_rad = math.radians(self.rotation)
            point = point.rotated(angle_rad, origin=center)

        return point

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Rect:
        """
        Rotate the rectangle around a point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: rectangle center).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            # Rotate around own center: just update rotation angle
            self.rotation = (self.rotation + angle) % 360
        else:
            # Rotate position around external origin — switch to pixel mode
            self._to_pixel_mode()

            if isinstance(origin, tuple):
                origin = Coord(*origin)

            angle_rad = math.radians(angle)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            center = self._center
            dx = center.x - origin.x
            dy = center.y - origin.y
            new_cx = dx * cos_a - dy * sin_a + origin.x
            new_cy = dx * sin_a + dy * cos_a + origin.y

            self._position = Coord(new_cx - self.width / 2, new_cy - self.height / 2)
            self.rotation = (self.rotation + angle) % 360

        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Rect:
        """
        Scale the rectangle around a point.

        Args:
            factor: Scale factor (2.0 = double dimensions).
            origin: Center of scaling (default: rectangle center).

        Returns:
            self, for method chaining.
        """
        old_center = self._center

        # Scale dimensions (property setters clear relative bindings)
        self.width *= factor
        self.height *= factor

        if origin is not None:
            self._to_pixel_mode()
            if isinstance(origin, tuple):
                origin = Coord(*origin)
            new_cx = origin.x + (old_center.x - origin.x) * factor
            new_cy = origin.y + (old_center.y - origin.y) * factor
            self._position = Coord(new_cx - self.width / 2, new_cy - self.height / 2)
        else:
            # Keep center fixed
            self._position = Coord(old_center.x - self.width / 2, old_center.y - self.height / 2)

        return self

    def bounds(self) -> tuple[float, float, float, float]:
        """Get axis-aligned bounding box (accounts for rotation)."""
        if self.rotation == 0:
            return (self.x, self.y, self.x + self.width, self.y + self.height)

        # Get all four corners rotated
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

        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        """Render to SVG rect element."""
        parts = [
            f'<rect x="{self.x}" y="{self.y}" '
            f'width="{self.width}" height="{self.height}"'
        ]

        if self._fill:
            parts.append(f' fill="{self.fill}"')
        else:
            parts.append(' fill="none"')

        if self._stroke:
            parts.append(f' stroke="{self.stroke}" stroke-width="{self.stroke_width}"')

        # Opacity
        eff_fill_opacity = self.fill_opacity if self.fill_opacity is not None else self.opacity
        eff_stroke_opacity = self.stroke_opacity if self.stroke_opacity is not None else self.opacity
        if eff_fill_opacity < 1.0:
            parts.append(f' fill-opacity="{eff_fill_opacity}"')
        if eff_stroke_opacity < 1.0:
            parts.append(f' stroke-opacity="{eff_stroke_opacity}"')

        # Rotation (use SVG transform around center)
        if self.rotation != 0:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            parts.append(f' transform="rotate({self.rotation} {cx} {cy})"')

        parts.append(' />')
        return ''.join(parts)

    def __repr__(self) -> str:
        rot = f", rotation={self.rotation}°" if self.rotation != 0 else ""
        return (
            f"Rect({self.x}, {self.y}, {self.width}x{self.height}, "
            f"fill={self.fill!r}, stroke={self.stroke!r}{rot})"
        )
