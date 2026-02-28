"""Reactive animation synthesis — polygon vertex and connection endpoint tracking.

When polygon vertices or connection endpoints reference entities with
``.move()`` animations, this module synthesizes SMIL ``<animate>``
elements that make the shape follow the moving entities.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Callable

from ..animation.models import PropertyAnimation
from ..core.coord import Coord
from ..core.entity import Entity
from ..core.svg_utils import svg_num
from .smil_elements import build_animate_element

if TYPE_CHECKING:
    from ..core.connection import Connection

# A vertex/endpoint spec: raw Coord, Entity, or (Entity, anchor_name) tuple.
VertexSpec = Coord | Entity | tuple[Entity, str]


# ======================================================================
# Position animation extraction
# ======================================================================


def extract_position_anims(
    entity: Entity,
) -> tuple[PropertyAnimation, PropertyAnimation] | None:
    """Extract the first (at_rx, at_ry) animation pair from an entity.

    Returns ``None`` if the entity has no position (move) animations.
    """
    rx_anim: PropertyAnimation | None = None
    ry_anim: PropertyAnimation | None = None
    for anim in entity._animations:
        if isinstance(anim, PropertyAnimation):
            if anim.prop == "at_rx" and rx_anim is None:
                rx_anim = anim
            elif anim.prop == "at_ry" and ry_anim is None:
                ry_anim = anim
        if rx_anim is not None and ry_anim is not None:
            return (rx_anim, ry_anim)
    return None


def resolve_abs_position(
    entity: Entity, rx: float, ry: float,
) -> tuple[float, float]:
    """Convert relative (rx, ry) to absolute pixels using entity's surface."""
    surface = entity._surface
    if surface is None:
        return (rx, ry)
    return (
        surface._x + rx * surface._width,
        surface._y + ry * surface._height,
    )


# ======================================================================
# Animation compatibility and timing
# ======================================================================


def check_anim_compatibility(
    anims: list[PropertyAnimation],
) -> PropertyAnimation | None:
    """Verify all animations share compatible timing; return template or None."""
    if not anims:
        return None
    template = anims[0]
    for a in anims[1:]:
        if (
            a.duration != template.duration
            or a.delay != template.delay
            or a.easing != template.easing
            or a.bounce != template.bounce
            or a.repeat != template.repeat
            or len(a.keyframes) != len(template.keyframes)
        ):
            return None
    return template


def compute_cycle_duration(
    anims: list[PropertyAnimation],
) -> tuple[float, bool]:
    """Compute a unified cycle duration and repeat flag for mixed-timing animations.

    Returns:
        (duration, all_repeat): The cycle duration in seconds and whether
        all animations repeat (so the unified animation should too).
    """
    if not anims:
        return (1.0, False)

    all_repeat = all(a.repeat for a in anims)

    if not all_repeat:
        return (max(a.delay + a.duration for a in anims), False)

    durations = [a.duration for a in anims if a.duration > 0]
    if not durations:
        return (1.0, True)

    # Convert to centiseconds for integer LCM (avoids float imprecision)
    cs_values = [max(1, round(d * 100)) for d in durations]
    result = cs_values[0]
    for v in cs_values[1:]:
        result = abs(result * v) // math.gcd(result, v)

    # Cap at 30 seconds to avoid huge SVGs
    return (min(result / 100.0, 30.0), True)


# ======================================================================
# Vertex / endpoint resolution
# ======================================================================


AnimPair = tuple[PropertyAnimation, PropertyAnimation]


def _resolve_vertex(
    spec: VertexSpec,
    pair: AnimPair | None,
    get_value: Callable[[PropertyAnimation], float],
) -> Coord:
    """Resolve a vertex/endpoint spec to absolute Coord.

    The *get_value* callable extracts a coordinate value from a
    PropertyAnimation (e.g. a keyframe lookup or time-based evaluation).
    """
    if isinstance(spec, Coord):
        return spec
    if pair is not None:
        entity = spec if isinstance(spec, Entity) else spec[0]
        rx, ry = get_value(pair[0]), get_value(pair[1])
        ax, ay = resolve_abs_position(entity, rx, ry)
        return Coord(ax, ay)
    if isinstance(spec, Entity):
        return spec.position
    return spec[0].anchor(spec[1])


