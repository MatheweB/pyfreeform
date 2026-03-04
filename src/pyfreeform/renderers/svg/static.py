"""Static SVG renderer — produces identical output to the original to_svg() methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...config.caps import svg_cap_and_marker_attrs
from ...core.svg_utils import (
    fill_stroke_attrs,
    opacity_attr,
    shape_opacity_attrs,
    stroke_attrs,
    svg_num,
    xml_escape,
)
from ..base import Renderer

if TYPE_CHECKING:
    from ...core.connection import Connection
    from ...core.entity import Entity
    from ...entities.curve import Curve
    from ...entities.dot import Dot
    from ...entities.ellipse import Ellipse
    from ...entities.entity_group import EntityGroup
    from ...entities.line import Line
    from ...entities.path import Path
    from ...entities.point import Point
    from ...entities.polygon import Polygon
    from ...entities.rect import Rect
    from ...entities.text import Text
    from ...scene.scene import Scene


class SVGRenderer(Renderer):
    """Renders PyFreeform scenes as static SVG.

    This renderer produces output identical to the original inline
    ``to_svg()`` methods. It ignores any animations on entities —
    use :class:`SMILRenderer` for animated SVG output.
    """

    # ------------------------------------------------------------------
    # Scene rendering
    # ------------------------------------------------------------------

    def _build_svg_header(
        self,
        scene: Scene,
        all_entities: list[Entity],
        all_connections: list[Connection],
    ) -> list[str]:
        """Build SVG preamble: XML declaration, ``<svg>`` open, ``<defs>``, background."""
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
                lines.append(f'  <rect width="100%" height="100%" fill="{scene.background}" />')

        return lines

    def render_scene(self, scene: Scene) -> str:
        """Render a complete SVG document."""
        all_entities = scene.entities
        all_connections = scene._collect_connections()

        lines = self._build_svg_header(scene, all_entities, all_connections)

        # Collect all renderables with z_index
        renderables: list[tuple[int, str]] = []
        renderables.extend((c.z_index, self.render_connection(c)) for c in all_connections)
        renderables.extend((e.z_index, self.render_entity(e)) for e in all_entities)

        # Sort by z_index (stable sort preserves add-order for ties)
        renderables.sort(key=lambda x: x[0])

        for _, svg in renderables:
            if svg:
                lines.append(f"  {svg}")

        lines.append("</svg>")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Defs collection
    # ------------------------------------------------------------------

    def _collect_markers(
        self, entities: list[Entity], connections: list[Connection]
    ) -> dict[str, str]:
        markers = {mid: svg for entity in entities for mid, svg in entity.get_required_markers()}
        markers |= {mid: svg for conn in connections for mid, svg in conn.get_required_markers()}
        return markers

    def _collect_path_defs(self, entities: list[Entity]) -> dict[str, str]:
        return {pid: svg for entity in entities for pid, svg in entity.get_required_paths()}

    def _collect_gradients(
        self, entities: list[Entity], connections: list[Connection]
    ) -> dict[str, str]:
        gradients = {
            gid: svg for entity in entities for gid, svg in entity.get_required_gradients()
        }
        gradients |= {
            gid: svg for conn in connections for gid, svg in conn.get_required_gradients()
        }
        return gradients

    # ------------------------------------------------------------------
    # Entity renderers
    # ------------------------------------------------------------------

    def render_dot(self, dot: Dot) -> str:
        """Render Dot as SVG ``<circle>``."""
        return (
            f'<circle cx="{svg_num(dot.x)}" cy="{svg_num(dot.y)}"'
            f' r="{svg_num(dot.radius)}" fill="{dot.color}"'
            f"{opacity_attr(dot.opacity)}"
            f"{_build_svg_transform(dot)} />"
        )

    def render_rect(self, rect: Rect) -> str:
        """Render Rect as SVG ``<rect>``."""
        return (
            f'<rect x="{svg_num(rect.x)}" y="{svg_num(rect.y)}"'
            f' width="{svg_num(rect.width)}" height="{svg_num(rect.height)}"'
            f"{fill_stroke_attrs(rect.fill, rect.stroke, rect.stroke_width)}"
            f"{shape_opacity_attrs(rect.opacity, rect.fill_opacity, rect.stroke_opacity)}"
            f"{_build_svg_transform(rect)} />"
        )

    def render_ellipse(self, ellipse: Ellipse) -> str:
        """Render Ellipse as SVG ``<ellipse>``."""
        return (
            f'<ellipse cx="{svg_num(ellipse.position.x)}"'
            f' cy="{svg_num(ellipse.position.y)}"'
            f' rx="{svg_num(ellipse.rx)}" ry="{svg_num(ellipse.ry)}"'
            f"{fill_stroke_attrs(ellipse.fill, ellipse.stroke, ellipse.stroke_width)}"
            f"{shape_opacity_attrs(ellipse.opacity, ellipse.fill_opacity, ellipse.stroke_opacity)}"
            f"{_build_svg_transform(ellipse)} />"
        )

    def render_line(self, line: Line) -> str:
        """Render Line as SVG ``<line>``."""
        s = line.start
        e = line.end
        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            line.cap, line.start_cap, line.end_cap, line.width, line.color
        )
        return (
            f'<line x1="{svg_num(s.x)}" y1="{svg_num(s.y)}"'
            f' x2="{svg_num(e.x)}" y2="{svg_num(e.y)}"'
            f"{stroke_attrs(line.color, line.width, svg_cap, marker_attrs)}"
            f"{opacity_attr(line.opacity)}"
            f"{_build_svg_transform(line)} />"
        )

    def render_curve(self, curve: Curve) -> str:
        """Render Curve as SVG ``<path>`` (quadratic Bezier)."""
        s = curve.start
        c = curve.control
        e = curve.end
        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            curve.cap, curve.start_cap, curve.end_cap, curve.width, curve.color
        )
        return (
            f'<path d="M {svg_num(s.x)} {svg_num(s.y)}'
            f" Q {svg_num(c.x)} {svg_num(c.y)}"
            f' {svg_num(e.x)} {svg_num(e.y)}"'
            f' fill="none"'
            f"{stroke_attrs(curve.color, curve.width, svg_cap, marker_attrs)}"
            f"{opacity_attr(curve.opacity)}"
            f"{_build_svg_transform(curve)} />"
        )

    def render_polygon(self, polygon: Polygon) -> str:
        """Render Polygon as SVG ``<polygon>``."""
        points_str = " ".join(f"{svg_num(v.x)},{svg_num(v.y)}" for v in polygon.vertices)
        return (
            f'<polygon points="{points_str}"'
            f"{fill_stroke_attrs(polygon.fill, polygon.stroke, polygon.stroke_width)}"
            f"{shape_opacity_attrs(polygon.opacity, polygon.fill_opacity, polygon.stroke_opacity)}"
            f"{_build_svg_transform(polygon)} />"
        )

    def render_text(self, text: Text) -> str:
        """Render Text as SVG ``<text>`` (or with ``<textPath>``)."""
        if text._textpath_info is not None:
            return self._render_textpath(text, text._textpath_info)

        escaped = xml_escape(text.content)
        return (
            f'<text x="{svg_num(text.x)}" y="{svg_num(text.y)}" '
            f'font-size="{svg_num(text.font_size)}" '
            f'font-family="{text.font_family}" '
            f'font-style="{text.font_style}" '
            f'font-weight="{text.font_weight}" '
            f'fill="{text.color}" '
            f'text-anchor="{text.text_anchor}" '
            f'dominant-baseline="{text.baseline}"'
            f"{opacity_attr(text.opacity)}"
            f"{_build_svg_transform(text)}>"
            f"{escaped}"
            f"</text>"
        )

    def _render_textpath(self, text: Text, info: dict) -> str:
        """Render Text with textPath warping."""
        escaped = xml_escape(text.content)

        offset = info["start_offset"]
        offset_attr = f' startOffset="{offset}"' if offset not in ("0%", "0.0%") else ""

        text_len = info.get("text_length")
        textlen_attr = f' textLength="{text_len:.1f}" lengthAdjust="spacing"' if text_len else ""

        return (
            f'<text font-size="{svg_num(text.font_size)}" '
            f'font-family="{text.font_family}" '
            f'font-style="{text.font_style}" '
            f'font-weight="{text.font_weight}" '
            f'fill="{text.color}" '
            f'text-anchor="{text.text_anchor}" '
            f'dominant-baseline="{text.baseline}"'
            f"{textlen_attr}"
            f"{opacity_attr(text.opacity)}>"
            f'<textPath href="#{info["path_id"]}"'
            f"{offset_attr}{textlen_attr}>"
            f"{escaped}"
            f"</textPath></text>"
        )

    def render_path(self, path: Path) -> str:
        """Render Path as SVG ``<path>``."""
        if not path._bezier_segments:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            path.cap, path.start_cap, path.end_cap, path.width, path.color
        )

        d_attr = path.to_svg_path_d()
        fill_attr = path.fill if path.closed and path._fill is not None else "none"

        return (
            f'<path d="{d_attr}" fill="{fill_attr}"'
            f"{stroke_attrs(path.color, path.width, svg_cap, marker_attrs)}"
            f' stroke-linejoin="round"'
            f"{shape_opacity_attrs(path.opacity, path.fill_opacity, path.stroke_opacity)}"
            f"{_build_svg_transform(path)} />"
        )

    def render_entitygroup(self, group: EntityGroup) -> str:
        """Render EntityGroup as SVG ``<g>`` with transform."""
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
        parts.extend(f"  {self.render_entity(child)}" for child in sorted_children)
        parts.append("</g>")
        return "\n".join(parts)

    def render_point(self, point: Point) -> str:
        """Point is invisible — returns empty string."""
        return ""

    # ------------------------------------------------------------------
    # Connection rendering
    # ------------------------------------------------------------------

    def render_connection(self, conn: Connection) -> str:
        """Render Connection as SVG ``<line>`` or ``<path>``."""
        if not conn._visible:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            conn.cap, conn.start_cap, conn.end_cap, conn.width, conn.color
        )

        if conn._shape_kind == "line":
            p1 = conn.start_point
            p2 = conn.end_point
            return (
                f'<line x1="{svg_num(p1.x)}" y1="{svg_num(p1.y)}"'
                f' x2="{svg_num(p2.x)}" y2="{svg_num(p2.y)}"'
                f"{stroke_attrs(conn.color, conn.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(conn.opacity)} />"
            )

        d_attr = conn.to_svg_path_d()
        return (
            f'<path d="{d_attr}" fill="none"'
            f"{stroke_attrs(conn.color, conn.width, svg_cap, marker_attrs)}"
            f' stroke-linejoin="round"'
            f"{opacity_attr(conn.opacity)} />"
        )


# ======================================================================
# Shared helper: SVG transform attribute
# ======================================================================


def _build_svg_transform(entity: Entity) -> str:
    """Build SVG ``transform`` attribute string for rotation/scale.

    Returns empty string for identity transforms, otherwise a
    fully-formed ``' transform="..."'`` attribute (leading space).
    """
    has_rot = entity._rotation != 0
    has_scale = entity._scale_factor != 1.0
    if not has_rot and not has_scale:
        return ""
    center = entity.rotation_center
    cx, cy = svg_num(center.x), svg_num(center.y)
    ncx, ncy = svg_num(-center.x), svg_num(-center.y)
    if has_rot and not has_scale:
        return f' transform="rotate({svg_num(entity._rotation)} {cx} {cy})"'
    if has_scale and not has_rot:
        s = svg_num(entity._scale_factor)
        return f' transform="translate({cx},{cy}) scale({s}) translate({ncx},{ncy})"'
    s = svg_num(entity._scale_factor)
    return (
        f' transform="translate({cx},{cy})'
        f" rotate({svg_num(entity._rotation)})"
        f" scale({s})"
        f' translate({ncx},{ncy})"'
    )
