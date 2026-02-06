"""Point - Immutable 2D coordinate with math operations."""

from __future__ import annotations

import math
from typing import NamedTuple


class Point(NamedTuple):
    """
    An immutable 2D point with math operations.
    
    Points are the foundation of all positioning in PyFreeform.
    They support arithmetic operations and common geometric calculations.
    
    Attributes:
        x: Horizontal coordinate
        y: Vertical coordinate
    
    Examples:
        >>> p1 = Point(100, 200)
        >>> p2 = Point(50, 50)
        >>> p1 + p2
        Point(x=150, y=250)
        >>> p1.distance_to(p2)
        158.11...
    """
    
    x: float
    y: float
    
    def __add__(self, other: Point | tuple[float, float]) -> Point:
        """Add two points (vector addition)."""
        if isinstance(other, tuple):
            other = Point(*other)
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point | tuple[float, float]) -> Point:
        """Subtract two points (vector subtraction)."""
        if isinstance(other, tuple):
            other = Point(*other)
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> Point:
        """Multiply point by scalar."""
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> Point:
        """Multiply point by scalar (reversed)."""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> Point:
        """Divide point by scalar."""
        return Point(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> Point:
        """Negate point (flip sign)."""
        return Point(-self.x, -self.y)
    
    def distance_to(self, other: Point) -> float:
        """Calculate Euclidean distance to another point."""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx * dx + dy * dy)
    
    def lerp(self, other: Point, t: float) -> Point:
        """
        Linear interpolation between this point and another.
        
        Args:
            other: The target point.
            t: Interpolation factor (0 = self, 1 = other).
               Values outside 0-1 extrapolate beyond the points.
        
        Returns:
            The interpolated point.
        
        Examples:
            >>> p1 = Point(0, 0)
            >>> p2 = Point(100, 100)
            >>> p1.lerp(p2, 0.5)
            Point(x=50.0, y=50.0)
        """
        return Point(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t
        )
    
    def midpoint(self, other: Point) -> Point:
        """Return the midpoint between this point and another."""
        return self.lerp(other, 0.5)
    
    def normalized(self) -> Point:
        """Return a unit vector pointing in the same direction."""
        length = math.sqrt(self.x * self.x + self.y * self.y)
        if length == 0:
            return Point(0, 0)
        return Point(self.x / length, self.y / length)
    
    def dot(self, other: Point) -> float:
        """Calculate dot product with another point (as vectors)."""
        return self.x * other.x + self.y * other.y
    
    def rotated(self, angle: float, origin: Point | None = None) -> Point:
        """
        Rotate point around an origin.
        
        Args:
            angle: Rotation angle in radians (counter-clockwise).
            origin: Center of rotation (default: origin 0,0).
        
        Returns:
            The rotated point.
        """
        if origin is None:
            origin = Point(0, 0)
        
        # Translate to origin
        dx = self.x - origin.x
        dy = self.y - origin.y
        
        # Rotate
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        new_x = dx * cos_a - dy * sin_a
        new_y = dx * sin_a + dy * cos_a
        
        # Translate back
        return Point(new_x + origin.x, new_y + origin.y)
    
    def clamped(self, min_x: float, min_y: float, max_x: float, max_y: float) -> Point:
        """Return point clamped to the given bounds."""
        return Point(
            max(min_x, min(max_x, self.x)),
            max(min_y, min(max_y, self.y))
        )
    
    def rounded(self, decimals: int = 0) -> Point:
        """Return point with coordinates rounded."""
        if decimals == 0:
            return Point(round(self.x), round(self.y))
        return Point(round(self.x, decimals), round(self.y, decimals))
    
    def as_tuple(self) -> tuple[float, float]:
        """Return as a plain tuple."""
        return (self.x, self.y)
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
