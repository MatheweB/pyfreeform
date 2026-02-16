"""Binding — Immutable positioning configuration for entities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .relcoord import RelCoord
    from .entity import Entity
    from .pathable import Pathable
    from .surface import Surface


@dataclass(frozen=True, slots=True)
class Binding:
    """How an entity is positioned relative to a reference frame.

    Modes are mutually exclusive:
    - ``at`` — relative position within the reference (or cell)
    - ``along`` + ``t`` — positioned along a Pathable at parameter t

    ``reference`` optionally overrides the default cell as the frame of reference.

    Example:
        ```python
        # Position at 25% x, 75% y within the cell
        entity.binding = Binding(at=RelCoord(0.25, 0.75))

        # Position at center of another entity
        entity.binding = Binding(at=RelCoord(0.5, 0.5), reference=rect)

        # Position along a path at t=0.3
        entity.binding = Binding(along=line, t=0.3)
        ```
    """

    at: RelCoord | None = None
    reference: Surface | Entity | None = None
    along: Pathable | None = None
    t: float = 0.5
    along_offset: float | None = None
