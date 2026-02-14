"""Generate SVGs for Getting Started: How PyFreeform Works."""

from pyfreeform import Scene, Palette, Polygon
from pyfreeform.core import NAMED_POSITIONS

from wiki._generator import save


def generate():
    colors = Palette.midnight()

    # --- 1. The mental model: Scene > Grid > Cells > Entities ---
    # Show a small grid with visible borders, a few cells with entities
    scene = Scene.with_grid(cols=6, rows=6, cell_size=40, background=colors.background)
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.5)

    # Highlight a few cells with different entities to show variety
    scene.grid[1, 1].add_dot(radius=0.3, color=colors.primary)
    scene.grid[1, 2].add_dot(radius=0.2, color=colors.secondary)
    scene.grid[2, 1].add_line(start="bottom_left", end="top_right", width=2, color=colors.accent).fit_to_cell()
    scene.grid[2, 2].add_fill(color=colors.primary, opacity=0.3)
    scene.grid[2, 2].add_dot(radius=0.15, color=colors.accent)
    scene.grid[3, 3].add_polygon(Polygon.hexagon(size=0.7), fill=colors.secondary, opacity=0.7)
    scene.grid[3, 4].add_curve(
        start="bottom_left",
        end="top_right",
        curvature=0.5,
        width=2,
        color=colors.primary,
    ).fit_to_cell()
    scene.grid[4, 2].add_polygon(Polygon.star(points=5, size=0.65), fill=colors.accent, opacity=0.8)
    save(scene, "getting-started/how-mental-model.svg")

    # --- 2. Named positions within a cell ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=160, background=colors.background)
    cell = scene.grid[0, 0]
    cell.add_border(color=colors.grid, width=1)
    # (position, dot_color, radius, baseline, text_anchor)
    positions = [
        ("center", colors.primary, 0.05, "middle", "middle"),
        ("top_left", colors.accent, 0.05, "hanging", "start"),
        ("top_right", colors.accent, 0.05, "hanging", "end"),
        ("bottom_left", colors.accent, 0.05, "auto", "start"),
        ("bottom_right", colors.accent, 0.05, "auto", "end"),
        ("top", colors.secondary, 0.05, "hanging", "middle"),
        ("bottom", colors.secondary, 0.05, "auto", "middle"),
        ("left", colors.secondary, 0.05, "middle", "start"),
        ("right", colors.secondary, 0.05, "middle", "end"),
    ]
    for pos_name, color, radius, baseline, anchor in positions:
        if pos_name in NAMED_POSITIONS:
            cell.add_dot(at=pos_name, radius=radius, color=color)
            cell.add_text(
                pos_name,
                at=pos_name,
                font_size=0.05,
                color="#aaaacc",
                baseline=baseline,
                text_anchor=anchor,
                fit=True,
            )
    save(scene, "getting-started/how-named-positions.svg")

    # --- 3. The Surface protocol: same methods on Cell and Scene ---
    # Show cell-level and scene-level entities side by side
    scene = Scene.with_grid(cols=8, rows=6, cell_size=30, background=colors.background)
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)

    # Cell-level: dots in each cell of top-left region
    for cell in scene.grid.region(0, 3, 0, 4):
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        cell.add_dot(radius=0.15 + t * 0.2, color=colors.primary, opacity=0.5 + t * 0.5)

    # Scene-level: place entities directly
    from pyfreeform import Dot, Line

    scene.place(Dot(160, 110, radius=15, color=colors.accent, opacity=0.8, z_index=1))
    scene.place(Line(140, 90, 220, 160, width=2, color=colors.secondary, opacity=0.6, z_index=2))
    save(scene, "getting-started/how-surface-protocol.svg")

    # --- 4. z_index layering demo ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=180, background=colors.background)
    cell = scene.grid[0, 0]
    # Background fill
    cell.add_fill(color="#2a2a4e", z_index=0)
    # Large circle behind
    cell.add_ellipse(
        at="center",
        rx=0.33,
        ry=0.33,
        fill=colors.primary,
        opacity=0.4,
        z_index=1,
    )
    # Medium shape in middle
    cell.add_polygon(
        Polygon.hexagon(size=0.5),
        fill=colors.accent,
        opacity=0.7,
        z_index=2,
    )
    # Small dot on top
    cell.add_dot(at="center", radius=0.10, color="#ffffff", z_index=3)
    # Text on very top
    cell.add_text(
        "z=3",
        at="center",
        font_size=0.05,
        color=colors.background,
        z_index=4,
    )
    save(scene, "getting-started/how-z-index.svg")
