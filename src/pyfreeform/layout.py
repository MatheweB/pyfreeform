"""Layout utilities for relative-first positioning.

All functions work with ``RelCoord`` values — fractions of a surface —
rather than pixel coordinates.  They read ``entity.at`` and
``entity.relative_bounds()`` and write back ``entity.at``, so entities
stay in relative mode after layout operations.

Example::

    from pyfreeform import Scene, align, distribute, between, stack

    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    cell = scene.grid.merge()          # one big merged cell

    dots = [cell.add_dot(at=(0.5, 0.5), color="red") for _ in range(5)]
    distribute(*dots, axis="x", start=0.1, end=0.9)
    align(*dots, anchor="center_y")
"""

from __future__ import annotations

from typing import Literal

from .core.entity import Entity
from .core.relcoord import RelCoord
from .core.surface import Surface
from .core.positions import AnchorSpec

# Types accepted by between()
Locatable = Entity | Surface | RelCoord | tuple[float, float]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _to_relcoord(obj: Locatable, anchor: AnchorSpec = "center") -> RelCoord:
    """Extract a RelCoord from an Entity, Surface, RelCoord, or tuple."""
    if isinstance(obj, RelCoord):
        return obj
    if isinstance(obj, tuple):
        return RelCoord(*obj)
    if isinstance(obj, Entity | Surface):
        return obj.relative_anchor(anchor)
    raise TypeError(
        f"Expected Entity, Surface, RelCoord, or tuple, got {type(obj).__name__}"
    )


def _normalize_entities(args: tuple) -> list[Entity]:
    """Accept *args or a single list/tuple of entities."""
    if len(args) == 1 and isinstance(args[0], list | tuple):
        entities = list(args[0])
    else:
        entities = list(args)
    if len(entities) < 2:
        raise ValueError("Need at least 2 entities")
    for e in entities:
        if not isinstance(e, Entity):
            raise TypeError(
                f"Expected Entity, got {type(e).__name__}. "
                "Layout functions operate on entities, not surfaces or coords."
            )
    return entities


def _reposition(entity: Entity, delta_rx: float, delta_ry: float) -> None:
    """Apply a relative delta to an entity's position.

    Clears any existing binding (along-path, within-reference, etc.)
    and shifts ``entity.at`` by the given amounts.
    """
    at = entity.at or RelCoord(0.5, 0.5)
    entity.binding = None
    entity.at = RelCoord(at.rx + delta_rx, at.ry + delta_ry)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def between(
    a: Locatable,
    b: Locatable,
    t: float = 0.5,
    *,
    anchor: AnchorSpec = "center",
) -> RelCoord:
    """Point between two objects as a ``RelCoord``.

    Interpolates between the relative anchor positions of *a* and *b*.
    The result can be used directly with ``at=``.

    Args:
        a: First object (Entity, Surface, RelCoord, or tuple).
        b: Second object.
        t: Interpolation factor — 0.0 returns *a*, 1.0 returns *b*,
           0.5 (default) is the midpoint.
        anchor: Anchor name or RelCoord used when extracting
                positions from Entity / Surface arguments.

    Returns:
        Interpolated RelCoord.

    Example::

        mid = between(shape, cell, anchor="bottom")
        cell.add_text("Label", at=mid)
    """
    pa = _to_relcoord(a, anchor)
    pb = _to_relcoord(b, anchor)
    return pa.lerp(pb, t)


def align(
    *entities: Entity | list[Entity],
    anchor: Literal["left", "right", "top", "bottom", "center_x", "center_y"] = "center_y",
) -> list[Entity]:
    """Align entities to a shared edge or centerline.

    The first entity is the reference — all others are moved to match
    its value on the specified axis.

    Center anchors (``"center_x"``, ``"center_y"``) adjust
    ``entity.at`` directly.  Edge anchors (``"top"``, ``"bottom"``,
    ``"left"``, ``"right"``) use ``relative_bounds()`` to compute the
    edge positions and shift ``at`` by the delta.

    Args:
        *entities: Two or more entities, or a single list.
        anchor: Alignment axis — one of ``"left"``, ``"right"``,
                ``"top"``, ``"bottom"``, ``"center_x"``,
                ``"center_y"``.

    Returns:
        The entities (for chaining into other calls).

    Raises:
        ValueError: Fewer than 2 entities or invalid anchor.
        TypeError: Non-Entity argument.

    Example::

        align(dot1, dot2, dot3, anchor="center_y")
        align([dot1, dot2, dot3], anchor="left")
    """
    items = _normalize_entities(entities)
    ref = items[0]

    _VALID = {"left", "right", "top", "bottom", "center_x", "center_y"}
    if anchor not in _VALID:
        raise ValueError(
            f"Invalid anchor '{anchor}'. Use one of: {sorted(_VALID)}"
        )

    if anchor in ("center_x", "center_y"):
        ref_center = ref.relative_anchor("center")
        target = ref_center.rx if anchor == "center_x" else ref_center.ry
        for e in items[1:]:
            e_center = e.relative_anchor("center")
            if anchor == "center_x":
                _reposition(e, target - e_center.rx, 0)
            else:
                _reposition(e, 0, target - e_center.ry)
    else:
        # Edge alignment via relative_bounds
        _EDGE_INDEX = {"left": 0, "top": 1, "right": 2, "bottom": 3}
        idx = _EDGE_INDEX[anchor]
        is_x = anchor in ("left", "right")

        ref_rb = ref.relative_bounds()
        target_edge = ref_rb[idx]

        for e in items[1:]:
            e_rb = e.relative_bounds()
            delta = target_edge - e_rb[idx]
            if is_x:
                _reposition(e, delta, 0)
            else:
                _reposition(e, 0, delta)

    return items


