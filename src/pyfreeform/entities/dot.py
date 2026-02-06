"""Dot - A circular entity at a point."""

from __future__ import annotations

from ..color import Color
from ..core.entity import Entity
from ..core.point import Point


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
    
    Examples:
        >>> dot = Dot(100, 100)
        >>> dot = Dot(100, 100, radius=10, color="coral")
        >>> dot.move_to(150, 200)
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
    ) -> None:
        """
        Create a dot at the specified position.
        
        Args:
            x: Horizontal position.
            y: Vertical position.
            radius: Radius of the dot in pixels.
            color: Fill color (name, hex, or RGB tuple).
            z_index: Layer ordering (higher = on top).
        """
        super().__init__(x, y, z_index)
        self.radius = float(radius)
        self._color = Color(color)
    
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
    
    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        if name == "center":
            return self.position
        raise ValueError(f"Dot has no anchor '{name}'. Available: {self.anchor_names}")
    
    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box."""
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )
    
    def scale(self, factor: float, origin: Point | tuple[float, float] | None = None) -> Dot:
        """
        Scale the dot (changes radius and optionally position).
        
        Args:
            factor: Scale factor (2.0 = double the radius).
            origin: If provided, also moves position away from origin.
        
        Returns:
            self, for method chaining.
        """
        self.radius *= factor
        
        if origin is not None:
            # Also scale position relative to origin
            super().scale(factor, origin)
        
        return self
    
    def to_svg(self) -> str:
        """Render to SVG circle element."""
        return (
            f'<circle cx="{self.x}" cy="{self.y}" '
            f'r="{self.radius}" fill="{self.color}" />'
        )
    
    def __repr__(self) -> str:
        return f"Dot({self.x}, {self.y}, radius={self.radius}, color={self.color!r})"
