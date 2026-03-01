"""Animated SVG renderer using SMIL (Synchronized Multimedia Integration Language).

The ``SMILRenderer`` extends :class:`SVGRenderer` with animation support.
Animation-related logic is split across three supporting modules:

- :mod:`.smil_elements` — Low-level ``<animate>`` element builder.
- :mod:`.smil_converters` — Animation model → SMIL string conversion.
- :mod:`.smil_reactive` — Reactive polygon/connection animation synthesis.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...animation.models import (
    DrawAnimation,
    MotionAnimation,
    PropertyAnimation,
)
from ...core.entity import Entity
from ...core.svg_utils import (
    fill_stroke_attrs,
    opacity_attr,
    shape_opacity_attrs,
    stroke_attrs,
    svg_num,
    xml_escape,
)
from ...config.caps import svg_cap_and_marker_attrs
from .smil_converters import (
    FillLayerOpt,
    _anim_key_times,
    extract_fill_layers,
    render_connection_prop_smil,
    render_draw_smil,
    render_motion_smil,
    render_property_smil,
)
from .smil_elements import build_animate_element
from .smil_reactive import (
    reactive_connection_anims,
    reactive_polygon_anims,
)
from .static import SVGRenderer, _build_svg_transform

if TYPE_CHECKING:
    from ...core.connection import Connection
    from ...entities.curve import Curve
    from ...entities.dot import Dot
    from ...entities.ellipse import Ellipse
    from ...entities.entity_group import EntityGroup
    from ...entities.line import Line
    from ...entities.path import Path
    from ...entities.polygon import Polygon
    from ...entities.rect import Rect
    from ...entities.text import Text


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

    # ------------------------------------------------------------------
    # Animation helpers
    # ------------------------------------------------------------------

    def _render_animations(self, entity: Entity) -> list[str]:
        """Render all animations on an entity to SMIL element strings."""
        result: list[str] = []
        for anim in entity._animations:
            if isinstance(anim, PropertyAnimation):
                result.extend(render_property_smil(anim, entity))
            elif isinstance(anim, MotionAnimation):
                result.append(render_motion_smil(anim))
            elif isinstance(anim, DrawAnimation):
                result.append(render_draw_smil(anim, entity))
        return [r for r in result if r]

    def _render_animations_excluding(
        self, entity: Entity, exclude: set[int],
    ) -> list[str]:
        """Like :meth:`_render_animations` but skip indices in *exclude*."""
        result: list[str] = []
        for i, anim in enumerate(entity._animations):
            if i in exclude:
                continue
            if isinstance(anim, PropertyAnimation):
                result.extend(render_property_smil(anim, entity))
            elif isinstance(anim, MotionAnimation):
                result.append(render_motion_smil(anim))
            elif isinstance(anim, DrawAnimation):
                result.append(render_draw_smil(anim, entity))
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

    def _draw_attrs(self, entity: Entity | Connection) -> str:
        """Build pathLength/stroke-dasharray/offset attrs for draw animation.

        Uses ``pathLength="1"`` so all dash values are normalized to
        ``[0, 1]``, eliminating arc-length precision mismatches between
        Python and the browser (which cause round-cap flash artifacts).
        """
        length = entity.arc_length() if hasattr(entity, "arc_length") else 0
        if length <= 0:
            return ""
        draw_anim = self._has_draw_animation(entity)
        if draw_anim is None:
            return ""
        offset = "1" if not draw_anim.reverse else "0"
        return f' pathLength="1" stroke-dasharray="1" stroke-dashoffset="{offset}"'

    # ------------------------------------------------------------------
    # Element wrapper
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

    # ------------------------------------------------------------------
    # Entity renderers
    # ------------------------------------------------------------------

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
        fill_opt = extract_fill_layers(rect)
        if fill_opt is not None:
            geometry = (
                f' x="{svg_num(rect.x)}" y="{svg_num(rect.y)}"'
                f' width="{svg_num(rect.width)}" height="{svg_num(rect.height)}"'
            )
            base_attrs = (
                f"{fill_stroke_attrs(fill_opt.base_color, rect.stroke, rect.stroke_width)}"
                f"{self._shape_opacity_for_smil(rect.opacity, rect.fill_opacity, rect.stroke_opacity, rect)}"
            )
            return self._render_entity_layered(
                "rect", geometry, rect, fill_opt,
                base_attrs, _build_svg_transform(rect),
            )
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
        fill_opt = extract_fill_layers(ellipse)
        if fill_opt is not None:
            geometry = (
                f' cx="{svg_num(ellipse.position.x)}"'
                f' cy="{svg_num(ellipse.position.y)}"'
                f' rx="{svg_num(ellipse.rx)}" ry="{svg_num(ellipse.ry)}"'
            )
            base_attrs = (
                f"{fill_stroke_attrs(fill_opt.base_color, ellipse.stroke, ellipse.stroke_width)}"
                f"{self._shape_opacity_for_smil(ellipse.opacity, ellipse.fill_opacity, ellipse.stroke_opacity, ellipse)}"
            )
            return self._render_entity_layered(
                "ellipse", geometry, ellipse, fill_opt,
                base_attrs, _build_svg_transform(ellipse),
            )
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

    def render_polygon(self, polygon: Polygon) -> str:
        reactive = reactive_polygon_anims(polygon)
        if not polygon._animations and not reactive:
            return super().render_polygon(polygon)

        # Opacity-layer optimization: replace fill animation with stacked
        # opacity layers for GPU-accelerated rendering.
        fill_opt = extract_fill_layers(polygon)
        if fill_opt is not None:
            points_str = " ".join(
                f"{svg_num(v.x)},{svg_num(v.y)}" for v in polygon.vertices
            )
            base_attrs = (
                f"{fill_stroke_attrs(fill_opt.base_color, polygon.stroke, polygon.stroke_width)}"
                f"{self._shape_opacity_for_smil(polygon.opacity, polygon.fill_opacity, polygon.stroke_opacity, polygon)}"
            )
            return self._render_entity_layered(
                "polygon", f' points="{points_str}"', polygon, fill_opt,
                base_attrs, _build_svg_transform(polygon), reactive,
            )

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

    def _build_layered_svg(
        self,
        tag: str,
        geometry_attrs: str,
        fill_opt: FillLayerOpt,
        base_attrs: str,
        transform: str,
        base_anims: list[str],
        overlay_color_attr: str,
        overlay_extra: str,
        reactive: list[str] | None,
    ) -> str:
        """Render an entity as stacked opacity layers instead of a color animation.

        Emits N ``<tag>`` elements (one per unique color) inside a ``<g>``.
        The base element carries stroke and non-color animations; each
        overlay has a synthesized opacity ``<animate>``.  GPU-accelerated
        opacity compositing replaces CPU-intensive color interpolation.

        Works for both ``fill`` color animations (entities) and ``stroke``
        color animations (connections) — the *overlay_color_attr* parameter
        selects which attribute carries the overlay color.
        """
        key_times = _anim_key_times(fill_opt.anim)

        # --- Base element: first color, stroke, non-color animations ---
        all_base_anims = list(base_anims)
        if reactive:
            all_base_anims.extend(reactive)

        if all_base_anims:
            base_anim_str = "\n".join(f"    {a}" for a in all_base_anims)
            base_el = f"  <{tag}{geometry_attrs}{base_attrs}{transform}>\n{base_anim_str}\n  </{tag}>"
        else:
            base_el = f"  <{tag}{geometry_attrs}{base_attrs}{transform} />"

        # --- Overlay elements: one per additional color ---
        overlay_els: list[str] = []
        for color, opacities in fill_opt.overlays:
            overlay_attrs = (
                f'{geometry_attrs} {overlay_color_attr}="{color}"'
                f'{overlay_extra} opacity="0"{transform}'
            )
            overlay_anims: list[str] = [
                build_animate_element(
                    attribute_name="opacity",
                    values=[svg_num(v) for v in opacities],
                    key_times=key_times,
                    duration=fill_opt.anim.duration,
                    delay=fill_opt.anim.delay,
                    easing=fill_opt.anim.easing,
                    bounce=fill_opt.anim.bounce,
                    hold=fill_opt.anim.hold,
                    repeat=fill_opt.anim.repeat,
                ),
            ]
            if reactive:
                overlay_anims.extend(reactive)
            overlay_anim_str = "\n".join(f"    {a}" for a in overlay_anims)
            overlay_els.append(
                f"  <{tag}{overlay_attrs}>\n{overlay_anim_str}\n  </{tag}>"
            )

        return "\n".join(["<g>", base_el, *overlay_els, "</g>"])

    def _render_entity_layered(
        self,
        tag: str,
        geometry_attrs: str,
        entity: Entity,
        fill_opt: FillLayerOpt,
        base_attrs: str,
        transform: str,
        reactive: list[str] | None = None,
    ) -> str:
        """Wrapper around :meth:`_build_layered_svg` for entity fill animations."""
        base_anims = self._render_animations_excluding(
            entity, {fill_opt.anim_index},
        )
        return self._build_layered_svg(
            tag, geometry_attrs, fill_opt, base_attrs, transform,
            base_anims, "fill", "", reactive,
        )

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
        draw_extra = self._draw_attrs(path) if self._has_draw_animation(path) else ""

        # Opacity-layer optimization for closed paths with fill
        fill_opt = None
        if path.closed and path._fill is not None:
            fill_opt = extract_fill_layers(path)
        if fill_opt is not None:
            d_attr = path.to_svg_path_d()
            base_attrs = (
                f' fill="{fill_opt.base_color}"'
                f"{stroke_attrs(path.color, path.width, svg_cap, marker_attrs)}"
                f' stroke-linejoin="round"'
                f"{self._shape_opacity_for_smil(path.opacity, path.fill_opacity, path.stroke_opacity, path)}"
                f"{draw_extra}"
            )
            return self._render_entity_layered(
                "path", f' d="{d_attr}"', path, fill_opt,
                base_attrs, _build_svg_transform(path),
            )

        fill_attr = (
            path.fill
            if path.closed and path._fill is not None
            else "none"
        )
        d_attr = path.to_svg_path_d()
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

    # ------------------------------------------------------------------
    # Connection renderer
    # ------------------------------------------------------------------

    def render_connection(self, conn: Connection) -> str:
        reactive = reactive_connection_anims(conn)

        if not getattr(conn, "_animations", []) and not reactive:
            return super().render_connection(conn)

        if not conn._visible:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            conn.cap, conn.start_cap, conn.end_cap, conn.width, conn.color
        )
        draw_extra = self._draw_attrs(conn)

        # Determine tag and geometry
        if conn._shape_kind == "line":
            tag = "line"
            p1 = conn.start_point
            p2 = conn.end_point
            geometry = (
                f' x1="{svg_num(p1.x)}" y1="{svg_num(p1.y)}"'
                f' x2="{svg_num(p2.x)}" y2="{svg_num(p2.y)}"'
            )
        else:
            tag = "path"
            geometry = f' d="{conn.to_svg_path_d()}" fill="none"'

        # Opacity-layer optimization for stroke color animation
        stroke_opt = extract_fill_layers(conn, target_attr="stroke")
        if stroke_opt is not None:
            base_anims: list[str] = []
            for i, anim in enumerate(conn._animations):
                if i == stroke_opt.anim_index:
                    continue
                if isinstance(anim, PropertyAnimation):
                    s = render_connection_prop_smil(anim, conn)
                elif isinstance(anim, DrawAnimation):
                    s = render_draw_smil(anim, conn)
                else:
                    continue
                if s:
                    base_anims.append(s)

            base_attrs = (
                f"{stroke_attrs(stroke_opt.base_color, conn.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(conn.opacity)}"
                f"{draw_extra}"
            )
            if tag == "path":
                base_attrs += ' stroke-linejoin="round"'

            overlay_extra = f' stroke-width="{svg_num(conn.width)}" stroke-linecap="{svg_cap}"'
            if tag == "path":
                overlay_extra += ' stroke-linejoin="round"'

            return self._build_layered_svg(
                tag, geometry, stroke_opt, base_attrs, "",
                base_anims, "stroke", overlay_extra, reactive,
            )

        # Standard (non-optimized) rendering
        anims: list[str] = []
        for anim in conn._animations:
            if isinstance(anim, PropertyAnimation):
                anims.append(render_connection_prop_smil(anim, conn))
            elif isinstance(anim, DrawAnimation):
                anims.append(render_draw_smil(anim, conn))
        anims = [a for a in anims if a]
        anims.extend(reactive)

        if tag == "line":
            attrs = (
                f"{geometry}"
                f"{stroke_attrs(conn.color, conn.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(conn.opacity)}"
                f"{draw_extra}"
            )
        else:
            attrs = (
                f"{geometry}"
                f"{stroke_attrs(conn.color, conn.width, svg_cap, marker_attrs)}"
                f' stroke-linejoin="round"'
                f"{opacity_attr(conn.opacity)}"
                f"{draw_extra}"
            )

        if not anims:
            return f"<{tag}{attrs} />"
        anim_str = "\n".join(f"  {a}" for a in anims)
        return f"<{tag}{attrs}>\n{anim_str}\n</{tag}>"
