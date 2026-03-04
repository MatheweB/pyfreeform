"""Protocols for cross-module type narrowing without circular imports.

These protocols let the renderer distinguish Entity objects from Surface
objects at runtime, without creating a circular import between the renderer
package and ``core.entity`` / ``core.connection``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .coord import Coord
from .positions import AnchorSpec


@runtime_checkable
class Animatable(Protocol):
    """Structural protocol satisfied by all concrete Entity subclasses.

    Captures the minimal interface that the reactive animation renderer
    needs to track animated connection endpoints and polygon vertices.
    Surface objects do *not* satisfy this protocol (they have no
    ``_animations``), so ``isinstance(obj, Animatable)`` cleanly separates
    Entity endpoints from Surface endpoints at runtime.
    """

    _animations: list

    def surface_position_at(self, rx: float, ry: float) -> tuple[float, float]: ...

    @property
    def position(self) -> Coord: ...

    def anchor(self, spec: AnchorSpec = "center") -> Coord: ...
