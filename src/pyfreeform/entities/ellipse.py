"""Ellipse - An elliptical entity with parametric positioning."""

from __future__ import annotations

import math

from ..color import Color, apply_brightness
from ..core.coord import Coord, CoordLike
from ..core.entity import Entity
from ..core.bezier import sample_arc_length
from ..core.svg_utils import fill_stroke_attrs, shape_opacity_attrs, svg_num


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

    Example:
        ```python
        ellipse = Ellipse(100, 100, rx=30, ry=20, fill="coral")
        ellipse = Ellipse.at_center(Coord(100, 100), rx=30, ry=20)

        # Parametric positioning (t from 0 to 1)
        point = ellipse.point_at(0.25)  # Top of ellipse

        # Direct angle positioning (degrees)
        point = ellipse.point_at_angle(45)  # 45° from right

        # In a cell:
        ellipse = cell.add_ellipse(rx=0.3, ry=0.2, rotation=30)
        cell.add_dot(along=ellipse, t=cell.brightness)
        ```
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
        fill_brightness: float | None = None,
        stroke_brightness: float | None = None,
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
            fill_brightness: Brightness multiplier for fill 0.0 (black) to 1.0 (unchanged).
            stroke_brightness: Brightness multiplier for stroke 0.0 (black) to 1.0 (unchanged).
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

        if fill_brightness is not None and fill is not None:
            fill = apply_brightness(fill, fill_brightness)
        if stroke_brightness is not None and stroke is not None:
            stroke = apply_brightness(stroke, stroke_brightness)
        self._fill = Color(fill) if fill is not None else None
        self._stroke = Color(stroke) if stroke is not None else None

    @property
    def relative_rx(self) -> float | None:
        """Relative x-radius (fraction of reference width), or None."""
        return self._relative_rx

    @relative_rx.setter
    def relative_rx(self, value: float | None) -> None:
        self._relative_rx = value

    @property
    def relative_ry(self) -> float | None:
        """Relative y-radius (fraction of reference height), or None."""
        return self._relative_ry

    @relative_ry.setter
    def relative_ry(self, value: float | None) -> None:
        self._relative_ry = value

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
        center = Coord.coerce(center)
        return cls(
            center.x,
            center.y,
            rx,
            ry,
            rotation,
            fill,
            stroke,
            stroke_width,
            z_index,
            opacity,
            fill_opacity,
            stroke_opacity,
        )

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

    def _has_relative_properties(self) -> bool:
        return (
            super()._has_relative_properties()
            or self._relative_rx is not None
            or self._relative_ry is not None
        )

    def _resolve_to_absolute(self) -> None:
        """Resolve relative radii (rx/ry) and position to absolute values."""
        if self._relative_rx is not None:
            self._pixel_rx = self.rx
            self._relative_rx = None
        if self._relative_ry is not None:
            self._pixel_ry = self.ry
            self._relative_ry = None
        super()._resolve_to_absolute()

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

    def _named_anchor(self, name: str) -> Coord:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        if name == "right":
            return self.point_at_angle(0)
        if name == "top":
            return self.point_at_angle(90)
        if name == "left":
            return self.point_at_angle(180)
        if name == "bottom":
            return self.point_at_angle(270)
        raise ValueError(f"Ellipse has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Coord:
        """
        Get a point at parameter t along the ellipse perimeter.

        This is the key method for parametric positioning (Pathable protocol).

        Args:
            t:  Parameter from 0.0 to 1.0 around the ellipse.
                t=0 and t=1 are the same point (rightmost, 0°).
                t=0.25 is top (90°), t=0.5 is left (180°), t=0.75 is bottom (270°).

        Returns:
            Coord on the ellipse at parameter t.

        Example:
            ```python
            ellipse = cell.add_ellipse(rx=0.4, ry=0.3)
            cell.add_dot(along=ellipse, t=0.5)  # Dot at left side
            ```
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
        return sample_arc_length(self.point_at, segments)

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t on the ellipse.

        Uses the derivative of the parametric ellipse equations,
        then adds the entity's rotation.

        Args:
            t: Parameter from 0.0 to 1.0 around the ellipse.

        Returns:
            Angle in degrees (world space).
        """
        angle_rad = t * 2 * math.pi

        # Derivative of parametric ellipse (unrotated):
        # dx/dθ = -rx * sin(θ)
        # dy/dθ =  ry * cos(θ)
        dx = -self.rx * math.sin(angle_rad)
        dy = self.ry * math.cos(angle_rad)

        if dx == 0 and dy == 0:
            return self._rotation
        return math.degrees(math.atan2(dy, dx)) + self._rotation

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
            f"M {svg_num(sx)} {svg_num(sy)} "
            f"A {svg_num(self.rx)} {svg_num(self.ry)} {svg_num(self.rotation)} 1 1 {svg_num(mx)} {svg_num(my)} "
            f"A {svg_num(self.rx)} {svg_num(self.ry)} {svg_num(self.rotation)} 1 1 {svg_num(sx)} {svg_num(sy)}"
        )

    def point_at_angle(self, degrees: float) -> Coord:
        """
        Get a point at a specific angle on the ellipse perimeter.

        Args:
            degrees: Angle in degrees (0° = right, 90° = top, counterclockwise).

        Returns:
            Coord on the ellipse at the specified angle.

        Example:
            ```python
            point = ellipse.point_at_angle(45)  # Northeast
            point = ellipse.point_at_angle(180)  # Leftmost point
            ```
        """
        angle_rad = math.radians(degrees)
        return self._point_at_angle_rad(angle_rad)

    def _point_at_angle_rad(self, angle_rad: float) -> Coord:
        """Internal: Get point at angle (in radians) in world space.

        Computes the model-space point on the unrotated/unscaled ellipse,
        then delegates to ``_to_world_space`` for rotation and scale.
        """
        x_local = self.rx * math.cos(angle_rad)
        y_local = self.ry * math.sin(angle_rad)
        model_point = Coord(self.position.x + x_local, self.position.y + y_local)
        return self._to_world_space(model_point)

    @staticmethod
    def _ellipse_extents(rx: float, ry: float, angle_rad: float) -> tuple[float, float]:
        """Half-extents of an ellipse rotated by *angle_rad*. O(1), exact."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        dx = math.sqrt(rx * rx * c * c + ry * ry * s * s)
        dy = math.sqrt(rx * rx * s * s + ry * ry * c * c)
        return dx, dy

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Exact bounding box of the ellipse (handles rotation and scale).

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        cx, cy = self.position.x, self.position.y
        s = self._scale_factor
        if self._rotation == 0:
            dx, dy = self.rx * s, self.ry * s
        else:
            dx, dy = Ellipse._ellipse_extents(
                self.rx * s,
                self.ry * s,
                math.radians(self._rotation),
            )
        min_x, min_y = cx - dx, cy - dy
        max_x, max_y = cx + dx, cy + dy
        if visual and self.stroke_width:
            half = self.stroke_width * s / 2
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
        """Exact AABB of this ellipse rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        s = self._scale_factor
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        cx = self.position.x * cos_a - self.position.y * sin_a
        cy = self.position.x * sin_a + self.position.y * cos_a
        combined = math.radians(self._rotation) + rad
        dx, dy = Ellipse._ellipse_extents(self.rx * s, self.ry * s, combined)
        b = (cx - dx, cy - dy, cx + dx, cy + dy)
        if visual and self.stroke_width:
            half = self.stroke_width * s / 2
            b = (b[0] - half, b[1] - half, b[2] + half, b[3] + half)
        return b

    def inner_bounds(self) -> tuple[float, float, float, float]:
        """Inscribed rectangle of the ellipse."""
        cx, cy = self.position.x, self.position.y
        s = self._scale_factor
        if self._rotation == 0:
            hw = self.rx * s / math.sqrt(2)
            hh = self.ry * s / math.sqrt(2)
        else:
            hw = hh = min(self.rx, self.ry) * s / math.sqrt(2)
        return (cx - hw, cy - hh, cx + hw, cy + hh)

    def to_svg(self) -> str:
        """Render to SVG ellipse element."""
        return (
            f'<ellipse cx="{svg_num(self.position.x)}" cy="{svg_num(self.position.y)}"'
            f' rx="{svg_num(self.rx)}" ry="{svg_num(self.ry)}"'
            f"{fill_stroke_attrs(self.fill, self.stroke, self.stroke_width)}"
            f"{shape_opacity_attrs(self.opacity, self.fill_opacity, self.stroke_opacity)}"
            f"{self._build_svg_transform()} />"
        )

    def __repr__(self) -> str:
        return (
            f"Ellipse(center=({self.position.x}, {self.position.y}), "
            f"rx={self.rx}, ry={self.ry}, rotation={self.rotation}°)"
        )
