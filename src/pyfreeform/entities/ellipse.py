"""Ellipse - An elliptical entity with parametric positioning."""

from __future__ import annotations

import math

from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike


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
        >>> ellipse = Ellipse.at_center(Coord(100, 100), rx=30, ry=20)

        >>> # Parametric positioning (t from 0 to 1)
        >>> point = ellipse.point_at(0.25)  # Top of ellipse

        >>> # Direct angle positioning (degrees)
        >>> point = ellipse.point_at_angle(45)  # 45° from right

        >>> # In a cell:
        >>> ellipse = cell.add_ellipse(rx=0.3, ry=0.2, rotation=30)
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
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
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
            opacity: Opacity for both fill and stroke (0.0-1.0).
            fill_opacity: Override opacity for fill only (None = use opacity).
            stroke_opacity: Override opacity for stroke only (None = use opacity).
        """
        super().__init__(x, y, z_index)
        self._pixel_rx = float(rx)
        self._pixel_ry = float(ry)
        self._relative_rx: float | None = None
        self._relative_ry: float | None = None
        self.rotation = float(rotation)
        self.stroke_width = float(stroke_width)
        self.opacity = float(opacity)
        self.fill_opacity = fill_opacity
        self.stroke_opacity = stroke_opacity

        self._fill = Color(fill) if fill is not None else None
        self._stroke = Color(stroke) if stroke is not None else None

    @classmethod
    def at_center(
        cls,
        center: CoordLike,
        rx: float = 10,
        ry: float = 10,
        rotation: float = 0,
        fill: str | tuple[int, int, int] | None = DEFAULT_FILL,
        stroke: str | tuple[int, int, int] | None = DEFAULT_STROKE,
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
    ) -> Ellipse:
        """
        Create an ellipse at a specific center point.

        Args:
            center: Center position as Coord or (x, y) tuple.
            rx: Horizontal radius.
            ry: Vertical radius.
            rotation: Rotation in degrees.
            fill: Fill color.
            stroke: Stroke color.
            stroke_width: Stroke width.
            z_index: Layer ordering.
            opacity: Opacity for both fill and stroke.
            fill_opacity: Override opacity for fill only.
            stroke_opacity: Override opacity for stroke only.

        Returns:
            A new Ellipse entity.
        """
        center = Coord._coerce(center)
        return cls(center.x, center.y, rx, ry, rotation, fill, stroke, stroke_width,
                   z_index, opacity, fill_opacity, stroke_opacity)

    @property
    def rx(self) -> float:
        """Horizontal radius in pixels (resolved from relative fraction if set)."""
        if self._relative_rx is not None:
            resolved = self._resolve_size(self._relative_rx, "width")
            if resolved is not None:
                return resolved
        return self._pixel_rx

    @rx.setter
    def rx(self, value: float) -> None:
        self._pixel_rx = float(value)
        self._relative_rx = None

    @property
    def ry(self) -> float:
        """Vertical radius in pixels (resolved from relative fraction if set)."""
        if self._relative_ry is not None:
            resolved = self._resolve_size(self._relative_ry, "height")
            if resolved is not None:
                return resolved
        return self._pixel_ry

    @ry.setter
    def ry(self, value: float) -> None:
        self._pixel_ry = float(value)
        self._relative_ry = None

    def _to_pixel_mode(self) -> None:
        """Resolve radii and position to pixels."""
        if self._relative_rx is not None:
            self._pixel_rx = self.rx
            self._relative_rx = None
        if self._relative_ry is not None:
            self._pixel_ry = self.ry
            self._relative_ry = None
        super()._to_pixel_mode()

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

    def anchor(self, name: str = "center") -> Coord:
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

    def point_at(self, t: float) -> Coord:
        """
        Get a point at parameter t along the ellipse perimeter.

        This is the key method for parametric positioning (Pathable protocol).

        Args:
            t: Parameter from 0.0 to 1.0 around the ellipse.
               t=0 and t=1 are the same point (rightmost, 0°).
               t=0.25 is top (90°), t=0.5 is left (180°), t=0.75 is bottom (270°).

        Returns:
            Coord on the ellipse at parameter t.

        Example:
            >>> ellipse = cell.add_ellipse(rx=0.4, ry=0.3)
            >>> cell.add_dot(along=ellipse, t=0.5)  # Dot at left side
        """
        # Convert t (0-1) to angle in radians
        angle_rad = t * 2 * math.pi
        return self._point_at_angle_rad(angle_rad)

    def arc_length(self, segments: int = 100) -> float:
        """
        Approximate the perimeter (arc length) of the ellipse by sampling.

        Args:
            segments: Number of line segments to approximate with.

        Returns:
            Approximate arc length in pixels.
        """
        total = 0.0
        prev = self.point_at(0)
        for i in range(1, segments + 1):
            curr = self.point_at(i / segments)
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            total += math.sqrt(dx * dx + dy * dy)
            prev = curr
        return total

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t on the ellipse.

        Uses the derivative of the parametric ellipse equations,
        accounting for rotation.

        Args:
            t: Parameter from 0.0 to 1.0 around the ellipse.

        Returns:
            Angle in degrees.
        """
        angle_rad = t * 2 * math.pi

        # Derivative of parametric ellipse (unrotated):
        # dx/dθ = -rx * sin(θ)
        # dy/dθ =  ry * cos(θ)
        dx_unrot = -self.rx * math.sin(angle_rad)
        dy_unrot = self.ry * math.cos(angle_rad)

        # Apply ellipse rotation
        if self.rotation != 0:
            rot_rad = math.radians(self.rotation)
            cos_r = math.cos(rot_rad)
            sin_r = math.sin(rot_rad)
            dx = dx_unrot * cos_r - dy_unrot * sin_r
            dy = dx_unrot * sin_r + dy_unrot * cos_r
        else:
            dx, dy = dx_unrot, dy_unrot

        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for the full ellipse as two arcs."""
        cx, cy = self.position.x, self.position.y

        # Right point (start) and left point (midway), accounting for rotation
        if self.rotation != 0:
            rot_rad = math.radians(self.rotation)
            cos_r, sin_r = math.cos(rot_rad), math.sin(rot_rad)
            # Rightmost point
            sx = cx + self.rx * cos_r
            sy = cy + self.rx * sin_r
            # Leftmost point
            mx = cx - self.rx * cos_r
            my = cy - self.rx * sin_r
        else:
            sx = cx + self.rx
            sy = cy
            mx = cx - self.rx
            my = cy

        return (
            f"M {sx} {sy} "
            f"A {self.rx} {self.ry} {self.rotation} 1 1 {mx} {my} "
            f"A {self.rx} {self.ry} {self.rotation} 1 1 {sx} {sy}"
        )

    def point_at_angle(self, degrees: float) -> Coord:
        """
        Get a point at a specific angle on the ellipse perimeter.

        Args:
            degrees: Angle in degrees (0° = right, 90° = top, counterclockwise).

        Returns:
            Coord on the ellipse at the specified angle.

        Example:
            >>> point = ellipse.point_at_angle(45)  # Northeast
            >>> point = ellipse.point_at_angle(180)  # Leftmost point
        """
        angle_rad = math.radians(degrees)
        return self._point_at_angle_rad(angle_rad)

    def _point_at_angle_rad(self, angle_rad: float) -> Coord:
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
        return Coord(self.position.x + x_rot, self.position.y + y_rot)

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Ellipse:
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
            # Rotate position around external origin — switch to pixel mode
            self._to_pixel_mode()

            origin = Coord._coerce(origin)

            angle_rad = math.radians(angle)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            dx = self.position.x - origin.x
            dy = self.position.y - origin.y
            new_x = dx * cos_a - dy * sin_a + origin.x
            new_y = dx * sin_a + dy * cos_a + origin.y
            self._position = Coord(new_x, new_y)

            self.rotation = (self.rotation + angle) % 360

        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Ellipse:
        """
        Scale the ellipse around a point.

        Args:
            factor: Scale factor (2.0 = double the radii).
            origin: Center of scaling (default: ellipse center).

        Returns:
            self, for method chaining.
        """
        # Scale the radii (property setters clear relative bindings)
        self.rx *= factor
        self.ry *= factor

        if origin is not None:
            self._to_pixel_mode()
            origin = Coord._coerce(origin)

            new_x = origin.x + (self.position.x - origin.x) * factor
            new_y = origin.y + (self.position.y - origin.y) * factor
            self._position = Coord(new_x, new_y)

        return self

    @staticmethod
    def _ellipse_extents(rx: float, ry: float, angle_rad: float) -> tuple[float, float]:
        """Half-extents of an ellipse rotated by *angle_rad*. O(1), exact."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        dx = math.sqrt(rx * rx * c * c + ry * ry * s * s)
        dy = math.sqrt(rx * rx * s * s + ry * ry * c * c)
        return dx, dy

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Exact bounding box of the ellipse (handles rotation analytically).

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        cx, cy = self.position.x, self.position.y
        if self.rotation == 0:
            dx, dy = self.rx, self.ry
        else:
            dx, dy = Ellipse._ellipse_extents(
                self.rx, self.ry, math.radians(self.rotation),
            )
        min_x, min_y = cx - dx, cy - dy
        max_x, max_y = cx + dx, cy + dy
        if visual and self.stroke_width:
            half = self.stroke_width / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def _rotated_bounds(
        self, angle: float, *, visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this ellipse rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        cx = self.position.x * cos_a - self.position.y * sin_a
        cy = self.position.x * sin_a + self.position.y * cos_a
        combined = math.radians(self.rotation) + rad
        dx, dy = Ellipse._ellipse_extents(self.rx, self.ry, combined)
        b = (cx - dx, cy - dy, cx + dx, cy + dy)
        if visual and self.stroke_width:
            half = self.stroke_width / 2
            b = (b[0] - half, b[1] - half, b[2] + half, b[3] + half)
        return b

    def inner_bounds(self) -> tuple[float, float, float, float]:
        """Inscribed rectangle of the ellipse."""
        cx, cy = self.position.x, self.position.y
        if self.rotation == 0:
            hw = self.rx / math.sqrt(2)
            hh = self.ry / math.sqrt(2)
        else:
            # Conservative: inscribed square using the smaller radius
            hw = hh = min(self.rx, self.ry) / math.sqrt(2)
        return (cx - hw, cy - hh, cx + hw, cy + hh)

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

        # Opacity
        eff_fill_opacity = self.fill_opacity if self.fill_opacity is not None else self.opacity
        eff_stroke_opacity = self.stroke_opacity if self.stroke_opacity is not None else self.opacity
        if eff_fill_opacity < 1.0:
            parts.append(f' fill-opacity="{eff_fill_opacity}"')
        if eff_stroke_opacity < 1.0:
            parts.append(f' stroke-opacity="{eff_stroke_opacity}"')

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
