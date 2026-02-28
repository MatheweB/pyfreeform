"""Animated SVG renderer using SMIL (Synchronized Multimedia Integration Language)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..animation.models import (
    Animation,
    DrawAnimation,
    MotionAnimation,
    PropertyAnimation,
)
from ..core.svg_utils import opacity_attr, svg_num, fill_stroke_attrs, shape_opacity_attrs, stroke_attrs, xml_escape
from ..config.caps import svg_cap_and_marker_attrs
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
    ("Rect", "fill_opacity"): "fill-opacity",
    ("Rect", "stroke_opacity"): "stroke-opacity",
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

def _smil_repeat(repeat: bool | int) -> str:
    """Convert repeat parameter to SVG repeatCount attribute."""
    if repeat is True:
        return ' repeatCount="indefinite"'
    if isinstance(repeat, int) and repeat > 1:
        return f' repeatCount="{repeat}"'
    return ""


def _smil_direction(bounce: bool) -> str:
    """Convert bounce to SMIL direction."""
    # SVG SMIL doesn't have a direct "direction" attribute like CSS.
    # Bounce is handled differently — we reverse keyframe values for
    # alternate cycles. For simplicity, we approximate bounce by
    # duplicating keyframes in reverse when bounce is True.
    return ""


def _render_property_smil(anim: PropertyAnimation, entity: Entity) -> str:
    """Render a PropertyAnimation as an SVG ``<animate>`` element."""
    entity_type = type(entity).__name__

    # Special handling for rotation and scale (animateTransform)
    if anim.prop == "rotation":
        return _render_rotation_smil(anim, entity)
    if anim.prop == "scale" or anim.prop == "scale_factor":
        return _render_scale_smil(anim, entity)

    # Special handling for position animations
    if anim.prop in ("at_rx", "at_ry"):
        return _render_position_smil(anim, entity)

    svg_attr = _resolve_svg_attr(entity_type, anim.prop)
    if svg_attr is None:
        # Try using the prop name directly as SVG attribute
        svg_attr = anim.prop

    values = _format_values(anim)
    key_times = _format_key_times(anim)

    parts = [f'<animate attributeName="{svg_attr}"']
    parts.append(f' values="{values}"')
    parts.append(f' keyTimes="{key_times}"')
    parts.append(f' dur="{anim.duration}s"')

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))

    parts.append(" />")
    return "".join(parts)


def _render_rotation_smil(anim: PropertyAnimation, entity: Entity) -> str:
    """Render rotation as ``<animateTransform type="rotate">``."""
    center = entity.rotation_center
    cx, cy = svg_num(center.x), svg_num(center.y)

    values = ";".join(
        f"{svg_num(kf.value)} {cx} {cy}" for kf in anim.keyframes
    )

    parts = [
        '<animateTransform attributeName="transform" type="rotate"',
        f' values="{values}"',
        f' dur="{anim.duration}s"',
    ]

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))
    parts.append(' additive="sum" />')
    return "".join(parts)


def _render_scale_smil(anim: PropertyAnimation, entity: Entity) -> str:
    """Render scale as ``<animateTransform type="scale">``."""
    values = ";".join(svg_num(kf.value) for kf in anim.keyframes)

    parts = [
        '<animateTransform attributeName="transform" type="scale"',
        f' values="{values}"',
        f' dur="{anim.duration}s"',
    ]

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))
    parts.append(' additive="sum" />')
    return "".join(parts)


def _render_position_smil(anim: PropertyAnimation, entity: Entity) -> str:
    """Render a relative position animation as ``<animate>`` on cx/cy or x/y."""
    entity_type = type(entity).__name__

    # Map at_rx/at_ry to actual SVG position attributes
    if anim.prop == "at_rx":
        # Resolve relative → pixel for x-axis
        svg_attr = _resolve_svg_attr(entity_type, "cx") or _resolve_svg_attr(entity_type, "x") or "cx"
        surface = entity._surface
        if surface:
            _, _, sw, _ = surface._x, surface._y, surface._width, surface._height
            values = ";".join(
                svg_num(surface._x + kf.value * sw) for kf in anim.keyframes
            )
        else:
            values = ";".join(svg_num(kf.value) for kf in anim.keyframes)
    else:  # at_ry
        svg_attr = _resolve_svg_attr(entity_type, "cy") or _resolve_svg_attr(entity_type, "y") or "cy"
        surface = entity._surface
        if surface:
            _, _, _, sh = surface._x, surface._y, surface._width, surface._height
            values = ";".join(
                svg_num(surface._y + kf.value * sh) for kf in anim.keyframes
            )
        else:
            values = ";".join(svg_num(kf.value) for kf in anim.keyframes)

    key_times = _format_key_times(anim)

    parts = [f'<animate attributeName="{svg_attr}"']
    parts.append(f' values="{values}"')
    parts.append(f' keyTimes="{key_times}"')
    parts.append(f' dur="{anim.duration}s"')

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))
    parts.append(" />")
    return "".join(parts)


def _render_motion_smil(anim: MotionAnimation) -> str:
    """Render a MotionAnimation as ``<animateMotion>``."""
    path_d = anim.path.to_svg_path_d()

    rotate_attr = ""
    if anim.rotate is True:
        rotate_attr = ' rotate="auto"'
    elif isinstance(anim.rotate, (int, float)) and anim.rotate:
        rotate_attr = f' rotate="{svg_num(anim.rotate)}"'

    parts = [f'<animateMotion dur="{anim.duration}s"']

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))
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

    parts = ['<animate attributeName="stroke-dashoffset"']
    parts.append(f' from="{from_val}" to="{to_val}"')
    parts.append(f' dur="{anim.duration}s"')

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))
    parts.append(" />")
    return "".join(parts)


# ======================================================================
# Helpers
# ======================================================================

def _format_values(anim: PropertyAnimation) -> str:
    """Format keyframe values as semicolon-separated string."""
    return ";".join(_format_value(kf.value) for kf in anim.keyframes)


def _format_value(v: Any) -> str:
    """Format a single keyframe value for SVG."""
    if isinstance(v, float):
        return svg_num(v)
    if isinstance(v, int):
        return str(v)
    return str(v)


def _format_key_times(anim: PropertyAnimation) -> str:
    """Format keyframe times as normalized 0–1 values."""
    dur = anim.duration
    if dur <= 0:
        return ";".join("0" for _ in anim.keyframes)
    base = anim.keyframes[0].time
    return ";".join(
        svg_num((kf.time - base) / dur) for kf in anim.keyframes
    )


def _smil_easing(anim: PropertyAnimation | MotionAnimation | DrawAnimation) -> str:
    """Build calcMode + keySplines attributes for easing."""
    from ..animation.models import Easing

    easing = anim.easing
    if easing == Easing.LINEAR:
        return ""

    n_segments = max(1, len(anim.keyframes) - 1) if hasattr(anim, "keyframes") else 1
    spline = f"{easing.x1} {easing.y1} {easing.x2} {easing.y2}"
    splines = ";".join([spline] * n_segments)
    return f' calcMode="spline" keySplines="{splines}"'


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
        result = []
        for anim in entity._animations:
            if isinstance(anim, PropertyAnimation):
                result.append(_render_property_smil(anim, entity))
            elif isinstance(anim, MotionAnimation):
                result.append(_render_motion_smil(anim))
            elif isinstance(anim, DrawAnimation):
                result.append(_render_draw_smil(anim, entity))
        return [r for r in result if r]

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
        self, tag: str, attrs: str, entity: Entity, content: str = ""
    ) -> str:
        """Wrap an SVG element with SMIL animation children.

        If the entity has no animations, returns the element as-is
        (self-closing or with content). If animations are present,
        injects ``<animate>`` children.
        """
        anims = self._render_animations(entity)
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
            f"{shape_opacity_attrs(rect.opacity, rect.fill_opacity, rect.stroke_opacity)}"
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
            f"{shape_opacity_attrs(ellipse.opacity, ellipse.fill_opacity, ellipse.stroke_opacity)}"
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

    def render_polygon(self, polygon: Polygon) -> str:
        if not polygon._animations:
            return super().render_polygon(polygon)
        points_str = " ".join(
            f"{svg_num(v.x)},{svg_num(v.y)}" for v in polygon.vertices
        )
        attrs = (
            f' points="{points_str}"'
            f"{fill_stroke_attrs(polygon.fill, polygon.stroke, polygon.stroke_width)}"
            f"{shape_opacity_attrs(polygon.opacity, polygon.fill_opacity, polygon.stroke_opacity)}"
            f"{_build_svg_transform(polygon)}"
        )
        return self._wrap_element("polygon", attrs, polygon)

    def render_text(self, text: Text) -> str:
        if not text._animations:
            return super().render_text(text)

        if text._textpath_info is not None:
            # TextPath animations are complex — delegate to static for now
            return super().render_text(text)

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
            f"{shape_opacity_attrs(path.opacity, path.fill_opacity, path.stroke_opacity)}"
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

    def render_connection(self, conn: Connection) -> str:
        if not getattr(conn, "_animations", []):
            return super().render_connection(conn)

        if not conn._visible:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            conn.cap, conn.start_cap, conn.end_cap, conn.width, conn.color
        )

        anims = []
        for anim in conn._animations:
            if isinstance(anim, PropertyAnimation):
                # For connections, map prop names manually
                svg_attr = {"opacity": "opacity", "color": "stroke", "width": "stroke-width"}.get(
                    anim.prop, anim.prop
                )
                anim_copy = PropertyAnimation(
                    prop=svg_attr,
                    keyframes=anim.keyframes,
                    easing=anim.easing,
                    hold=anim.hold,
                    repeat=anim.repeat,
                    bounce=anim.bounce,
                    delay=anim.delay,
                )
                anims.append(_render_property_smil.__wrapped__(anim_copy, conn)
                    if hasattr(_render_property_smil, "__wrapped__")
                    else _render_connection_prop_smil(anim, conn))
            elif isinstance(anim, DrawAnimation):
                anims.append(_render_draw_smil(anim, conn))

        anims = [a for a in anims if a]

        if conn._shape_kind == "line":
            p1 = conn.start_point
            p2 = conn.end_point
            draw_anim = next((a for a in conn._animations if isinstance(a, DrawAnimation)), None)
            draw_extra = ""
            if draw_anim and hasattr(conn, "arc_length"):
                length = conn.arc_length()
                if length > 0:
                    offset = svg_num(length) if not draw_anim.reverse else "0"
                    draw_extra = f' stroke-dasharray="{svg_num(length)}" stroke-dashoffset="{offset}"'
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
            draw_anim = next((a for a in conn._animations if isinstance(a, DrawAnimation)), None)
            draw_extra = ""
            if draw_anim and hasattr(conn, "arc_length"):
                length = conn.arc_length()
                if length > 0:
                    offset = svg_num(length) if not draw_anim.reverse else "0"
                    draw_extra = f' stroke-dasharray="{svg_num(length)}" stroke-dashoffset="{offset}"'
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

    values = _format_values(anim)
    key_times = _format_key_times(anim)

    parts = [f'<animate attributeName="{svg_attr}"']
    parts.append(f' values="{values}"')
    parts.append(f' keyTimes="{key_times}"')
    parts.append(f' dur="{anim.duration}s"')

    if anim.delay > 0:
        parts.append(f' begin="{anim.delay}s"')

    parts.append(_smil_easing(anim))

    if anim.hold:
        parts.append(' fill="freeze"')

    parts.append(_smil_repeat(anim.repeat))
    parts.append(" />")
    return "".join(parts)
