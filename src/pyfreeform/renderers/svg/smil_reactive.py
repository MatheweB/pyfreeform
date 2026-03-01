"""Reactive animation synthesis — polygon vertex and connection endpoint tracking.

When polygon vertices or connection endpoints reference entities with
``.animate_move()`` animations, this module synthesizes SMIL ``<animate>``
elements that make the shape follow the moving entities.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import TYPE_CHECKING

from ...animation.models import Easing, PropertyAnimation, _apply_repeat, _interpolate
from ...core.coord import Coord
from ...core.entity import Entity
from ...core.svg_utils import svg_num
from .smil_elements import build_animate_element

if TYPE_CHECKING:
    from ...core.connection import Connection
    from ...entities.polygon import Polygon

# A vertex/endpoint spec: raw Coord, Entity, or (Entity, anchor_name) tuple.
VertexSpec = Coord | Entity | tuple[Entity, str]


# ======================================================================
# Easing lookup table — replaces Newton-Raphson with O(1) interpolation
# ======================================================================

_TABLE_SIZE = 256
_easing_tables: dict[tuple[float, float, float, float], list[float]] = {}


def _get_easing_table(easing: Easing) -> list[float]:
    """Return a pre-computed lookup table for the given easing curve.

    The table maps uniform input t in [0, 1] to eased output at
    ``_TABLE_SIZE + 1`` evenly spaced points.  Subsequent lookups use
    linear interpolation — constant time instead of Newton-Raphson.
    """
    key = (easing.x1, easing.x2, easing.y1, easing.y2)
    table = _easing_tables.get(key)
    if table is not None:
        return table
    n = _TABLE_SIZE
    table = [easing.evaluate(i / n) for i in range(n + 1)]
    _easing_tables[key] = table
    return table


def _easing_lookup(table: list[float], t: float) -> float:
    """Look up eased value from a pre-computed table with linear interpolation."""
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    idx_f = t * _TABLE_SIZE
    idx = int(idx_f)
    frac = idx_f - idx
    return table[idx] + (table[idx + 1] - table[idx]) * frac


def fast_evaluate(anim: PropertyAnimation, t: float, table: list[float]) -> float:
    """Evaluate a PropertyAnimation at time *t* using a pre-computed easing table.

    Replicates ``PropertyAnimation.evaluate()`` logic but replaces the
    per-call Newton-Raphson easing solve with a constant-time table lookup.
    """
    kfs = anim.keyframes
    n_kf = len(kfs)
    if n_kf < 2:
        return kfs[0].value if kfs else 0.0

    dur = anim.duration
    if dur <= 0:
        return kfs[-1].value

    t = t - anim.delay
    if t < 0:
        return kfs[0].value

    t = _apply_repeat(t, dur, anim.repeat, anim.bounce)
    if t is None:
        return kfs[-1].value if anim.hold else kfs[0].value

    base_time = kfs[0].time
    for i in range(n_kf - 1):
        kf0 = kfs[i]
        kf1 = kfs[i + 1]
        if t <= kf1.time - base_time:
            seg_dur = kf1.time - kf0.time
            if seg_dur <= 0:
                return kf1.value
            local_t = (t - (kf0.time - base_time)) / seg_dur
            eased_t = _easing_lookup(table, local_t)
            return _interpolate(kf0.value, kf1.value, eased_t)

    return kfs[-1].value


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


def check_delay_only_mismatch(
    anims: list[PropertyAnimation],
) -> tuple[PropertyAnimation, float] | None:
    """Check if animations match on everything except delay.

    Returns ``(template, avg_delay)`` if all animations share the same
    duration, easing, bounce, repeat, and keyframe count — differing
    only in delay.  Returns ``None`` otherwise.
    """
    if not anims:
        return None
    ref = anims[0]
    total_delay = ref.delay
    for a in anims[1:]:
        if (
            a.duration != ref.duration
            or a.easing != ref.easing
            or a.bounce != ref.bounce
            or a.repeat != ref.repeat
            or len(a.keyframes) != len(ref.keyframes)
        ):
            return None
        total_delay += a.delay
    return (ref, total_delay / len(anims))


def compute_cycle_duration(
    anims: list[PropertyAnimation],
) -> tuple[float, bool]:
    """Compute a unified cycle duration and repeat flag for mixed-timing animations.

    When animations bounce, the effective period is ``2 * duration``
    (forward + backward), so the cycle must cover the full round-trip.

    Returns:
        (duration, all_repeat): The cycle duration in seconds and whether
        all animations repeat (so the unified animation should too).
    """
    if not anims:
        return (1.0, False)

    all_repeat = all(a.repeat for a in anims)

    if not all_repeat:
        return (max(a.delay + a.duration for a in anims), False)

    # Effective period per animation: 2*dur if bouncing, dur otherwise
    periods = [
        a.duration * (2 if a.bounce else 1) for a in anims if a.duration > 0
    ]
    if not periods:
        return (1.0, True)

    # Convert to centiseconds for integer LCM (avoids float imprecision)
    cs_values = [max(1, round(p * 100)) for p in periods]
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


def resolve_vertex_at_time_fast(
    spec: VertexSpec, pair: AnimPair | None, t: float,
    table: list[float],
) -> Coord:
    """Like ``resolve_vertex_at_time`` but uses a pre-computed easing table."""
    return _resolve_vertex(spec, pair, lambda a: fast_evaluate(a, t, table))


# ======================================================================
# Animate element builders (reactive-specific)
# ======================================================================


def build_reactive_animate(
    svg_attr: str,
    val_list: list[str],
    template: PropertyAnimation,
    *,
    delay: float | None = None,
) -> str:
    """Build a single ``<animate>`` from pre-computed values and a template animation.

    All timing parameters are taken from *template*.  Pass *delay* to
    override the template's delay (used by the delay-only fast path
    to set a per-polygon start offset).
    """
    dur = template.duration
    base = template.keyframes[0].time if template.keyframes else 0
    kt_list = [(kf.time - base) / dur if dur > 0 else 0 for kf in template.keyframes]

    return build_animate_element(
        attribute_name=svg_attr,
        values=val_list, key_times=kt_list,
        duration=template.duration,
        delay=delay if delay is not None else template.delay,
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


# ======================================================================
# Reactive polygon animation orchestration
# ======================================================================


def reactive_polygon_anims(polygon: Polygon) -> list[str]:
    """Synthesize ``<animate attributeName="points">`` from animated vertex entities.

    Pure function — all heavy lifting delegated to helpers in this module.
    """
    # Classify each vertex: (anim_pair | None, spec)
    vertex_info: list[tuple[AnimPair | None, VertexSpec]] = []
    all_rx_anims: list[PropertyAnimation] = []

    for spec in polygon._vertex_specs:
        entity: Entity | None = None
        if isinstance(spec, Entity):
            entity = spec
        elif isinstance(spec, tuple) and isinstance(spec[0], Entity):
            entity = spec[0]

        if entity is not None:
            pair = extract_position_anims(entity)
            vertex_info.append((pair, spec))
            if pair is not None:
                all_rx_anims.append(pair[0])
        else:
            vertex_info.append((None, spec))

    if not all_rx_anims:
        return []

    # Fast path: all animations share identical timing, OR same
    # timing with different delays (delay-only mismatch).  The
    # delay-only case uses the average delay as a per-polygon
    # start offset — the tiny per-vertex delay difference within
    # one polygon is invisible, while per-polygon offsets create
    # the visible ripple effect.
    template = check_anim_compatibility(all_rx_anims)
    avg_delay: float | None = None
    if template is None:
        delay_result = check_delay_only_mismatch(all_rx_anims)
        if delay_result is not None:
            template, avg_delay = delay_result

    if template is not None:
        n_keyframes = len(template.keyframes)
        val_list: list[str] = []
        for k in range(n_keyframes):
            pts: list[str] = []
            for pair, spec in vertex_info:
                c = resolve_vertex_at_keyframe(spec, pair, k)
                pts.append(f"{svg_num(c.x)},{svg_num(c.y)}")
            val_list.append(" ".join(pts))
        return [build_reactive_animate(
            "points", val_list, template, delay=avg_delay,
        )]

    # Slow path: mixed timing — resample all animations onto a unified timeline.
    # Each vertex's easing/bounce/repeat is baked into the sampled values.
    # Uses a pre-computed easing lookup table for O(1) evaluation instead
    # of per-call Newton-Raphson — critical for large grids (10 000+ polygons).
    all_anims = []
    for pair, _ in vertex_info:
        if pair is not None:
            all_anims.extend(pair)
    cycle, all_repeat = compute_cycle_duration(all_anims)
    n_samples = max(2, min(120, int(cycle * 20)))

    # Build easing table once — shared across all vertices
    easing_table = _get_easing_table(all_anims[0].easing) if all_anims else []

    val_list_r: list[str] = []
    key_times: list[float] = []
    for i in range(n_samples):
        t = i * cycle / (n_samples - 1) if n_samples > 1 else 0.0
        key_times.append(t / cycle if cycle > 0 else 0.0)
        pts: list[str] = []
        for pair, spec in vertex_info:
            c = resolve_vertex_at_time_fast(spec, pair, t, easing_table)
            pts.append(f"{svg_num(c.x)},{svg_num(c.y)}")
        val_list_r.append(" ".join(pts))

    return [build_resampled_animate("points", val_list_r, key_times,
                                    cycle, 0.0, all_repeat)]


# ======================================================================
# Reactive connection animation orchestration
# ======================================================================


def reactive_connection_anims(conn: Connection) -> list[str]:
    """Synthesize SMIL elements from animated connection endpoints.

    Pure function — dispatches to line or path helpers below.
    """
    start_pair = extract_position_anims(conn._start) if isinstance(conn._start, Entity) else None
    end_pair = extract_position_anims(conn._end) if isinstance(conn._end, Entity) else None

    if start_pair is None and end_pair is None:
        return []

    rx_anims: list[PropertyAnimation] = []
    if start_pair:
        rx_anims.append(start_pair[0])
    if end_pair:
        rx_anims.append(end_pair[0])

    # Fast path: identical timing, or same timing with different delays
    template = check_anim_compatibility(rx_anims)
    if template is None:
        delay_result = check_delay_only_mismatch(rx_anims)
        if delay_result is not None:
            template, _ = delay_result  # avg_delay unused — endpoints are few

    if template is not None:
        n_kf = len(template.keyframes)
        if conn._shape_kind == "line":
            return _reactive_line_anims(conn, start_pair, end_pair, template, n_kf)
        return _reactive_path_anims(conn, start_pair, end_pair, template, n_kf)

    # Slow path: mixed timing — resample onto unified timeline
    all_anims: list[PropertyAnimation] = []
    if start_pair:
        all_anims.extend(start_pair)
    if end_pair:
        all_anims.extend(end_pair)
    cycle, all_repeat = compute_cycle_duration(all_anims)
    n_samples = max(2, min(120, int(cycle * 20)))
    easing_table = _get_easing_table(all_anims[0].easing) if all_anims else []

    if conn._shape_kind == "line":
        return _reactive_line_anims_resampled(
            conn, start_pair, end_pair, cycle, n_samples, all_repeat,
            easing_table,
        )
    return _reactive_path_anims_resampled(
        conn, start_pair, end_pair, cycle, n_samples, all_repeat,
        easing_table,
    )


# ── Connection fast-path helpers ──────────────────────────────────────


def _reactive_line_anims(
    conn: Connection,
    start_pair: AnimPair | None,
    end_pair: AnimPair | None,
    template: PropertyAnimation, n_kf: int,
) -> list[str]:
    """Synthesize x1/y1/x2/y2 animations for a straight-line connection."""
    result: list[str] = []

    if start_pair:
        x1_vals, y1_vals = [], []
        for k in range(n_kf):
            c = resolve_vertex_at_keyframe(conn._start, start_pair, k)
            x1_vals.append(svg_num(c.x))
            y1_vals.append(svg_num(c.y))
        result.append(build_reactive_animate("x1", x1_vals, template))
        result.append(build_reactive_animate("y1", y1_vals, template))

    if end_pair:
        x2_vals, y2_vals = [], []
        for k in range(n_kf):
            c = resolve_vertex_at_keyframe(conn._end, end_pair, k)
            x2_vals.append(svg_num(c.x))
            y2_vals.append(svg_num(c.y))
        result.append(build_reactive_animate("x2", x2_vals, template))
        result.append(build_reactive_animate("y2", y2_vals, template))

    return result


def _reactive_path_anims(
    conn: Connection,
    start_pair: AnimPair | None,
    end_pair: AnimPair | None,
    template: PropertyAnimation, n_kf: int,
) -> list[str]:
    """Synthesize ``d`` animation for a curved/path connection."""
    d_vals: list[str] = []
    for k in range(n_kf):
        start_k = resolve_vertex_at_keyframe(conn._start, start_pair, k) if start_pair else conn.start_point
        end_k = resolve_vertex_at_keyframe(conn._end, end_pair, k) if end_pair else conn.end_point
        d_vals.append(connection_path_d_at(conn, start_k, end_k))

    return [build_reactive_animate("d", d_vals, template)]


# ── Connection resampled helpers (mixed timing) ──────────────────────


def _reactive_line_anims_resampled(
    conn: Connection,
    start_pair: AnimPair | None,
    end_pair: AnimPair | None,
    cycle: float, n_samples: int, all_repeat: bool,
    easing_table: list[float],
) -> list[str]:
    """Resampled x1/y1/x2/y2 animations for mixed-timing line connections."""
    result: list[str] = []
    key_times: list[float] = []
    x1_vals: list[str] = []
    y1_vals: list[str] = []
    x2_vals: list[str] = []
    y2_vals: list[str] = []

    for i in range(n_samples):
        t = i * cycle / (n_samples - 1) if n_samples > 1 else 0.0
        key_times.append(t / cycle if cycle > 0 else 0.0)

        sp = resolve_vertex_at_time_fast(conn._start, start_pair, t, easing_table) if start_pair else conn.start_point
        ep = resolve_vertex_at_time_fast(conn._end, end_pair, t, easing_table) if end_pair else conn.end_point

        if start_pair:
            x1_vals.append(svg_num(sp.x))
            y1_vals.append(svg_num(sp.y))
        if end_pair:
            x2_vals.append(svg_num(ep.x))
            y2_vals.append(svg_num(ep.y))

    if start_pair:
        result.append(build_resampled_animate("x1", x1_vals, key_times, cycle, 0.0, all_repeat))
        result.append(build_resampled_animate("y1", y1_vals, key_times, cycle, 0.0, all_repeat))
    if end_pair:
        result.append(build_resampled_animate("x2", x2_vals, key_times, cycle, 0.0, all_repeat))
        result.append(build_resampled_animate("y2", y2_vals, key_times, cycle, 0.0, all_repeat))

    return result


def _reactive_path_anims_resampled(
    conn: Connection,
    start_pair: AnimPair | None,
    end_pair: AnimPair | None,
    cycle: float, n_samples: int, all_repeat: bool,
    easing_table: list[float],
) -> list[str]:
    """Resampled ``d`` animation for mixed-timing curved connections."""
    d_vals: list[str] = []
    key_times: list[float] = []

    for i in range(n_samples):
        t = i * cycle / (n_samples - 1) if n_samples > 1 else 0.0
        key_times.append(t / cycle if cycle > 0 else 0.0)

        sp = resolve_vertex_at_time_fast(conn._start, start_pair, t, easing_table) if start_pair else conn.start_point
        ep = resolve_vertex_at_time_fast(conn._end, end_pair, t, easing_table) if end_pair else conn.end_point
        d_vals.append(connection_path_d_at(conn, sp, ep))

    return [build_resampled_animate("d", d_vals, key_times, cycle, 0.0, all_repeat)]
