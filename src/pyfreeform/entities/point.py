"""Point - An invisible positional entity used as a movable anchor."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.entity import Entity

if TYPE_CHECKING:
    from ..core.coord import Coord


class Point(Entity):
    """
    An invisible entity that renders nothing.

    Use as a reactive vertex in Polygons or as a connection endpoint.
    Think of it as a thumbtack on a board — other shapes can reference
    it, and when the Point moves, everything attached follows.

    Anchors:
        - "center": The position (same as position)

    Example:
        ```python
        a = Point(0, 0)
        b = Point(100, 0)
        c = Point(50, 80)
        tri = Polygon([a, b, c], fill="coral")
        b.move_to_cell(cell, at=(0.8, 0.3))  # triangle vertex moves
        ```
    """

    def __init__(self, x: float = 0, y: float = 0, z_index: int = 0) -> None:
        super().__init__(x, y, z_index=z_index)

    @property
    def anchor_names(self) -> list[str]:
        return ["center"]

    def _named_anchor(self, name: str) -> Coord:
        if name == "center":
            return self._position
        raise ValueError(f"Point has no anchor '{name}'. Available: {self.anchor_names}")

    def to_svg(self) -> str:
        return ""

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        return (self._position.x, self._position.y, self._position.x, self._position.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
