"""Animation model → SMIL string conversion.

Standalone functions that convert :mod:`~pyfreeform.animation.models`
objects (PropertyAnimation, MotionAnimation, DrawAnimation) into SVG
SMIL element strings.  These are pure functions — no renderer instance
needed — used by :class:`~pyfreeform.renderers.svg.smil.SMILRenderer`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...animation.models import (
    DrawAnimation,
    Easing,
    MotionAnimation,
    PropertyAnimation,
)
from ...color import Color
from ...core.entity import Entity
from ...core.svg_utils import svg_num
from .smil_elements import (
    build_animate_element,
    format_value,
    smil_easing_n,
    smil_repeat,
)

if TYPE_CHECKING:
    from ...core.connection import Connection


# ======================================================================
# Fill-to-opacity layer optimization
# ======================================================================


@dataclass(frozen=True, slots=True)
class FillLayerOpt:
    """Data for rendering a fill animation as stacked opacity layers.

    Instead of a single ``<animate attributeName="fill">`` (CPU-bound color
    interpolation), the renderer emits N ``<polygon>`` elements — one base
    with the first color, plus one overlay per additional color with an
    opacity animation.  GPU-accelerated opacity compositing replaces
    per-frame color string parsing.
    """

    base_color: str
    """Fill color for the base polygon (first keyframe color)."""

    overlays: list[tuple[str, list[float]]]
    """(color, opacity_per_keyframe) for each overlay, ordered by first appearance."""

    anim: PropertyAnimation
    """Original fill animation (timing source for synthesized opacity animations)."""

    anim_index: int
    """Index in ``entity._animations`` so the fill anim can be excluded."""


def extract_fill_layers(
    entity: Entity, target_attr: str = "fill",
) -> FillLayerOpt | None:
    """Detect a color animation suitable for opacity-layer optimization.

    Works for both ``fill`` animations (entities) and ``stroke`` color
    animations (connections).  Pass ``target_attr="stroke"`` for stroke
    color optimization.

    Returns :class:`FillLayerOpt` if the entity has exactly one color
    ``PropertyAnimation`` targeting *target_attr* using solid colors and
    no conflicting opacity animations.  Returns ``None`` otherwise
    (caller falls back to standard animation rendering).
    """
    entity_type = type(entity).__name__

    fill_anim: PropertyAnimation | None = None
    fill_index: int = -1

    for i, anim in enumerate(entity._animations):
        if not isinstance(anim, PropertyAnimation):
            continue
        # Conflict: any opacity animation would fight the overlay
        if anim.prop in ("opacity", "fill_opacity", "stroke_opacity"):
            return None
        svg_attr = _resolve_svg_attr(entity_type, anim.prop)
        if svg_attr == target_attr:
            if fill_anim is not None:
                return None  # multiple color animations
            fill_anim = anim
            fill_index = i

    if fill_anim is None or len(fill_anim.keyframes) < 2:
        return None

    # Normalize colors — reject gradients and unparseable values
    try:
        normalized = []
        for kf in fill_anim.keyframes:
            val = str(kf.value)
            if val.startswith("url("):
                return None
            normalized.append(Color(val).to_hex())
    except (ValueError, TypeError):
        return None

    # Need at least 2 unique colors for the optimization to matter
    unique_ordered: list[str] = []
    seen: set[str] = set()
    for c in normalized:
        if c not in seen:
            unique_ordered.append(c)
            seen.add(c)
    if len(unique_ordered) < 2:
        return None

    base_color = unique_ordered[0]
    overlays: list[tuple[str, list[float]]] = []
    for color in unique_ordered[1:]:
        opacities = [1.0 if c == color else 0.0 for c in normalized]
        overlays.append((color, opacities))

    return FillLayerOpt(
        base_color=base_color,
        overlays=overlays,
        anim=fill_anim,
        anim_index=fill_index,
    )


# ======================================================================
# Property name → SVG attribute mapping
# ======================================================================

# Maps (entity_class_name, pyfreeform_prop) → svg_attribute_name
# Falls back to (None, prop) for universal properties.
_PROP_TO_SVG: dict[tuple[str | None, str], str] = {
    # Universal
    (None, "opacity"): "opacity",
    (None, "fill_opacity"): "fill-opacity",
    (None, "stroke_opacity"): "stroke-opacity",
    # Dot
    ("Dot", "r"): "r",
    ("Dot", "radius"): "r",
    ("Dot", "color"): "fill",
    ("Dot", "cx"): "cx",
    ("Dot", "cy"): "cy",
    # Rect
    ("Rect", "fill"): "fill",
    ("Rect", "stroke"): "stroke",
    ("Rect", "width"): "width",
    ("Rect", "height"): "height",
    ("Rect", "x"): "x",
    ("Rect", "y"): "y",
    ("Rect", "stroke_width"): "stroke-width",
    # Ellipse
    ("Ellipse", "rx"): "rx",
    ("Ellipse", "ry"): "ry",
    ("Ellipse", "fill"): "fill",
    ("Ellipse", "stroke"): "stroke",
    ("Ellipse", "cx"): "cx",
    ("Ellipse", "cy"): "cy",
    # Line
    ("Line", "x1"): "x1",
    ("Line", "y1"): "y1",
    ("Line", "x2"): "x2",
    ("Line", "y2"): "y2",
    ("Line", "color"): "stroke",
    ("Line", "width"): "stroke-width",
    # Curve
    ("Curve", "color"): "stroke",
    ("Curve", "width"): "stroke-width",
    # Text
    ("Text", "color"): "fill",
    ("Text", "font_size"): "font-size",
    ("Text", "x"): "x",
    ("Text", "y"): "y",
    # Polygon
    ("Polygon", "fill"): "fill",
    ("Polygon", "stroke"): "stroke",
    ("Polygon", "stroke_width"): "stroke-width",
    # Path
    ("Path", "color"): "stroke",
    ("Path", "width"): "stroke-width",
    ("Path", "fill"): "fill",
    # Connection
    ("Connection", "color"): "stroke",
    ("Connection", "opacity"): "opacity",
    ("Connection", "width"): "stroke-width",
}


def _resolve_svg_attr(entity_type: str, prop: str) -> str | None:
    """Resolve a pyfreeform property name to an SVG attribute name."""
    key = (entity_type, prop)
    if key in _PROP_TO_SVG:
        return _PROP_TO_SVG[key]
    universal = (None, prop)
    if universal in _PROP_TO_SVG:
        return _PROP_TO_SVG[universal]
    return None


# ======================================================================
# Shared helpers
# ======================================================================


def _anim_key_times(anim: PropertyAnimation) -> list[float]:
    """Compute normalized [0..1] keyTimes from animation keyframes."""
    dur = anim.duration
    base = anim.keyframes[0].time if anim.keyframes else 0
    return [(kf.time - base) / dur if dur > 0 else 0 for kf in anim.keyframes]


def _transform_common(anim: PropertyAnimation) -> dict:
    """Shared timing kwargs for ``<animateTransform>`` elements."""
    return dict(
        tag="animateTransform",
        attribute_name="transform",
        key_times=_anim_key_times(anim),
        duration=anim.duration, delay=anim.delay,
        easing=anim.easing, bounce=anim.bounce,
        hold=anim.hold, repeat=anim.repeat,
    )


# ======================================================================
# PropertyAnimation converters
# ======================================================================


def render_property_smil(anim: PropertyAnimation, entity: Entity) -> list[str]:
    """Render a PropertyAnimation as one or more SMIL elements."""
    entity_type = type(entity).__name__

    if anim.prop == "rotation":
        return [_render_rotation_smil(anim, entity)]
    if anim.prop in ("scale", "scale_factor"):
        return _render_scale_smil(anim, entity)
    if anim.prop in ("at_rx", "at_ry"):
        return [_render_position_smil(anim, entity)]

    svg_attr = _resolve_svg_attr(entity_type, anim.prop) or anim.prop
    return [build_animate_element(
        attribute_name=svg_attr,
        values=[format_value(kf.value) for kf in anim.keyframes],
        key_times=_anim_key_times(anim),
        duration=anim.duration, delay=anim.delay,
        easing=anim.easing, bounce=anim.bounce,
        hold=anim.hold, repeat=anim.repeat,
    )]


def _render_rotation_smil(anim: PropertyAnimation, entity: Entity) -> str:
    """Render rotation as ``<animateTransform type="rotate">``."""
    center = entity.rotation_center
    cx, cy = svg_num(center.x), svg_num(center.y)
    return build_animate_element(
        **_transform_common(anim),
        values=[f"{svg_num(kf.value)} {cx} {cy}" for kf in anim.keyframes],
        extra_attrs=' type="rotate" additive="sum"',
    )


def _render_scale_smil(anim: PropertyAnimation, entity: Entity) -> list[str]:
    """Scale around entity center via translate + scale + translate.

    SVG SMIL ``type="scale"`` scales from (0, 0). We emit three
    synchronized elements for the classic
    ``translate(cx,cy) scale(s) translate(-cx,-cy)`` pattern.
    """
    center = entity.rotation_center
    cx, cy = svg_num(center.x), svg_num(center.y)
    ncx, ncy = svg_num(-center.x), svg_num(-center.y)
    n = len(anim.keyframes)
    common = _transform_common(anim)
    return [
        build_animate_element(
            **common, values=[f"{cx} {cy}"] * n,
            extra_attrs=' type="translate" additive="sum"',
        ),
        build_animate_element(
            **common, values=[svg_num(kf.value) for kf in anim.keyframes],
            extra_attrs=' type="scale" additive="sum"',
        ),
        build_animate_element(
            **common, values=[f"{ncx} {ncy}"] * n,
            extra_attrs=' type="translate" additive="sum"',
        ),
    ]


def _render_position_smil(anim: PropertyAnimation, entity: Entity) -> str:
    """Render a relative position animation as ``<animate>`` on cx/cy or x/y."""
    entity_type = type(entity).__name__
    is_x = anim.prop == "at_rx"

    center_attr = "cx" if is_x else "cy"
    fallback_attr = "x" if is_x else "y"
    svg_attr = _resolve_svg_attr(entity_type, center_attr) or _resolve_svg_attr(entity_type, fallback_attr) or center_attr

    surface = entity._surface
    if surface:
        offset = surface._x if is_x else surface._y
        scale = surface._width if is_x else surface._height
        val_list = [svg_num(offset + kf.value * scale) for kf in anim.keyframes]
    else:
        val_list = [svg_num(kf.value) for kf in anim.keyframes]

    return build_animate_element(
        attribute_name=svg_attr,
        values=val_list,
        key_times=_anim_key_times(anim),
        duration=anim.duration, delay=anim.delay,
        easing=anim.easing, bounce=anim.bounce,
        hold=anim.hold, repeat=anim.repeat,
    )


# ======================================================================
# MotionAnimation converter
# ======================================================================


def _translate_path_d(path_d: str, dx: float, dy: float) -> str:
    """Translate all coordinates in an SVG path data string by (dx, dy).

    Handles absolute M, C, L, Q, S, T, A commands and Z (no coords).
    """
    import re

    tokens = re.split(r"(\s+|,)", path_d)
    result: list[str] = []
    coord_idx = 0  # alternates 0=x, 1=y

    for tok in tokens:
        stripped = tok.strip().rstrip(",")
        if not stripped:
            result.append(tok)
            continue
        if stripped in ("M", "C", "L", "Q", "S", "T", "H", "V", "A", "Z"):
            result.append(tok)
            coord_idx = 0
            continue
        try:
            val = float(stripped)
            if coord_idx % 2 == 0:
                val += dx
            else:
                val += dy
            coord_idx += 1
            result.append(svg_num(val))
        except ValueError:
            result.append(tok)

    return "".join(result)


def render_motion_smil(anim: MotionAnimation) -> str:
    """Render a MotionAnimation as ``<animateMotion>``.

    The path is translated so it starts at the origin (0, 0) because
    ``<animateMotion>`` applies the path as an offset from the element's
    current position.
    """
    path_d = anim.path.to_svg_path_d()

    # Translate path so it starts at (0, 0) — animateMotion adds the path
    # coordinates as an offset from the element's current position.
    start = anim.path.point_at(0.0)
    path_d = _translate_path_d(path_d, -start.x, -start.y)

    rotate_attr = ""
    if anim.rotate is True:
        rotate_attr = ' rotate="auto"'
    elif isinstance(anim.rotate, int | float) and anim.rotate:
        rotate_attr = f' rotate="{svg_num(anim.rotate)}"'

    parts = [f'<animateMotion dur="{anim.duration}s"']

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    if anim.bounce:
        parts.append(' keyPoints="0;1;0"')
        parts.append(' keyTimes="0;0.5;1"')
        if anim.easing == Easing.LINEAR:
            parts.append(' calcMode="linear"')
        else:
            spline = f"{anim.easing.x1} {anim.easing.y1} {anim.easing.x2} {anim.easing.y2}"
            parts.append(f' calcMode="spline" keySplines="{spline};{spline}"')
    else:
        parts.append(smil_easing_n(anim.easing, 1))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(smil_repeat(anim.repeat))
    parts.append(rotate_attr)
    parts.append(f' path="{path_d}" />')
    return "".join(parts)


# ======================================================================
# DrawAnimation converter
# ======================================================================


def render_draw_smil(anim: DrawAnimation, entity: Entity | Connection) -> str:
    """Render a DrawAnimation as stroke-dashoffset ``<animate>``.

    Uses ``pathLength="1"`` on the parent element so dash values are
    normalized to ``[0, 1]`` — no arc-length mismatch between Python
    and the browser, which eliminates round-cap flash artifacts.
    """
    length = entity.arc_length() if hasattr(entity, "arc_length") else 0
    if length <= 0:
        return ""

    from_val = "1" if not anim.reverse else "0"
    to_val = "0" if not anim.reverse else "1"

    if anim.bounce:
        return build_animate_element(
            attribute_name="stroke-dashoffset",
            values=[from_val, to_val, from_val],
            key_times=[0.0, 0.5, 1.0],
            duration=anim.duration, delay=anim.delay,
            easing=anim.easing, bounce=False,  # bounce already manual
            hold=anim.hold, repeat=anim.repeat,
        )

    # Non-bounce uses from/to instead of values (simpler SVG output)
    parts = ['<animate attributeName="stroke-dashoffset"']
    parts.append(f' from="{from_val}" to="{to_val}"')
    parts.append(f' dur="{anim.duration}s"')
    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')
    parts.append(smil_easing_n(anim.easing, 1))
    if anim.hold:
        parts.append(' fill="freeze"')
    parts.append(smil_repeat(anim.repeat))
    parts.append(" />")
    return "".join(parts)


# ======================================================================
# Connection property animation
# ======================================================================


def render_connection_prop_smil(anim: PropertyAnimation, conn: Connection) -> str:
    """Render a property animation for a Connection."""
    svg_attr_map = {"opacity": "opacity", "color": "stroke", "width": "stroke-width"}
    svg_attr = svg_attr_map.get(anim.prop, anim.prop)

    return build_animate_element(
        attribute_name=svg_attr,
        values=[format_value(kf.value) for kf in anim.keyframes],
        key_times=_anim_key_times(anim),
        duration=anim.duration, delay=anim.delay,
        easing=anim.easing, bounce=anim.bounce,
        hold=anim.hold, repeat=anim.repeat,
    )
