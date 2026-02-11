"""Generate SVG for the PyFreeform Relationship Map (Section 14 of API Reference)."""

from pyfreeform import (
    Scene,
    Palette,
    Line,
    Curve,
    Text,
    ConnectionStyle,
)
from wiki._generator import save


def generate():
    """Build the class relationship diagram — PyFreeform documenting itself.

    Uses a 12x7 grid so all layout is cell-relative — no manual coordinates.
    """
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=12,
        rows=7,
        cell_width=56,
        cell_height=72,
        background=colors.background,
    )
    g = scene.grid

    # ── Styles ──────────────────────────────────────────────
    ARROW = ConnectionStyle(width=1.5, color=colors.line, opacity=0.7, end_cap="arrow")
    FAINT = ConnectionStyle(width=1, color=colors.line, opacity=0.35, end_cap="arrow")
    INHERIT = ConnectionStyle(width=0.8, color=colors.secondary, opacity=0.15)
    LABEL = "#aaaacc"
    DIM = "#888899"

    # ── Helpers ─────────────────────────────────────────────
    def class_box(
        area,
        label,
        fill,
        *,
        font_size=0.20,
        text_color="#ffffff",
        fill_opacity=0.25,
        stroke_opacity=0.7,
    ):
        """Place a labeled class box centered in a merged cell area."""
        w_rel = min(0.88, 108 / area.width)
        h_rel = 32 / area.height
        r = area.add_rect(
            fill=fill,
            stroke=fill,
            stroke_width=1.5,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
            width=w_rel,
            height=h_rel,
        )
        area.add_text(label, font_size=font_size, bold=True, color=text_color, fit=True)
        return r

    def surface_badge(area):
        """Yellow 'Surface' badge below the center of an area."""
        area.add_rect(
            at=(0.5, 0.74),
            fill=colors.accent,
            stroke=colors.accent,
            stroke_width=0,
            fill_opacity=0.85,
            stroke_opacity=0,
            width=58 / area.width,
            height=15 / area.height,
        )
        area.add_text(
            "Surface",
            at=(0.5, 0.74),
            font_size=0.10,
            bold=True,
            color="#1a1a2e",
        )

    def wire(
        a,
        b,
        style,
        shape=None,
        label=None,
        start_anchor="center",
        end_anchor="center",
        label_dx=0,
        label_dy=0,
        label_t=0.5,
    ):
        """Connect two entities and optionally label the midpoint."""
        if shape is None:
            shape = Line()
        conn = a.connect(
            b,
            shape=shape,
            style=style,
            start_anchor=start_anchor,
            end_anchor=end_anchor,
        )
        scene.add_connection(conn)
        if label:
            mid = conn.point_at(label_t)
            scene.place(Text(mid.x + label_dx, mid.y + label_dy, label, font_size=9, color=LABEL))
        return conn

    # ═══════════════════════════════════════════════════════════
    # ROW 0 — Scene  (entry point, alone at top)
    # ═══════════════════════════════════════════════════════════
    scene_area = g.merge((0, 4), (0, 5))
    scene_box = class_box(scene_area, "Scene", colors.primary)
    surface_badge(scene_area)

    # ═══════════════════════════════════════════════════════════
    # ROW 1 — Grid + Image  (same row → clean horizontal arrow)
    # ═══════════════════════════════════════════════════════════
    grid_area = g.merge((1, 3), (1, 4))
    grid_box = class_box(grid_area, "Grid", colors.primary)

    image_area = g.merge((1, 8), (1, 9))
    image_box = class_box(
        image_area,
        "Image",
        colors.grid,
        font_size=0.15,
        text_color=LABEL,
        fill_opacity=0.3,
        stroke_opacity=0.5,
    )

    # ═══════════════════════════════════════════════════════════
    # ROW 2 — Cell + CellGroup
    # ═══════════════════════════════════════════════════════════
    cell_area = g.merge((2, 1), (2, 2))
    cell_box = class_box(cell_area, "Cell", colors.primary)
    surface_badge(cell_area)

    cg_area = g.merge((2, 7), (2, 9))
    cg_box = class_box(cg_area, "CellGroup", colors.primary, font_size=0.15)
    surface_badge(cg_area)

    # ═══════════════════════════════════════════════════════════
    # ROW 3 — Entity
    # ═══════════════════════════════════════════════════════════
    entity_area = g.merge((3, 3), (3, 4))
    entity_box = class_box(entity_area, "Entity", colors.secondary)

    # ═══════════════════════════════════════════════════════════
    # ROW 4 — 10 Entity subclasses  +  Connection (right)
    # ═══════════════════════════════════════════════════════════
    names = [
        "Dot",
        "Point",
        "Line",
        "Curve",
        "Ellipse",
        "Rect",
        "Polygon",
        "Text",
        "Path",
        "EntityGroup",
    ]
    sub_rects = []
    for i, name in enumerate(names):
        cell = g[4, i]
        r = cell.add_rect(
            fill=colors.secondary,
            stroke=colors.secondary,
            stroke_width=1,
            fill_opacity=0.15,
            stroke_opacity=0.5,
            width=min(0.9, 52 / cell.width),
            height=22 / cell.height,
        )
        fs = 0.10 if len(name) > 7 else 0.15
        cell.add_text(name, font_size=fs, color=colors.secondary, fit=True)
        sub_rects.append(r)

    # Pathable indicator dots below Line(2), Curve(3), Ellipse(4), Path(8)
    for idx in [2, 3, 4, 8]:
        g[4, idx].add_dot(
            at=(0.5, 0.82),
            radius=0.05,
            color=colors.accent,
            opacity=0.7,
        )
    # Small annotation
    g[4, 3].add_text("Pathable", at=(0.5, 0.95), font_size=0.10, color=DIM, fit=True)

    # Connection — right side of the same row
    conn_area = g.merge((4, 10), (4, 11))
    conn_box = class_box(
        conn_area,
        "Connection",
        colors.secondary,
        font_size=0.15,
    )
    # StrokedPathMixin annotation
    conn_area.add_text(
        "StrokedPathMixin",
        at=(0.5, 0.78),
        font_size=0.10,
        color=DIM,
        fit=True,
    )

    # ═══════════════════════════════════════════════════════════
    # ROW 5 — Pathable protocol box
    # ═══════════════════════════════════════════════════════════
    path_area = g.merge((6, 1), (6, 10))
    pathable_box = path_area.add_rect(
        fill=colors.accent,
        stroke=colors.accent,
        stroke_width=1.5,
        fill_opacity=0.1,
        stroke_opacity=0.5,
        width=1.0,
        height=0.7,
    )
    path_area.add_text(
        "Pathable protocol: point_at(t)",
        at=(0.5, 0.35),
        font_size=0.15,
        bold=True,
        color=colors.accent,
        fit=True,
    )
    path_area.add_text(
        "Line  \u00b7  Curve  \u00b7  Ellipse  \u00b7  Path  \u00b7  Connection",
        at=(0.5, 0.65),
        font_size=0.15,
        color=LABEL,
        fit=True,
    )

    # ═══════════════════════════════════════════════════════════
    # CONNECTIONS
    # ═══════════════════════════════════════════════════════════

    # Scene → Grid
    wire(
        scene_box,
        grid_box,
        ARROW,
        start_anchor="bottom",
        end_anchor="top",
        label="has",
        label_dx=-18,
    )

    # Image → Grid
    wire(
        image_box,
        grid_box,
        FAINT,
        start_anchor="left",
        end_anchor="right",
        label="from_image()",
        label_dy=-12,
    )

    # Grid → Cell
    wire(
        grid_box,
        cell_box,
        ARROW,
        start_anchor="bottom_left",
        end_anchor="top",
        label="has",
        label_dx=-18,
    )

    # Grid → CellGroup
    wire(
        grid_box,
        cg_box,
        ARROW,
        shape=Curve(curvature=-0.3),
        start_anchor="bottom_right",
        end_anchor="top",
        label=".merge()",
        label_dx=22,
        label_t=0.4,
    )

    # Cell → Entity
    wire(
        cell_box,
        entity_box,
        ARROW,
        start_anchor="bottom",
        end_anchor="top_left",
        label="add_*()",
        label_dx=-28,
    )

    # Entity → 10 subclasses (inheritance fan — very faint)
    for sr in sub_rects:
        wire(entity_box, sr, INHERIT, start_anchor="bottom", end_anchor="top")

    # Entity → Connection (curved right, past the fan)
    wire(
        entity_box,
        conn_box,
        ARROW,
        shape=Curve(curvature=-0.45),
        start_anchor="right",
        end_anchor="top",
        label=".connect()",
        label_dx=12,
        label_dy=-10,
        label_t=0.2,
    )

    # Connection → Pathable
    wire(
        conn_box,
        pathable_box,
        ARROW,
        start_anchor="bottom",
        end_anchor="top_right",
        label="point_at(t)",
        label_dx=-35,
    )

    save(scene, "api-surface/relationship-map.svg")