def resolve_vertex_at_keyframe(
    spec: VertexSpec, pair: AnimPair | None, keyframe_index: int,
) -> Coord:
    """Resolve a vertex spec to absolute Coord at a specific keyframe index."""
    return _resolve_vertex(spec, pair, lambda a: a.keyframes[keyframe_index].value)


def resolve_vertex_at_time(
    spec: VertexSpec, pair: AnimPair | None, t: float,
) -> Coord:
    """Resolve a vertex spec to absolute Coord at a given time (with easing)."""
    return _resolve_vertex(spec, pair, lambda a: a.evaluate(t))


# ======================================================================
# Animate element builders (reactive-specific)
# ======================================================================


def build_reactive_animate(
    svg_attr: str,
    val_list: list[str],
    template: PropertyAnimation,
) -> str:
    """Build a single ``<animate>`` from pre-computed values and a template animation."""
    dur = template.duration
    base = template.keyframes[0].time if template.keyframes else 0
    kt_list = [(kf.time - base) / dur if dur > 0 else 0 for kf in template.keyframes]

    return build_animate_element(
        attribute_name=svg_attr,
        values=val_list, key_times=kt_list,
        duration=template.duration, delay=template.delay,
        easing=template.easing, bounce=template.bounce,
        hold=template.hold, repeat=template.repeat,
    )


def build_resampled_animate(
    svg_attr: str,
    val_list: list[str],
    key_times: list[float],
    duration: float,
    delay: float,
    repeat: bool | int,
) -> str:
    """Build an ``<animate>`` from pre-eased sample values (calcMode="linear")."""
    return build_animate_element(
        attribute_name=svg_attr,
        values=val_list, key_times=key_times,
        duration=duration, delay=delay,
        easing=None,  # pre-baked
        hold=True, repeat=repeat,
    )


# ======================================================================
# Connection path geometry
# ======================================================================


def connection_path_d_at(conn: Connection, start: Coord, end: Coord) -> str:
    """Compute connection SVG path ``d`` for arbitrary start/end points."""
    if conn._shape_kind == "line":
        return (
            f"M {svg_num(start.x)} {svg_num(start.y)}"
            f" L {svg_num(end.x)} {svg_num(end.y)}"
        )

    ss, se = conn._source_start, conn._source_end
    if ss is None or se is None:
        return (
            f"M {svg_num(start.x)} {svg_num(start.y)}"
            f" L {svg_num(end.x)} {svg_num(end.y)}"
        )

    src_dx, src_dy = se.x - ss.x, se.y - ss.y
    src_len = math.hypot(src_dx, src_dy)
    if src_len < 1e-9:
        return f"M {svg_num(start.x)} {svg_num(start.y)} L {svg_num(start.x)} {svg_num(start.y)}"

    tgt_dx, tgt_dy = end.x - start.x, end.y - start.y
    tgt_len = math.hypot(tgt_dx, tgt_dy)
    scale = tgt_len / src_len

    src_angle = math.atan2(src_dy, src_dx)
    tgt_angle = math.atan2(tgt_dy, tgt_dx)
    rot = tgt_angle - src_angle
    cos_r, sin_r = math.cos(rot), math.sin(rot)

    def transform(p: Coord) -> Coord:
        dx = p.x - ss.x
        dy = p.y - ss.y
        rx = scale * (cos_r * dx - sin_r * dy)
        ry = scale * (sin_r * dx + cos_r * dy)
        return Coord(start.x + rx, start.y + ry)

    first = transform(conn._shape_beziers[0][0])
    parts = [f"M {svg_num(first.x)} {svg_num(first.y)}"]
    for _, cp1, cp2, p3 in conn._shape_beziers:
        tcp1, tcp2, tp3 = transform(cp1), transform(cp2), transform(p3)
        parts.append(
            f" C {svg_num(tcp1.x)} {svg_num(tcp1.y)}"
            f" {svg_num(tcp2.x)} {svg_num(tcp2.y)}"
            f" {svg_num(tp3.x)} {svg_num(tp3.y)}"
        )
    return "".join(parts)
