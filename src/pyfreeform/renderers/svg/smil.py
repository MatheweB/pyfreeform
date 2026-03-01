"""Animated SVG renderer using SMIL (Synchronized Multimedia Integration Language).

The ``SMILRenderer`` extends :class:`SVGRenderer` with animation support.
Animation-related logic is split across three supporting modules:

- :mod:`.smil_elements` — Low-level ``<animate>`` element builder.
- :mod:`.smil_converters` — Animation model → SMIL string conversion.
- :mod:`.smil_reactive` — Reactive polygon/connection animation synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass
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
    fill_layer_timing_key,
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
    from ...scene.scene import Scene


# ======================================================================
# Batch overlay data
# ======================================================================


@dataclass(frozen=True, slots=True)
class _PendingOverlay:
    """Geometry for a single overlay element awaiting batch grouping."""

    tag: str
    """SVG element tag (``"polygon"``, ``"rect"``, etc.)."""

    geometry_attrs: str
    """Geometry attributes string (e.g., ``' points="0,0 100,0 50,80"'``)."""

    color_attr: str
    """Which attribute carries the overlay color (``"fill"`` or ``"stroke"``)."""

    color: str
    """The overlay color hex value."""

    extra_attrs: str
    """Additional attributes for overlays (e.g., stroke-width for stroke layers)."""

    transform: str
    """SVG transform attribute string."""

    reactive: tuple[str, ...]
    """Per-element reactive animations (vertex tracking)."""


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
        geometry = (
            f' x1="{svg_num(s.x)}" y1="{svg_num(s.y)}"'
            f' x2="{svg_num(e.x)}" y2="{svg_num(e.y)}"'
        )

        stroke_opt = extract_fill_layers(line, target_attr="stroke")
        if stroke_opt is not None:
            base_attrs = (
                f"{stroke_attrs(stroke_opt.base_color, line.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(line.opacity)}"
                f"{draw_extra}"
            )
            overlay_extra = f' stroke-width="{svg_num(line.width)}" stroke-linecap="{svg_cap}"'
            base_anims = self._render_animations_excluding(
                line, {stroke_opt.anim_index},
            )
            return self._build_layered_svg(
                "line", geometry, stroke_opt, base_attrs,
                _build_svg_transform(line), base_anims,
                "stroke", overlay_extra, None,
            )

        attrs = (
            f"{geometry}"
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
        geometry = (
            f' d="M {svg_num(s.x)} {svg_num(s.y)}'
            f" Q {svg_num(c.x)} {svg_num(c.y)}"
            f' {svg_num(e.x)} {svg_num(e.y)}"'
            f' fill="none"'
        )

        stroke_opt = extract_fill_layers(curve, target_attr="stroke")
        if stroke_opt is not None:
            base_attrs = (
                f"{stroke_attrs(stroke_opt.base_color, curve.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(curve.opacity)}"
                f"{draw_extra}"
            )
            overlay_extra = f' stroke-width="{svg_num(curve.width)}" stroke-linecap="{svg_cap}"'
            base_anims = self._render_animations_excluding(
                curve, {stroke_opt.anim_index},
            )
            return self._build_layered_svg(
                "path", geometry, stroke_opt, base_attrs,
                _build_svg_transform(curve), base_anims,
                "stroke", overlay_extra, None,
            )

        attrs = (
            f"{geometry}"
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
        *,
        batch_entity_id: int | None = None,
    ) -> str:
        """Render an entity as stacked opacity layers instead of a color animation.

        Emits N ``<tag>`` elements (one per unique color) inside a ``<g>``.
        The base element carries stroke and non-color animations; each
        overlay has a synthesized opacity ``<animate>``.  GPU-accelerated
        opacity compositing replaces CPU-intensive color interpolation.

        Works for both ``fill`` color animations (entities) and ``stroke``
        color animations (connections) — the *overlay_color_attr* parameter
        selects which attribute carries the overlay color.

        When *batch_entity_id* is set, only the base element is returned
        and overlay specs are stored in ``self._batch_pending`` for later
        batch rendering (multiple overlays sharing a single ``<animate>``).
        """
        # --- Base element: first color, stroke, non-color animations ---
        all_base_anims = list(base_anims)
        if reactive:
            all_base_anims.extend(reactive)

        if batch_entity_id is not None:
            # Batch mode: return base only, store overlays for later
            if all_base_anims:
                base_anim_str = "\n".join(f"  {a}" for a in all_base_anims)
                base_el = f"<{tag}{geometry_attrs}{base_attrs}{transform}>\n{base_anim_str}\n</{tag}>"
            else:
                base_el = f"<{tag}{geometry_attrs}{base_attrs}{transform} />"

            pending: list[_PendingOverlay] = []
            for color, _opacities in fill_opt.overlays:
                pending.append(_PendingOverlay(
                    tag=tag,
                    geometry_attrs=geometry_attrs,
                    color_attr=overlay_color_attr,
                    color=color,
                    extra_attrs=overlay_extra,
                    transform=transform,
                    reactive=tuple(reactive) if reactive else (),
                ))
            self._batch_pending[batch_entity_id] = pending
            return base_el

        # --- Normal mode: full <g> with base + overlays ---
        key_times = _anim_key_times(fill_opt.anim)

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
        batch_id = (
            id(entity)
            if hasattr(self, "_batch_pending") and id(entity) in self._batch_pending
            else None
        )
        return self._build_layered_svg(
            tag, geometry_attrs, fill_opt, base_attrs, transform,
            base_anims, "fill", "", reactive,
            batch_entity_id=batch_id,
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
        d_attr = path.to_svg_path_d()
        fill_attr = path.fill if path.closed and path._fill is not None else "none"

        # Opacity-layer optimization: fill (closed paths) or stroke color
        fill_opt = None
        if path.closed and path._fill is not None:
            fill_opt = extract_fill_layers(path)
        if fill_opt is not None:
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

        stroke_opt = extract_fill_layers(path, target_attr="stroke")
        if stroke_opt is not None:
            base_attrs = (
                f' fill="{fill_attr}"'
                f"{stroke_attrs(stroke_opt.base_color, path.width, svg_cap, marker_attrs)}"
                f' stroke-linejoin="round"'
                f"{self._shape_opacity_for_smil(path.opacity, path.fill_opacity, path.stroke_opacity, path)}"
                f"{draw_extra}"
            )
            overlay_extra = (
                f' fill="none" stroke-width="{svg_num(path.width)}"'
                f' stroke-linecap="{svg_cap}" stroke-linejoin="round"'
            )
            base_anims = self._render_animations_excluding(
                path, {stroke_opt.anim_index},
            )
            return self._build_layered_svg(
                "path", f' d="{d_attr}"', stroke_opt, base_attrs,
                _build_svg_transform(path), base_anims,
                "stroke", overlay_extra, None,
            )

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

    # ------------------------------------------------------------------
    # Fill-layer batching
    # ------------------------------------------------------------------

    def _render_batch_overlay_group(
        self,
        template_opt: FillLayerOpt,
        overlay_index: int,
        pending_overlays: list[_PendingOverlay],
    ) -> str:
        """Emit a shared ``<g>`` with one ``<animate>`` for batched overlays.

        All *pending_overlays* share the same timing envelope and opacity
        pattern (determined by ``fill_layer_timing_key``).  The single
        ``<animate attributeName="opacity">`` on the ``<g>`` replaces N
        individual per-entity opacity animations.
        """
        _color, opacities = template_opt.overlays[overlay_index]
        key_times = _anim_key_times(template_opt.anim)

        animate_el = build_animate_element(
            attribute_name="opacity",
            values=[svg_num(v) for v in opacities],
            key_times=key_times,
            duration=template_opt.anim.duration,
            delay=template_opt.anim.delay,
            easing=template_opt.anim.easing,
            bounce=template_opt.anim.bounce,
            hold=template_opt.anim.hold,
            repeat=template_opt.anim.repeat,
        )

        children: list[str] = []
        for ov in pending_overlays:
            attrs = (
                f"{ov.geometry_attrs}"
                f' {ov.color_attr}="{ov.color}"'
                f"{ov.extra_attrs}{ov.transform}"
            )
            if ov.reactive:
                reactive_str = "\n".join(f"    {r}" for r in ov.reactive)
                children.append(
                    f"  <{ov.tag}{attrs}>\n{reactive_str}\n  </{ov.tag}>"
                )
            else:
                children.append(f"  <{ov.tag}{attrs} />")

        parts = ['<g opacity="0">', f"  {animate_el}"]
        parts.extend(children)
        parts.append("</g>")
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Scene rendering with fill-layer batching
    # ------------------------------------------------------------------

    def render_scene(self, scene: Scene) -> str:
        """Render a complete animated SVG with fill-layer batching.

        Extends the parent renderer with a pre-scan pass that detects
        entities sharing the same fill animation timing.  Overlays from
        those entities are grouped into shared ``<g>`` elements with a
        single ``<animate>``, reducing the total number of SMIL animation
        elements the browser must evaluate.
        """
        all_entities = scene.entities
        all_connections = scene._collect_connections()

        # --- Pre-scan: identify batchable fill layers ---
        entity_fill_opts: dict[int, FillLayerOpt] = {}
        timing_groups: dict[tuple, list[tuple[Entity, FillLayerOpt]]] = {}

        for entity in all_entities:
            if not entity._animations:
                continue
            fill_opt = extract_fill_layers(entity)
            if fill_opt is None:
                continue
            eid = id(entity)
            entity_fill_opts[eid] = fill_opt
            group_key = (entity.z_index, fill_layer_timing_key(fill_opt))
            timing_groups.setdefault(group_key, []).append((entity, fill_opt))

        # Groups with >= 2 members -> batch mode
        batched_ids: set[int] = set()
        active_batches: dict[
            tuple, list[tuple[Entity, FillLayerOpt]]
        ] = {}
        for group_key, members in timing_groups.items():
            if len(members) >= 2:
                for entity, _opt in members:
                    batched_ids.add(id(entity))
                active_batches[group_key] = members

        # Initialize batch state for _build_layered_svg to detect
        self._batch_pending: dict[int, list[_PendingOverlay]] = {
            eid: [] for eid in batched_ids
        }

        # --- SVG document setup (mirrors parent) ---
        if scene._viewbox is not None:
            vb_x, vb_y, vb_w, vb_h = scene._viewbox
            display_h = vb_h * scene._width / vb_w if vb_w > 0 else scene._height
            svg_open = (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{scene._width}" height="{display_h:.1f}" '
                f'viewBox="{vb_x} {vb_y} {vb_w} {vb_h}">'
            )
        else:
            svg_open = (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{scene._width}" height="{scene._height}" '
                f'viewBox="0 0 {scene._width} {scene._height}">'
            )

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            svg_open,
        ]

        # Definitions (gradients, markers, path defs)
        markers = self._collect_markers(all_entities, all_connections)
        path_defs = self._collect_path_defs(all_entities)
        gradients = self._collect_gradients(all_entities, all_connections)
        if markers or path_defs or gradients:
            lines.append("  <defs>")
            lines.extend(f"    {svg}" for svg in gradients.values())
            lines.extend(f"    {svg}" for svg in markers.values())
            lines.extend(f"    {svg}" for svg in path_defs.values())
            lines.append("  </defs>")

        # Background
        if scene._background:
            if scene._viewbox is not None:
                vb_x, vb_y, vb_w, vb_h = scene._viewbox
                lines.append(
                    f'  <rect x="{vb_x}" y="{vb_y}" '
                    f'width="{vb_w}" height="{vb_h}" '
                    f'fill="{scene.background}" />'
                )
            else:
                lines.append(
                    f'  <rect width="100%" height="100%" fill="{scene.background}" />'
                )

        # --- Render entities and connections ---
        renderables: list[tuple[int, str]] = []
        renderables.extend(
            (c.z_index, self.render_connection(c)) for c in all_connections
        )
        renderables.extend(
            (e.z_index, self.render_entity(e)) for e in all_entities
        )

        # --- Emit batched overlay groups ---
        for group_key, members in active_batches.items():
            z_idx = group_key[0]
            template_opt = members[0][1]
            n_overlays = len(template_opt.overlays)

            overlays_by_index: list[list[_PendingOverlay]] = [
                [] for _ in range(n_overlays)
            ]
            for entity, _opt in members:
                pending = self._batch_pending.get(id(entity), [])
                for i, ov in enumerate(pending):
                    if i < n_overlays:
                        overlays_by_index[i].append(ov)

            for i in range(n_overlays):
                if overlays_by_index[i]:
                    overlay_svg = self._render_batch_overlay_group(
                        template_opt, i, overlays_by_index[i],
                    )
                    renderables.append((z_idx, overlay_svg))

        # Clean up batch state
        del self._batch_pending

        # --- Sort and assemble ---
        renderables.sort(key=lambda x: x[0])
        for _, svg in renderables:
            if svg:
                lines.append(f"  {svg}")

        lines.append("</svg>")
        return "\n".join(lines)
