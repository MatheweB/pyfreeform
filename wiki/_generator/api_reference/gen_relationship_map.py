"""Generate SVG for the PyFreeform Relationship Map (API Reference)."""

from pyfreeform import Scene, Palette, PathStyle, distribute
from wiki._generator import save


def generate():
    """Build the class relationship diagram — PyFreeform documenting itself.

    12x9 grid. Each logical group is its own CellGroup.
    Pills are distributed entities within category panels.
    Labels live in gap cells between boxes.
    """
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=12, rows=9,
        cell_width=63, cell_height=58,
        background=colors.background,
    )
    g = scene.grid

    # ── Styles ──────────────────────────────────────────────────
    ARROW = PathStyle(width=1.5, color=colors.line, opacity=0.7, end_cap="arrow")
    FAINT = PathStyle(width=1.0, color=colors.line, opacity=0.35, end_cap="arrow")
    INHERIT = PathStyle(width=1.0, color=colors.secondary, opacity=0.15)
    LABEL = "#aaaacc"
    DIM = "#888899"

    # ── Helpers ─────────────────────────────────────────────────
    def class_box(r1, c1, r2, c2, label, color, *, is_surface=False):
        """Class box in its own CellGroup."""
        area = g.merge((r1, c1), (r2, c2))
        r = area.add_rect(
            fill=color, stroke=color,
            stroke_width=1.5, fill_opacity=0.2, stroke_opacity=0.6,
            width=0.85, height=0.45,
        )
        area.add_text(label, within=r, fit=True, bold=True, color="#ffffff")
        if is_surface:
            area.add_line(
                within=r, start=(0.04, 0.25), end=(0.04, 0.75),
                width=3, color=colors.accent, opacity=0.8,
            )
            area.add_text(
                "Surface", within=r, at=(0.5, 1.35),
                font_size=0.22, bold=True,
                color=colors.accent, opacity=0.6,
            )
        return r, area

    def category(r1, c1, r2, c2, header, items):
        """Category panel — a CellGroup with header + distributed pills."""
        area = g.merge((r1, c1), (r2, c2))
        bg = area.add_rect(
            fill=colors.secondary, stroke=colors.secondary,
            stroke_width=1, fill_opacity=0.04, stroke_opacity=0.2,
            width=0.96, height=0.96, z_index=-1,
        )
        area.add_text(
            header, at=(0.5, 0.18),
            font_size=0.08, color=DIM, italic=True,
        )
        pills = []
        for name, pathable in items:
            r = area.add_rect(
                at=(0.5, 0.58),
                fill=colors.secondary, stroke=colors.secondary,
                stroke_width=1, fill_opacity=0.12, stroke_opacity=0.45,
                width=0.20, height=0.22,
            )
            area.add_text(name, within=r, fit=True, color=colors.secondary)
            if pathable:
                area.add_dot(
                    within=r, at=(0.5, 1.15),
                    radius=0.10, color=colors.accent, opacity=0.7,
                )
            pills.append(r)
        distribute(*pills, axis="x", start=0.06, end=0.94)
        return bg, area

    # ═══════════════════════════════════════════════════════════
    # CLASS BOXES — each in its own CellGroup
    # ═══════════════════════════════════════════════════════════
    scene_box, _ = class_box(0, 4, 0, 7, "Scene", colors.primary, is_surface=True)
    grid_box, _ = class_box(1, 3, 1, 5, "Grid", colors.primary)
    image_box, _ = class_box(1, 8, 1, 10, "Image", colors.grid)
    cell_box, _ = class_box(2, 1, 2, 3, "Cell", colors.primary, is_surface=True)
    cg_box, _ = class_box(2, 8, 2, 11, "CellGroup", colors.primary, is_surface=True)
    entity_box, _ = class_box(3, 4, 3, 6, "Entity", colors.secondary)
    conn_box, conn_area = class_box(3, 8, 3, 11, "Connection", colors.secondary)
    conn_area.add_dot(
        at=(0.5, 0.82), radius=0.05,
        color=colors.accent, opacity=0.7,
    )

    # ═══════════════════════════════════════════════════════════
    # CATEGORY PANELS — CellGroups with distributed pills
    # ═══════════════════════════════════════════════════════════
    prim_bg, _ = category(4, 0, 6, 3, "Primitives", [
        ("Dot", False), ("Point", False),
        ("Line", True), ("Curve", True),
    ])
    shape_bg, _ = category(4, 4, 6, 7, "Shapes", [
        ("Rect", False), ("Ellipse", True), ("Polygon", False),
    ])
    comp_bg, _ = category(4, 8, 6, 11, "Composites", [
        ("Text", False), ("Path", True), ("EGroup", False),
    ])

    # ═══════════════════════════════════════════════════════════
    # PATHABLE PROTOCOL + STYLES FOOTNOTE
    # ═══════════════════════════════════════════════════════════
    path_area = g.merge((7, 0), (7, 11))
    path_rect = path_area.add_rect(
        fill=colors.accent, stroke=colors.accent,
        stroke_width=1.5, fill_opacity=0.08, stroke_opacity=0.4,
        width=0.98, height=0.7,
    )
    path_area.add_text(
        "Pathable protocol: point_at(t)",
        within=path_rect, at=(0.5, 0.35),
        fit=True, bold=True, color=colors.accent,
    )
    path_area.add_text(
        "Line  \u00b7  Curve  \u00b7  Ellipse  \u00b7  Path  \u00b7  Connection",
        within=path_rect, at=(0.5, 0.65),
        fit=True, color=LABEL,
    )

    style_area = g.merge((8, 0), (8, 11))
    style_area.add_text(
        "Styles: PathStyle \u00b7 ShapeStyle \u00b7 TextStyle"
        " \u00b7 DotStyle \u00b7 FillStyle \u00b7 BorderStyle",
        font_size=0.11, color=DIM, fit=True,
    )

    # ═══════════════════════════════════════════════════════════
    # CONNECTIONS + LABELS — arrows with text along them
    # ═══════════════════════════════════════════════════════════
    c_grid = scene_box.connect(grid_box, style=ARROW, start_anchor="bottom", end_anchor="top")
    c_img = image_box.connect(grid_box, style=FAINT, start_anchor="left", end_anchor="right")
    c_cell = grid_box.connect(cell_box, style=ARROW, start_anchor="bottom_left", end_anchor="top")
    c_cg = grid_box.connect(cg_box, style=ARROW, start_anchor="bottom_right", end_anchor="left")
    c_ent = cell_box.connect(entity_box, style=ARROW, start_anchor="bottom", end_anchor="top_left")
    c_conn = entity_box.connect(conn_box, style=ARROW, start_anchor="right", end_anchor="left")

    # Inheritance: Entity → category panel backgrounds
    entity_box.connect(prim_bg, style=INHERIT, start_anchor="bottom_left", end_anchor="top")
    entity_box.connect(shape_bg, style=INHERIT, start_anchor="bottom", end_anchor="top")
    entity_box.connect(comp_bg, style=INHERIT, start_anchor="bottom_right", end_anchor="top")

    # Labels along connections (positive along_offset = below the line)
    scene.add_text(".grid", along=c_grid, t=0.5, along_offset=0.01, font_size=0.015, color=LABEL)
    scene.add_text("from_image()", along=c_img, t=0.5, along_offset=0.015, font_size=0.013, color=LABEL)
    scene.add_text("has", along=c_cell, t=0.3, along_offset=0.02, font_size=0.015, color=LABEL)
    scene.add_text(".merge()", along=c_cg, t=0.5, along_offset=0.02, font_size=0.013, color=LABEL)
    scene.add_text("add_*()", along=c_ent, t=0.5, along_offset=0.02, font_size=0.014, color=LABEL)
    scene.add_text(".connect()", along=c_conn, t=0.5, along_offset=0.015, font_size=0.013, color=LABEL)

    save(scene, "api-reference/relationship-map.svg")
