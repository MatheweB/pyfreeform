"""Dot - A circular entity at a point."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..color import Color, apply_brightness
from ..core.entity import Entity
from ..core.svg_utils import opacity_attr, svg_num

if TYPE_CHECKING:
    from ..core.coord import Coord


class Dot(Entity):
    """
    A filled circle at a specific point.

    The fundamental "mark" in PyFreeform - think of it as touching
    a pen or brush to paper.

    Attributes:
        position: Center of the dot
        radius: Size of the dot
        color: Fill color

    Anchors:
        - "center": The center point (same as position)

    Example:
        ```python
        dot = Dot(100, 100)
        dot = Dot(100, 100, radius=10, color="coral")
        dot.move_to_surface(cell, at=(0.5, 0.5))
        ```
    """

    DEFAULT_RADIUS = 5
    DEFAULT_COLOR = "black"

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = DEFAULT_RADIUS,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        z_index: int = 0,
        opacity: float = 1.0,
        color_brightness: float | None = None,
    ) -> None:
        """
        Create a dot at the specified position.

        Args:
            x: Horizontal position.
            y: Vertical position.
            radius: Radius of the dot in pixels.
            color: Fill color (name, hex, or RGB tuple).
            z_index: Layer ordering (higher = on top).
            opacity: Opacity (0.0 transparent to 1.0 opaque).
            color_brightness: Brightness multiplier 0.0 (black) to 1.0 (unchanged).
        """
        super().__init__(x, y, z_index)
        self._pixel_radius = float(radius)
        self._relative_radius: float | None = None
        if color_brightness is not None:
            color = apply_brightness(color, color_brightness)
        self._color = Color(color)
        self.opacity = float(opacity)

    @property
    def relative_radius(self) -> float | None:
        """Relative radius (fraction of min(surface_w, surface_h)), or None."""
        return self._relative_radius

    @relative_radius.setter
    def relative_radius(self, value: float | None) -> None:
        self._relative_radius = value

    @property
    def radius(self) -> float:
        """Radius in pixels (resolved from relative fraction if set)."""
        if self._relative_radius is not None:
            resolved = self._resolve_size(self._relative_radius, "min")
            if resolved is not None:
                return resolved
        return self._pixel_radius

    @radius.setter
    def radius(self, value: float) -> None:
        self._pixel_radius = float(value)
        self._relative_radius = None

    def _has_relative_properties(self) -> bool:
        return super()._has_relative_properties() or self._relative_radius is not None

    def _resolve_to_absolute(self) -> None:
        """Resolve relative radius and position to absolute values."""
        if self._relative_radius is not None:
            self._pixel_radius = self.radius
            self._relative_radius = None
        super()._resolve_to_absolute()

    @property
    def color(self) -> str:
        """The fill color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors: just 'center' for dots."""
        return ["center"]

    def _named_anchor(self, name: str) -> Coord:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        raise ValueError(f"Dot has no anchor '{name}'. Available: {self.anchor_names}")

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Get bounding box (accounts for scale)."""
        cx, cy = self.x, self.y
        r = self.radius * self._scale_factor
        return (cx - r, cy - r, cx + r, cy + r)

    def rotated_bounds(
        self,
        angle: float,
        *,
        visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this dot rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)

        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        cx = self.x * cos_a - self.y * sin_a
        cy = self.x * sin_a + self.y * cos_a
        r = self.radius * self._scale_factor
        return (cx - r, cy - r, cx + r, cy + r)

    def inner_bounds(self) -> tuple[float, float, float, float]:
        """Inscribed square of the circle."""
        r = self.radius * self._scale_factor / math.sqrt(2)
        return (self.x - r, self.y - r, self.x + r, self.y + r)

    def to_svg(self) -> str:
        """Render to SVG circle element."""
        return (
            f'<circle cx="{svg_num(self.x)}" cy="{svg_num(self.y)}" r="{svg_num(self.radius)}" fill="{self.color}"'
            f"{opacity_attr(self.opacity)}"
            f"{self._build_svg_transform()} />"
        )

    def __repr__(self) -> str:
        return f"Dot({self.x}, {self.y}, radius={self.radius}, color={self.color!r})"
