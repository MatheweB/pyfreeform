"""Animated SVG renderer using SMIL (Synchronized Multimedia Integration Language)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..animation.models import (
    DrawAnimation,
    MotionAnimation,
    PropertyAnimation,
)
from ..core.svg_utils import opacity_attr, svg_num, fill_stroke_attrs, shape_opacity_attrs, stroke_attrs, xml_escape
from ..config.caps import svg_cap_and_marker_attrs
from .smil_elements import (
    build_animate_element,
    format_value,
    smil_easing,
    smil_easing_n,
    smil_repeat,
)
from .smil_reactive import (
    build_reactive_animate,
    build_resampled_animate,
    check_anim_compatibility,
    compute_cycle_duration,
    connection_path_d_at,
    extract_position_anims,
    resolve_abs_position,
    resolve_vertex_at_keyframe,
    resolve_vertex_at_time,
)
from .svg import SVGRenderer, _build_svg_transform

if TYPE_CHECKING:
    from ..core.connection import Connection
    from ..core.entity import Entity
    from ..entities.curve import Curve
    from ..entities.dot import Dot
    from ..entities.ellipse import Ellipse
    from ..entities.entity_group import EntityGroup
    from ..entities.line import Line
    from ..entities.path import Path
    from ..entities.polygon import Polygon
    from ..entities.rect import Rect
    from ..entities.text import Text


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
# SMIL element rendering
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


def _render_property_smil(anim: PropertyAnimation, entity: Entity) -> list[str]:
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

    # Map at_rx/at_ry to actual SVG position attributes and resolve values
    if anim.prop == "at_rx":
        svg_attr = _resolve_svg_attr(entity_type, "cx") or _resolve_svg_attr(entity_type, "x") or "cx"
        surface = entity._surface
        if surface:
            val_list = [svg_num(surface._x + kf.value * surface._width) for kf in anim.keyframes]
        else:
            val_list = [svg_num(kf.value) for kf in anim.keyframes]
    else:  # at_ry
        svg_attr = _resolve_svg_attr(entity_type, "cy") or _resolve_svg_attr(entity_type, "y") or "cy"
        surface = entity._surface
        if surface:
            val_list = [svg_num(surface._y + kf.value * surface._height) for kf in anim.keyframes]
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


def _translate_path_d(path_d: str, dx: float, dy: float) -> str:
    """Translate all coordinates in an SVG path data string by (dx, dy).

    Handles absolute M, C, L, Q, S, T, A commands and Z (no coords).
    """
    import re

    tokens = re.split(r"(\s+|,)", path_d)
    result: list[str] = []
    coord_idx = 0  # alternates 0=x, 1=y
    in_command = False

    for tok in tokens:
        stripped = tok.strip().rstrip(",")
        if not stripped:
            result.append(tok)
            continue
        if stripped in ("M", "C", "L", "Q", "S", "T", "H", "V", "A", "Z"):
            result.append(tok)
            coord_idx = 0
            in_command = stripped not in ("Z",)
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


def _render_motion_smil(anim: MotionAnimation) -> str:
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
    elif isinstance(anim.rotate, (int, float)) and anim.rotate:
        rotate_attr = f' rotate="{svg_num(anim.rotate)}"'

    parts = [f'<animateMotion dur="{anim.duration}s"']

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    if anim.bounce:
        from ..animation.models import Easing

        parts.append(' keyPoints="0;1;0"')
        parts.append(' keyTimes="0;0.5;1"')
        if anim.easing == Easing.LINEAR:
            parts.append(' calcMode="linear"')
        else:
            spline = f"{anim.easing.x1} {anim.easing.y1} {anim.easing.x2} {anim.easing.y2}"
            parts.append(f' calcMode="spline" keySplines="{spline};{spline}"')
    else:
        parts.append(smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(smil_repeat(anim.repeat))
    parts.append(rotate_attr)
    parts.append(f' path="{path_d}" />')
    return "".join(parts)


def _render_draw_smil(anim: DrawAnimation, entity: Any) -> str:
    """Render a DrawAnimation as stroke-dashoffset ``<animate>``.

    The parent element must have stroke-dasharray set to the path length.
    """
    length = entity.arc_length() if hasattr(entity, "arc_length") else 0
    if length <= 0:
        return ""

    from_val = svg_num(length) if not anim.reverse else "0"
    to_val = "0" if not anim.reverse else svg_num(length)

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
# SMILRenderer
# ======================================================================

class SMILRenderer(SVGRenderer):
    """SVG renderer with SMIL animation support.

    Extends :class:`SVGRenderer`. For entities with no animations,
    produces identical output. For entities with animations, wraps
    SVG elements with ``<animate>``, ``<animateTransform>``, and
    ``<animateMotion>`` children.
    """

    def _render_animations(self, entity: Entity) -> list[str]:
        """Render all animations on an entity to SMIL element strings."""
        result: list[str] = []
        for anim in entity._animations:
            if isinstance(anim, PropertyAnimation):
                result.extend(_render_property_smil(anim, entity))
            elif isinstance(anim, MotionAnimation):
                result.append(_render_motion_smil(anim))
            elif isinstance(anim, DrawAnimation):
                result.append(_render_draw_smil(anim, entity))
        return [r for r in result if r]

    def _shape_opacity_for_smil(
        self, opacity: float, fill_opacity: float | None, stroke_opacity: float | None,
        entity: Entity,
    ) -> str:
        """Build opacity attrs for shapes, compatible with SMIL ``opacity`` animations.

        When the entity animates ``opacity``, we must emit the SVG ``opacity``
        attribute (not ``fill-opacity``/``stroke-opacity``) so the animation
        target matches the initial attribute.  Explicit ``fill_opacity`` /
        ``stroke_opacity`` overrides are still emitted independently.
        """
        animates_opacity = any(
            isinstance(a, PropertyAnimation) and a.prop == "opacity"
            for a in entity._animations
        )
        if animates_opacity:
            parts: list[str] = [opacity_attr(opacity)]
            if fill_opacity is not None and fill_opacity < 1.0:
                parts.append(f' fill-opacity="{svg_num(fill_opacity)}"')
            if stroke_opacity is not None and stroke_opacity < 1.0:
                parts.append(f' stroke-opacity="{svg_num(stroke_opacity)}"')
            return "".join(parts)
        return shape_opacity_attrs(opacity, fill_opacity, stroke_opacity)

    def _has_draw_animation(self, entity: Entity) -> DrawAnimation | None:
        """Check if entity has a DrawAnimation."""
        for anim in entity._animations:
            if isinstance(anim, DrawAnimation):
                return anim
        return None

    def _draw_attrs(self, entity: Any) -> str:
        """Build stroke-dasharray/offset attrs for draw animation."""
        length = entity.arc_length() if hasattr(entity, "arc_length") else 0
        if length <= 0:
            return ""
        draw_anim = self._has_draw_animation(entity)
        if draw_anim is None:
            return ""
        offset = svg_num(length) if not draw_anim.reverse else "0"
        return f' stroke-dasharray="{svg_num(length)}" stroke-dashoffset="{offset}"'

    # ------------------------------------------------------------------
    # Overridden entity renderers (animation-aware)
    # ------------------------------------------------------------------

    def _wrap_element(
        self, tag: str, attrs: str, entity: Entity, content: str = "",
        extra_anims: list[str] | None = None,
    ) -> str:
        """Wrap an SVG element with SMIL animation children.

        If the entity has no animations, returns the element as-is
        (self-closing or with content). If animations are present,
        injects ``<animate>`` children.

        Args:
            extra_anims: Additional SMIL strings (e.g. from reactive
                vertex/endpoint animations) to include alongside the
                entity's own animations.
        """
        anims = self._render_animations(entity)
        if extra_anims:
            anims.extend(extra_anims)
        if not anims and not content:
            return f"<{tag}{attrs} />"
        if not anims:
            return f"<{tag}{attrs}>{content}</{tag}>"
        anim_str = "\n".join(f"  {a}" for a in anims)
        if content:
            return f"<{tag}{attrs}>\n{anim_str}\n{content}\n</{tag}>"
        return f"<{tag}{attrs}>\n{anim_str}\n</{tag}>"

    def render_dot(self, dot: Dot) -> str:
        if not dot._animations:
            return super().render_dot(dot)
        attrs = (
            f' cx="{svg_num(dot.x)}" cy="{svg_num(dot.y)}"'
            f' r="{svg_num(dot.radius)}" fill="{dot.color}"'
            f"{opacity_attr(dot.opacity)}"
            f"{_build_svg_transform(dot)}"
        )
        return self._wrap_element("circle", attrs, dot)

    def render_rect(self, rect: Rect) -> str:
        if not rect._animations:
            return super().render_rect(rect)
        attrs = (
            f' x="{svg_num(rect.x)}" y="{svg_num(rect.y)}"'
            f' width="{svg_num(rect.width)}" height="{svg_num(rect.height)}"'
            f"{fill_stroke_attrs(rect.fill, rect.stroke, rect.stroke_width)}"
            f"{self._shape_opacity_for_smil(rect.opacity, rect.fill_opacity, rect.stroke_opacity, rect)}"
            f"{_build_svg_transform(rect)}"
        )
        return self._wrap_element("rect", attrs, rect)

    def render_ellipse(self, ellipse: Ellipse) -> str:
        if not ellipse._animations:
            return super().render_ellipse(ellipse)
        attrs = (
            f' cx="{svg_num(ellipse.position.x)}"'
            f' cy="{svg_num(ellipse.position.y)}"'
            f' rx="{svg_num(ellipse.rx)}" ry="{svg_num(ellipse.ry)}"'
            f"{fill_stroke_attrs(ellipse.fill, ellipse.stroke, ellipse.stroke_width)}"
            f"{self._shape_opacity_for_smil(ellipse.opacity, ellipse.fill_opacity, ellipse.stroke_opacity, ellipse)}"
            f"{_build_svg_transform(ellipse)}"
        )
        return self._wrap_element("ellipse", attrs, ellipse)

    def render_line(self, line: Line) -> str:
        if not line._animations:
            return super().render_line(line)
        s = line.start
        e = line.end
        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            line.cap, line.start_cap, line.end_cap, line.width, line.color
        )
        draw_extra = self._draw_attrs(line) if self._has_draw_animation(line) else ""
        attrs = (
            f' x1="{svg_num(s.x)}" y1="{svg_num(s.y)}"'
            f' x2="{svg_num(e.x)}" y2="{svg_num(e.y)}"'
            f"{stroke_attrs(line.color, line.width, svg_cap, marker_attrs)}"
            f"{opacity_attr(line.opacity)}"
            f"{draw_extra}"
            f"{_build_svg_transform(line)}"
        )
        return self._wrap_element("line", attrs, line)

    def render_curve(self, curve: Curve) -> str:
        if not curve._animations:
            return super().render_curve(curve)
        s = curve.start
        c = curve.control
        e = curve.end
        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            curve.cap, curve.start_cap, curve.end_cap, curve.width, curve.color
        )
        draw_extra = self._draw_attrs(curve) if self._has_draw_animation(curve) else ""
        attrs = (
            f' d="M {svg_num(s.x)} {svg_num(s.y)}'
            f" Q {svg_num(c.x)} {svg_num(c.y)}"
            f' {svg_num(e.x)} {svg_num(e.y)}"'
            f' fill="none"'
            f"{stroke_attrs(curve.color, curve.width, svg_cap, marker_attrs)}"
            f"{opacity_attr(curve.opacity)}"
            f"{draw_extra}"
            f"{_build_svg_transform(curve)}"
        )
        return self._wrap_element("path", attrs, curve)

    def _reactive_polygon_anims(self, polygon: Polygon) -> list[str]:
        """Synthesize ``<animate attributeName="points">`` from animated vertex entities."""
        from ..core.entity import Entity as _Entity

        # Classify each vertex: (anim_pair | None, spec)
        vertex_info: list[tuple[tuple[PropertyAnimation, PropertyAnimation] | None, Any]] = []
        all_rx_anims: list[PropertyAnimation] = []

        for spec in polygon._vertex_specs:
            entity: _Entity | None = None
            if isinstance(spec, _Entity):
                entity = spec
            elif isinstance(spec, tuple) and isinstance(spec[0], _Entity):
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

        # Fast path: all animations share identical timing
        template = check_anim_compatibility(all_rx_anims)
        if template is not None:
            n_keyframes = len(template.keyframes)
            val_list: list[str] = []
            for k in range(n_keyframes):
                pts: list[str] = []
                for pair, spec in vertex_info:
                    c = resolve_vertex_at_keyframe(spec, pair, k)
                    pts.append(f"{svg_num(c.x)},{svg_num(c.y)}")
                val_list.append(" ".join(pts))
            return [build_reactive_animate("points", val_list, template)]

        # Slow path: mixed timing — resample all animations onto a unified timeline.
        # Each vertex's easing/bounce/repeat is baked into the sampled values.
        all_anims = []
        for pair, _ in vertex_info:
            if pair is not None:
                all_anims.extend(pair)
        cycle, all_repeat = compute_cycle_duration(all_anims)
        n_samples = max(2, min(120, int(cycle * 20)))

        val_list_r: list[str] = []
        key_times: list[float] = []
        for i in range(n_samples):
            t = i * cycle / (n_samples - 1) if n_samples > 1 else 0.0
            key_times.append(t / cycle if cycle > 0 else 0.0)
            pts: list[str] = []
            for pair, spec in vertex_info:
                c = resolve_vertex_at_time(spec, pair, t)
                pts.append(f"{svg_num(c.x)},{svg_num(c.y)}")
            val_list_r.append(" ".join(pts))

        return [build_resampled_animate("points", val_list_r, key_times,
                                        cycle, 0.0, all_repeat)]

    def render_polygon(self, polygon: Polygon) -> str:
        reactive = self._reactive_polygon_anims(polygon)
        if not polygon._animations and not reactive:
            return super().render_polygon(polygon)
        points_str = " ".join(
            f"{svg_num(v.x)},{svg_num(v.y)}" for v in polygon.vertices
        )
        attrs = (
            f' points="{points_str}"'
            f"{fill_stroke_attrs(polygon.fill, polygon.stroke, polygon.stroke_width)}"
            f"{self._shape_opacity_for_smil(polygon.opacity, polygon.fill_opacity, polygon.stroke_opacity, polygon)}"
            f"{_build_svg_transform(polygon)}"
        )
        return self._wrap_element("polygon", attrs, polygon, extra_anims=reactive)

    def render_text(self, text: Text) -> str:
        if not text._animations:
            return super().render_text(text)

        if text._textpath_info is not None:
            return self._render_animated_textpath(text, text._textpath_info)

        escaped = xml_escape(text.content)
        attrs = (
            f' x="{svg_num(text.x)}" y="{svg_num(text.y)}" '
            f'font-size="{svg_num(text.font_size)}" '
            f'font-family="{text.font_family}" '
            f'font-style="{text.font_style}" '
            f'font-weight="{text.font_weight}" '
            f'fill="{text.color}" '
            f'text-anchor="{text.text_anchor}" '
            f'dominant-baseline="{text.baseline}"'
            f"{opacity_attr(text.opacity)}"
            f"{_build_svg_transform(text)}"
        )
        return self._wrap_element("text", attrs, text, content=escaped)

    def _render_animated_textpath(self, text: Text, info: dict) -> str:
        """Render animated text-on-a-path with SMIL elements."""
        escaped = xml_escape(text.content)

        offset = info["start_offset"]
        offset_attr = (
            f' startOffset="{offset}"' if offset not in ("0%", "0.0%") else ""
        )

        text_len = info.get("text_length")
        textlen_attr = (
            f' textLength="{text_len:.1f}" lengthAdjust="spacing"'
            if text_len
            else ""
        )

        anims = self._render_animations(text)
        anim_str = "\n".join(f"  {a}" for a in anims) if anims else ""

        textpath_child = (
            f'<textPath href="#{info["path_id"]}"'
            f"{offset_attr}{textlen_attr}>"
            f"{escaped}"
            f"</textPath>"
        )

        parts = [
            f'<text font-size="{svg_num(text.font_size)}" '
            f'font-family="{text.font_family}" '
            f'font-style="{text.font_style}" '
            f'font-weight="{text.font_weight}" '
            f'fill="{text.color}" '
            f'text-anchor="{text.text_anchor}" '
            f'dominant-baseline="{text.baseline}"'
            f"{textlen_attr}"
            f"{opacity_attr(text.opacity)}>"
        ]
        if anim_str:
            parts.append(f"\n{anim_str}")
        parts.append(f"\n{textpath_child}\n</text>")
        return "".join(parts)

    def render_path(self, path: Path) -> str:
        if not path._animations:
            return super().render_path(path)

        if not path._bezier_segments:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            path.cap, path.start_cap, path.end_cap, path.width, path.color
        )

        d_attr = path.to_svg_path_d()
        fill_attr = (
            path.fill
            if path.closed and path._fill is not None
            else "none"
        )

        draw_extra = self._draw_attrs(path) if self._has_draw_animation(path) else ""

        attrs = (
            f' d="{d_attr}" fill="{fill_attr}"'
            f"{stroke_attrs(path.color, path.width, svg_cap, marker_attrs)}"
            f' stroke-linejoin="round"'
            f"{self._shape_opacity_for_smil(path.opacity, path.fill_opacity, path.stroke_opacity, path)}"
            f"{draw_extra}"
            f"{_build_svg_transform(path)}"
        )
        return self._wrap_element("path", attrs, path)

    def render_entitygroup(self, group: EntityGroup) -> str:
        if not group._animations and not any(
            getattr(child, "_animations", []) for child in group._children
        ):
            return super().render_entitygroup(group)

        if not group._children:
            return ""

        transforms = [f"translate({svg_num(group.x)}, {svg_num(group.y)})"]
        if group._rotation != 0:
            transforms.append(f"rotate({svg_num(group._rotation)})")
        if group._scale != 1.0:
            transforms.append(f"scale({svg_num(group._scale)})")
        transform_str = " ".join(transforms)

        sorted_children = sorted(group._children, key=lambda e: e.z_index)
        parts = [f'<g transform="{transform_str}"{opacity_attr(group.opacity)}>']

        # Group-level animations
        group_anims = self._render_animations(group)
        parts.extend(f"  {a}" for a in group_anims)

        # Children (rendered recursively through this renderer)
        parts.extend(f"  {self.render_entity(child)}" for child in sorted_children)
        parts.append("</g>")
        return "\n".join(parts)

    def _reactive_connection_anims(self, conn: Connection) -> list[str]:
        """Synthesize SMIL elements from animated connection endpoints."""
        from ..core.entity import Entity as _Entity

        start_pair = extract_position_anims(conn._start) if isinstance(conn._start, _Entity) else None
        end_pair = extract_position_anims(conn._end) if isinstance(conn._end, _Entity) else None

        if start_pair is None and end_pair is None:
            return []

        rx_anims: list[PropertyAnimation] = []
        if start_pair:
            rx_anims.append(start_pair[0])
        if end_pair:
            rx_anims.append(end_pair[0])

        # Fast path: identical timing on all endpoints
        template = check_anim_compatibility(rx_anims)
        if template is not None:
            n_kf = len(template.keyframes)
            if conn._shape_kind == "line":
                return self._reactive_line_anims(conn, start_pair, end_pair, template, n_kf)
            return self._reactive_path_anims(conn, start_pair, end_pair, template, n_kf)

        # Slow path: mixed timing — resample onto unified timeline
        all_anims: list[PropertyAnimation] = []
        if start_pair:
            all_anims.extend(start_pair)
        if end_pair:
            all_anims.extend(end_pair)
        cycle, all_repeat = compute_cycle_duration(all_anims)
        n_samples = max(2, min(120, int(cycle * 20)))

        if conn._shape_kind == "line":
            return self._reactive_line_anims_resampled(
                conn, start_pair, end_pair, cycle, n_samples, all_repeat,
            )
        return self._reactive_path_anims_resampled(
            conn, start_pair, end_pair, cycle, n_samples, all_repeat,
        )

    def _reactive_line_anims(
        self, conn: Connection,
        start_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        end_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
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
        self, conn: Connection,
        start_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        end_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        template: PropertyAnimation, n_kf: int,
    ) -> list[str]:
        """Synthesize ``d`` animation for a curved/path connection."""
        d_vals: list[str] = []
        for k in range(n_kf):
            start_k = resolve_vertex_at_keyframe(conn._start, start_pair, k) if start_pair else conn.start_point
            end_k = resolve_vertex_at_keyframe(conn._end, end_pair, k) if end_pair else conn.end_point
            d_vals.append(connection_path_d_at(conn, start_k, end_k))

        return [build_reactive_animate("d", d_vals, template)]

    # ── Resampled reactive connection methods (mixed timing) ──────────

    def _reactive_line_anims_resampled(
        self, conn: Connection,
        start_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        end_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        cycle: float, n_samples: int, all_repeat: bool,
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

            sp = resolve_vertex_at_time(conn._start, start_pair, t) if start_pair else conn.start_point
            ep = resolve_vertex_at_time(conn._end, end_pair, t) if end_pair else conn.end_point

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
        self, conn: Connection,
        start_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        end_pair: tuple[PropertyAnimation, PropertyAnimation] | None,
        cycle: float, n_samples: int, all_repeat: bool,
    ) -> list[str]:
        """Resampled ``d`` animation for mixed-timing curved connections."""
        d_vals: list[str] = []
        key_times: list[float] = []

        for i in range(n_samples):
            t = i * cycle / (n_samples - 1) if n_samples > 1 else 0.0
            key_times.append(t / cycle if cycle > 0 else 0.0)

            sp = resolve_vertex_at_time(conn._start, start_pair, t) if start_pair else conn.start_point
            ep = resolve_vertex_at_time(conn._end, end_pair, t) if end_pair else conn.end_point
            d_vals.append(connection_path_d_at(conn, sp, ep))

        return [build_resampled_animate("d", d_vals, key_times, cycle, 0.0, all_repeat)]

    def render_connection(self, conn: Connection) -> str:
        reactive = self._reactive_connection_anims(conn)

        if not getattr(conn, "_animations", []) and not reactive:
            return super().render_connection(conn)

        if not conn._visible:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            conn.cap, conn.start_cap, conn.end_cap, conn.width, conn.color
        )

        anims = []
        for anim in conn._animations:
            if isinstance(anim, PropertyAnimation):
                anims.append(_render_connection_prop_smil(anim, conn))
            elif isinstance(anim, DrawAnimation):
                anims.append(_render_draw_smil(anim, conn))

        anims = [a for a in anims if a]
        anims.extend(reactive)

        draw_extra = self._draw_attrs(conn)

        if conn._shape_kind == "line":
            p1 = conn.start_point
            p2 = conn.end_point
            attrs = (
                f' x1="{svg_num(p1.x)}" y1="{svg_num(p1.y)}"'
                f' x2="{svg_num(p2.x)}" y2="{svg_num(p2.y)}"'
                f"{stroke_attrs(conn.color, conn.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(conn.opacity)}"
                f"{draw_extra}"
            )
            tag = "line"
        else:
            d_attr = conn.to_svg_path_d()
            attrs = (
                f' d="{d_attr}" fill="none"'
                f"{stroke_attrs(conn.color, conn.width, svg_cap, marker_attrs)}"
                f' stroke-linejoin="round"'
                f"{opacity_attr(conn.opacity)}"
                f"{draw_extra}"
            )
            tag = "path"

        if not anims:
            return f"<{tag}{attrs} />"
        anim_str = "\n".join(f"  {a}" for a in anims)
        return f"<{tag}{attrs}>\n{anim_str}\n</{tag}>"


def _render_connection_prop_smil(anim: PropertyAnimation, conn: Any) -> str:
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
