from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias, Union

NamedPosition: TypeAlias = Literal[
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

RelCoordLike = Union["RelCoord", tuple[float, float], NamedPosition]


@dataclass(frozen=True, slots=True)
class RelCoord:
    """
    An immutable 2D relative coordinate (fractions 0.0-1.0).

    Used for positioning within surfaces. (0, 0) is top-left, (1, 1) is bottom-right.
    Fields are named ``rx`` and ``ry`` to prevent confusion with pixel ``Coord(x, y)``.

    Example:
        ```python
        p = RelCoord(0.5, 0.5)
        p.rx, p.ry            # (0.5, 0.5)
        p + RelCoord(0.1, 0)  # RelCoord(0.6, 0.5)
        ```
    """

    rx: float
    ry: float

    def __iter__(self):
        """Support unpacking: rx, ry = relcoord."""
        yield self.rx
        yield self.ry

    def __getitem__(self, idx: int) -> float:
        """Support indexing: relcoord[0], relcoord[1]."""
        return (self.rx, self.ry)[idx]

    def __len__(self) -> int:
        return 2

    def __add__(self, other: RelCoordLike) -> RelCoord:
        """Add two relative coords."""
        other = RelCoord.coerce(other)
        return RelCoord(self.rx + other.rx, self.ry + other.ry)

    def __sub__(self, other: RelCoordLike) -> RelCoord:
        """Subtract two relative coords."""
        other = RelCoord.coerce(other)
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

    def clamped(
        self, min_rx: float = 0.0, min_ry: float = 0.0, max_rx: float = 1.0, max_ry: float = 1.0
    ) -> RelCoord:
        """Return clamped to valid range (default 0.0-1.0)."""
        return RelCoord(
            max(min_rx, min(max_rx, self.rx)),
            max(min_ry, min(max_ry, self.ry)),
        )

    def as_tuple(self) -> tuple[float, float]:
        """Return as a plain tuple."""
        return (self.rx, self.ry)

    @classmethod
    def coerce(cls, value: RelCoordLike) -> RelCoord:
        """Convert a RelCoordLike to a RelCoord, passing through if already a RelCoord."""
        if isinstance(value, RelCoord):
            return value

        if isinstance(value, tuple) and len(value) == 2:
            return RelCoord(*value)

        from .positions import NAMED_POSITIONS

        if isinstance(value, str) and value in NAMED_POSITIONS:
            return RelCoord(*NAMED_POSITIONS[value])

        raise TypeError(
            f"Cannot coerce {type(value).__name__} to RelCoord. "
            'Expected `RelCoord` or `tuple[float, float]` or String in NAMED_POSITIONS (e.g. "center")'
        )

    def __repr__(self) -> str:
        return f"RelCoord({self.rx}, {self.ry})"
