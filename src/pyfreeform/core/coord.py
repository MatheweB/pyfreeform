"""Coord and RelCoord - Immutable 2D coordinate types."""

from __future__ import annotations

import math
from typing import NamedTuple


class Coord(NamedTuple):
    """
    An immutable 2D coordinate with math operations.

    Coords are the foundation of all positioning in PyFreeform.
    They support arithmetic operations and common geometric calculations.

    Attributes:
        x: Horizontal coordinate
        y: Vertical coordinate

    Examples:
        >>> p1 = Coord(100, 200)
        >>> p2 = Coord(50, 50)
        >>> p1 + p2
        Coord(x=150, y=250)
        >>> p1.distance_to(p2)
        158.11...
    """

    x: float
    y: float

    def __add__(self, other: CoordLike) -> Coord:
        """Add two coords (vector addition)."""
        if isinstance(other, tuple):
            other = Coord(*other)
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: CoordLike) -> Coord:
        """Subtract two coords (vector subtraction)."""
        if isinstance(other, tuple):
            other = Coord(*other)
        return Coord(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Coord:
        """Multiply coord by scalar."""
        return Coord(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Coord:
        """Multiply coord by scalar (reversed)."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Coord:
        """Divide coord by scalar."""
        return Coord(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Coord:
        """Negate coord (flip sign)."""
        return Coord(-self.x, -self.y)

    def distance_to(self, other: Coord) -> float:
        """Calculate Euclidean distance to another coord."""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def lerp(self, other: Coord, t: float) -> Coord:
        """
        Linear interpolation between this coord and another.

        Args:
            other: The target coord.
            t: Interpolation factor (0 = self, 1 = other).
               Values outside 0-1 extrapolate beyond the coords.

        Returns:
            The interpolated coord.

        Examples:
            >>> p1 = Coord(0, 0)
            >>> p2 = Coord(100, 100)
            >>> p1.lerp(p2, 0.5)
            Coord(x=50.0, y=50.0)
        """
        return Coord(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t
        )

    def midpoint(self, other: Coord) -> Coord:
        """Return the midpoint between this coord and another."""
        return self.lerp(other, 0.5)

    def normalized(self) -> Coord:
        """Return a unit vector pointing in the same direction."""
        length = math.sqrt(self.x * self.x + self.y * self.y)
        if length == 0:
            return Coord(0, 0)
        return Coord(self.x / length, self.y / length)

    def dot(self, other: Coord) -> float:
        """Calculate dot product with another coord (as vectors)."""
        return self.x * other.x + self.y * other.y

    def rotated(self, angle: float, origin: Coord | None = None) -> Coord:
        """
        Rotate coord around an origin.

        Args:
            angle: Rotation angle in radians (counter-clockwise).
            origin: Center of rotation (default: origin 0,0).

        Returns:
            The rotated coord.
        """
        if origin is None:
            origin = Coord(0, 0)

        # Translate to origin
        dx = self.x - origin.x
        dy = self.y - origin.y

        # Rotate
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        new_x = dx * cos_a - dy * sin_a
        new_y = dx * sin_a + dy * cos_a

        # Translate back
        return Coord(new_x + origin.x, new_y + origin.y)

    def clamped(self, min_x: float, min_y: float, max_x: float, max_y: float) -> Coord:
        """Return coord clamped to the given bounds."""
        return Coord(
            max(min_x, min(max_x, self.x)),
            max(min_y, min(max_y, self.y))
        )

    def rounded(self, decimals: int = 0) -> Coord:
        """Return coord with coordinates rounded."""
        if decimals == 0:
            return Coord(round(self.x), round(self.y))
        return Coord(round(self.x, decimals), round(self.y, decimals))

    def as_tuple(self) -> tuple[float, float]:
        """Return as a plain tuple."""
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Coord({self.x}, {self.y})"


CoordLike = Coord | tuple[float, float]


class RelCoord(NamedTuple):
    """
    An immutable 2D relative coordinate (fractions 0.0–1.0).

    Used for positioning within surfaces. (0, 0) is top-left, (1, 1) is bottom-right.
    Fields are named ``rx`` and ``ry`` to prevent confusion with pixel ``Coord(x, y)``.

    Examples:
        >>> p = RelCoord(0.5, 0.5)
        >>> p.rx, p.ry
        (0.5, 0.5)
        >>> p + RelCoord(0.1, 0)
        RelCoord(rx=0.6, ry=0.5)
    """

    rx: float
    ry: float

    def __add__(self, other: RelCoordLike) -> RelCoord:
        """Add two relative coords."""
        if isinstance(other, tuple):
            other = RelCoord(*other)
        return RelCoord(self.rx + other.rx, self.ry + other.ry)

    def __sub__(self, other: RelCoordLike) -> RelCoord:
        """Subtract two relative coords."""
        if isinstance(other, tuple):
            other = RelCoord(*other)
        return RelCoord(self.rx - other.rx, self.ry - other.ry)

    def __mul__(self, scalar: float) -> RelCoord:
        """Multiply by scalar."""
        return RelCoord(self.rx * scalar, self.ry * scalar)

    def __rmul__(self, scalar: float) -> RelCoord:
        """Multiply by scalar (reversed)."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> RelCoord:
        """Divide by scalar."""
        return RelCoord(self.rx / scalar, self.ry / scalar)

    def __neg__(self) -> RelCoord:
        """Negate (flip sign)."""
        return RelCoord(-self.rx, -self.ry)

    def lerp(self, other: RelCoord, t: float) -> RelCoord:
        """Linear interpolation between this and another relative coord."""
        return RelCoord(
            self.rx + (other.rx - self.rx) * t,
            self.ry + (other.ry - self.ry) * t,
        )

    def clamped(self, min_rx: float = 0.0, min_ry: float = 0.0,
                max_rx: float = 1.0, max_ry: float = 1.0) -> RelCoord:
        """Return clamped to valid range (default 0.0–1.0)."""
        return RelCoord(
            max(min_rx, min(max_rx, self.rx)),
            max(min_ry, min(max_ry, self.ry)),
        )

    def as_tuple(self) -> tuple[float, float]:
        """Return as a plain tuple."""
        return (self.rx, self.ry)

    def __repr__(self) -> str:
        return f"RelCoord({self.rx}, {self.ry})"


RelCoordLike = RelCoord | tuple[float, float]
