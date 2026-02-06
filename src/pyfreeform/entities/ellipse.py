"""Ellipse - An elliptical entity with parametric positioning."""

from __future__ import annotations

import math

from ..color import Color
from ..core.entity import Entity
from ..core.point import Point


class Ellipse(Entity):
    """
    An ellipse (oval) with parametric positioning support.

    Ellipses are defined by horizontal radius (rx), vertical radius (ry),
    and optional rotation. They support both parametric positioning via
    `point_at(t)` and direct angle-based positioning via `point_at_angle(degrees)`.

    Attributes:
        position: Center of the ellipse
        rx: Horizontal radius
        ry: Vertical radius
        rotation: Rotation in degrees (counterclockwise)
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width in pixels

    Anchors:
        - "center": The center point (same as position)
        - "right": Rightmost point (0°)
        - "top": Topmost point (90°)
        - "left": Leftmost point (180°)
        - "bottom": Bottommost point (270°)

    Examples:
        >>> ellipse = Ellipse(100, 100, rx=30, ry=20, fill="coral")
        >>> ellipse = Ellipse.at_center(Point(100, 100), rx=30, ry=20)

        >>> # Parametric positioning (t from 0 to 1)
        >>> point = ellipse.point_at(0.25)  # Top of ellipse

        >>> # Direct angle positioning (degrees)
        >>> point = ellipse.point_at_angle(45)  # 45° from right

        >>> # In a cell:
        >>> ellipse = cell.add_ellipse(rx=15, ry=10, rotation=30)
        >>> cell.add_dot(along=ellipse, t=cell.brightness)
    """

    DEFAULT_FILL = "black"
    DEFAULT_STROKE = None
    DEFAULT_STROKE_WIDTH = 1

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        rx: float = 10,
        ry: float = 10,
        rotation: float = 0,
        fill: str | tuple[int, int, int] | None = DEFAULT_FILL,
        stroke: str | tuple[int, int, int] | None = DEFAULT_STROKE,
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        z_index: int = 0,
    ) -> None:
        """
        Create an ellipse at the specified center position.

        Args:
            x: Horizontal center position.
            y: Vertical center position.
            rx: Horizontal radius (half-width).
            ry: Vertical radius (half-height).
            rotation: Rotation in degrees (counterclockwise).
            fill: Fill color (name, hex, RGB tuple, or None for transparent).
            stroke: Stroke color (None for no stroke).
            stroke_width: Stroke width in pixels.
            z_index: Layer ordering (higher = on top).
        """
        super().__init__(x, y, z_index)
        self.rx = float(rx)
        self.ry = float(ry)
        self.rotation = float(rotation)
        self.stroke_width = float(stroke_width)

        self._fill = Color(fill) if fill is not None else None
        self._stroke = Color(stroke) if stroke is not None else None

    @classmethod
    def at_center(
        cls,
        center: Point | tuple[float, float],
        rx: float = 10,
        ry: float = 10,
        rotation: float = 0,
        fill: str | tuple[int, int, int] | None = DEFAULT_FILL,
        stroke: str | tuple[int, int, int] | None = DEFAULT_STROKE,
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        z_index: int = 0,
    ) -> Ellipse:
        """
        Create an ellipse at a specific center point.

        Args:
            center: Center position as Point or (x, y) tuple.
            rx: Horizontal radius.
            ry: Vertical radius.
            rotation: Rotation in degrees.
            fill: Fill color.
            stroke: Stroke color.
            stroke_width: Stroke width.
            z_index: Layer ordering.

        Returns:
            A new Ellipse entity.
        """
        if isinstance(center, tuple):
            center = Point(*center)
        return cls(center.x, center.y, rx, ry, rotation, fill, stroke, stroke_width, z_index)

    @property
    def fill(self) -> str | None:
        """The fill color as a string, or None if transparent."""
        return self._fill.to_hex() if self._fill else None

    @fill.setter
    def fill(self, value: str | tuple[int, int, int] | None) -> None:
        self._fill = Color(value) if value is not None else None

    @property
    def stroke(self) -> str | None:
        """The stroke color as a string, or None if no stroke."""
        return self._stroke.to_hex() if self._stroke else None

    @stroke.setter
    def stroke(self, value: str | tuple[int, int, int] | None) -> None:
        self._stroke = Color(value) if value is not None else None

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors: center, right, top, left, bottom."""
        return ["center", "right", "top", "left", "bottom"]

    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        elif name == "right":
            return self.point_at_angle(0)
        elif name == "top":
            return self.point_at_angle(90)
        elif name == "left":
            return self.point_at_angle(180)
        elif name == "bottom":
            return self.point_at_angle(270)
        raise ValueError(f"Ellipse has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Point:
        """
        Get a point at parameter t along the ellipse perimeter.

        This is the key method for parametric positioning (Pathable protocol).

        Args:
            t: Parameter from 0.0 to 1.0 around the ellipse.
               t=0 and t=1 are the same point (rightmost, 0°).
               t=0.25 is top (90°), t=0.5 is left (180°), t=0.75 is bottom (270°).

        Returns:
            Point on the ellipse at parameter t.

        Example:
            >>> ellipse = cell.add_ellipse(rx=20, ry=15)
            >>> cell.add_dot(along=ellipse, t=0.5)  # Dot at left side
        """
        # Convert t (0-1) to angle in radians
        angle_rad = t * 2 * math.pi
        return self._point_at_angle_rad(angle_rad)

    def point_at_angle(self, degrees: float) -> Point:
        """
        Get a point at a specific angle on the ellipse perimeter.

        Args:
            degrees: Angle in degrees (0° = right, 90° = top, counterclockwise).

        Returns:
            Point on the ellipse at the specified angle.

        Example:
            >>> point = ellipse.point_at_angle(45)  # Northeast
            >>> point = ellipse.point_at_angle(180)  # Leftmost point
        """
        angle_rad = math.radians(degrees)
        return self._point_at_angle_rad(angle_rad)

    def _point_at_angle_rad(self, angle_rad: float) -> Point:
        """Internal: Get point at angle (in radians), accounting for rotation."""
        # Parametric ellipse equation (unrotated)
        x_unrot = self.rx * math.cos(angle_rad)
        y_unrot = self.ry * math.sin(angle_rad)

        # Apply ellipse rotation if any
        if self.rotation != 0:
            rot_rad = math.radians(self.rotation)
            cos_r = math.cos(rot_rad)
            sin_r = math.sin(rot_rad)
            x_rot = x_unrot * cos_r - y_unrot * sin_r
            y_rot = x_unrot * sin_r + y_unrot * cos_r
        else:
            x_rot, y_rot = x_unrot, y_unrot

        # Translate to center position
        return Point(self.position.x + x_rot, self.position.y + y_rot)

    def rotate(self, angle: float, origin: Point | tuple[float, float] | None = None) -> Ellipse:
        """
        Rotate the ellipse around a point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: ellipse center).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            # Rotate around own center: just update rotation angle
            self.rotation = (self.rotation + angle) % 360
        else:
            # Rotate position around external origin
            if isinstance(origin, tuple):
                origin = Point(*origin)

            angle_rad = math.radians(angle)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            # Rotate position
            dx = self.position.x - origin.x
            dy = self.position.y - origin.y
            new_x = dx * cos_a - dy * sin_a + origin.x
            new_y = dx * sin_a + dy * cos_a + origin.y
            self._position = Point(new_x, new_y)

            # Also update intrinsic rotation
            self.rotation = (self.rotation + angle) % 360

        return self

    def scale(self, factor: float, origin: Point | tuple[float, float] | None = None) -> Ellipse:
        """
        Scale the ellipse around a point.

        Args:
            factor: Scale factor (2.0 = double the radii).
            origin: Center of scaling (default: ellipse center).

        Returns:
            self, for method chaining.
        """
        # Scale the radii
        self.rx *= factor
        self.ry *= factor

        if origin is not None:
            # Also scale position relative to origin
            if isinstance(origin, tuple):
                origin = Point(*origin)

            new_x = origin.x + (self.position.x - origin.x) * factor
            new_y = origin.y + (self.position.y - origin.y) * factor
            self._position = Point(new_x, new_y)

        return self

    def bounds(self) -> tuple[float, float, float, float]:
        """
        Get bounding box of the ellipse.

        For rotated ellipses, this computes the axis-aligned bounding box
        that fully contains the rotated ellipse.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        if self.rotation == 0:
            # Simple case: axis-aligned ellipse
            return (
                self.position.x - self.rx,
                self.position.y - self.ry,
                self.position.x + self.rx,
                self.position.y + self.ry,
            )

        # For rotated ellipse, compute bounds of the rotated bounding box
        # We check the extrema by sampling points around the ellipse
        angles = [i * math.pi / 180 for i in range(0, 360, 30)]  # Sample every 30°
        points = [self._point_at_angle_rad(a) for a in angles]

        min_x = min(p.x for p in points)
        min_y = min(p.y for p in points)
        max_x = max(p.x for p in points)
        max_y = max(p.y for p in points)

        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        """Render to SVG ellipse element."""
        parts = [
            f'<ellipse cx="{self.position.x}" cy="{self.position.y}"',
            f' rx="{self.rx}" ry="{self.ry}"',
        ]

        # Fill
        if self.fill:
            parts.append(f' fill="{self.fill}"')
        else:
            parts.append(' fill="none"')

        # Stroke
        if self.stroke:
            parts.append(f' stroke="{self.stroke}" stroke-width="{self.stroke_width}"')

        # Rotation (use SVG transform)
        if self.rotation != 0:
            parts.append(f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"')

        parts.append(' />')
        return ''.join(parts)

    def __repr__(self) -> str:
        return (
            f"Ellipse(center=({self.position.x}, {self.position.y}), "
            f"rx={self.rx}, ry={self.ry}, rotation={self.rotation}°)"
        )