def distribute(
    *entities: Entity | list[Entity],
    axis: Literal["x", "y"] = "x",
    start: float = 0.0,
    end: float = 1.0,
) -> list[Entity]:
    """Distribute entities evenly between two relative positions.

    Edge-aware: the first entity's leading edge sits at *start* and the
    last entity's trailing edge sits at *end*, with equal gaps between
    items.  The cross-axis position (``at.ry`` for ``axis="x"``,
    ``at.rx`` for ``axis="y"``) is preserved.

    Args:
        *entities: Two or more entities, or a single list.
        axis: ``"x"`` (horizontal) or ``"y"`` (vertical).
        start: Leading edge of the first entity (default 0.0).
        end: Trailing edge of the last entity (default 1.0).

    Returns:
        The entities in argument order.

    Raises:
        ValueError: Fewer than 2 entities or invalid axis.
        TypeError: Non-Entity argument.

    Example::

        distribute(d1, d2, d3, axis="x", start=0.1, end=0.9)
    """
    items = _normalize_entities(entities)
    if axis not in ("x", "y"):
        raise ValueError(f"axis must be 'x' or 'y', got '{axis}'")

    n = len(items)
    is_x = axis == "x"

    # Measure each entity's size along the distribution axis
    sizes = []
    for e in items:
        rb = e.relative_bounds()
        sizes.append(rb[2] - rb[0] if is_x else rb[3] - rb[1])

    total_size = sum(sizes)
    available = (end - start) - total_size
    gap = available / (n - 1) if n > 1 else 0

    # Place sequentially: leading edge at pos, center at pos + size/2
    pos = start
    for i, e in enumerate(items):
        target_center = pos + sizes[i] / 2
        e_center = e.relative_anchor("center")
        if is_x:
            _reposition(e, target_center - e_center.rx, 0)
        else:
            _reposition(e, 0, target_center - e_center.ry)
        pos += sizes[i] + gap

    return items


def stack(
    *entities: Entity | list[Entity],
    direction: Literal["right", "left", "above", "below"] = "below",
    gap: float = 0.0,
) -> list[Entity]:
    """Stack entities sequentially, accounting for their sizes.

    The first entity stays in place.  Each subsequent entity is
    positioned beside the previous one using ``relative_bounds()``
    to avoid overlap.

    Args:
        *entities: Two or more entities, or a single list.
        direction: ``"right"``, ``"left"``, ``"above"``, or
                   ``"below"``.
        gap: Gap as a fraction of the surface dimension.

    Returns:
        The entities in argument order.

    Raises:
        ValueError: Fewer than 2 entities or invalid direction.
        TypeError: Non-Entity argument.

    Example::

        stack(title, shape, caption, direction="below", gap=0.05)
    """
    items = _normalize_entities(entities)
    valid_dirs = {"right", "left", "above", "below"}
    if direction not in valid_dirs:
        raise ValueError(
            f"Invalid direction '{direction}'. Use one of: {sorted(valid_dirs)}"
        )

    for i in range(1, len(items)):
        prev = items[i - 1]
        curr = items[i]
        prev_rb = prev.relative_bounds()
        curr_rb = curr.relative_bounds()
        curr_rw = curr_rb[2] - curr_rb[0]
        curr_rh = curr_rb[3] - curr_rb[1]

        if direction == "right":
            target_cx = prev_rb[2] + gap + curr_rw / 2
            target_cy = (prev_rb[1] + prev_rb[3]) / 2
        elif direction == "left":
            target_cx = prev_rb[0] - gap - curr_rw / 2
            target_cy = (prev_rb[1] + prev_rb[3]) / 2
        elif direction == "below":
            target_cx = (prev_rb[0] + prev_rb[2]) / 2
            target_cy = prev_rb[3] + gap + curr_rh / 2
        else:  # above
            target_cx = (prev_rb[0] + prev_rb[2]) / 2
            target_cy = prev_rb[1] - gap - curr_rh / 2

        curr_center = curr.relative_anchor("center")
        _reposition(curr, target_cx - curr_center.rx, target_cy - curr_center.ry)

    return items
