"""Generate SVGs for Recipe: Advanced Compositions."""

from pyfreeform import (
    Scene,
    Palette,
    Polygon,
    EntityGroup,
    Dot,
    Line,
    Ellipse,
    ConnectionStyle,
)

from wiki._generator import save, sample_image


def generate():
    # --- 1. Multi-layer artwork ---
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=16, rows=12, cell_size=20, background=colors.background)

    # Layer 0: subtle grid lines
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.3, opacity=0.15, z_index=0)

    # Layer 1: faded hexagons
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        cell.add_polygon(
            Polygon.hexagon(size=0.6),
            fill=colors.secondary,
            opacity=0.1 + t * 0.15,
            z_index=1,
        )

    # Layer 2: diagonal lines
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        cell.add_diagonal(
            width=0.5 + nx * 1.5,
            color=colors.primary,
            opacity=0.2 + ny * 0.3,
            z_index=2,
        )

    # Layer 3: dots at intersections
    for cell in scene.grid.every(3):
        nx, ny = cell.normalized_position
        cell.add_dot(
            radius=0.15 + nx * 0.2,
            color=colors.accent,
            opacity=0.7,
            z_index=3,
        )
    save(scene, "recipes/adv-multi-layer.svg")

    # --- 2. EntityGroup reusable motifs ---
    def make_crosshair(color1, color2):
        g = EntityGroup()
        g.add(Dot(0, 0, radius=8, color=color1, opacity=0.6))
        g.add(Line(-12, 0, 12, 0, width=1, color=color2, opacity=0.5))
        g.add(Line(0, -12, 0, 12, width=1, color=color2, opacity=0.5))
        g.add(
            Ellipse(0, 0, rx=10, ry=10, fill="none", stroke=color2, stroke_width=0.5, opacity=0.3)
        )
        return g

    colors = Palette.ocean()
    scene = Scene.with_grid(cols=8, rows=6, cell_size=38, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        group = make_crosshair(colors.primary, colors.secondary)
        cell.add(group)
        group.fit_to_cell(0.8)
        group.rotate(nx * 45)
    save(scene, "recipes/adv-entity-groups.svg")

    # --- 3. CellGroup merged regions ---
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=12, rows=10, cell_size=22, background=colors.background)

    # Background pattern
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        cell.add_polygon(
            Polygon.diamond(size=0.4),
            fill=colors.secondary,
            opacity=0.15,
        )

    # Merge center region for a feature area
    feature = scene.grid.merge((2, 3), (7, 8))
    feature.add_fill(color=colors.primary, opacity=0.15)
    feature.add_border(color=colors.accent, width=1.5, opacity=0.6)
    feature.add_text(
        "FEATURED",
        at="center",
        font_size=0.10,
        color=colors.accent,
        bold=True,
        fit=True,
    )

    # Merge top for title
    title = scene.grid.merge_row(0)
    title.add_fill(color=colors.primary, opacity=0.2)
    title.add_text("COMPOSITION", at="center", font_size=0.55, color=colors.accent)
    save(scene, "recipes/adv-cell-groups.svg")

    # --- 4. Combined: image + geometry + connections ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=25,
        cell_size=16,
    )
    # Layer 0: faded image fills
    for cell in scene.grid:
        cell.add_fill(color=cell.color, opacity=0.25, z_index=0)

    # Layer 1: shapes by brightness
    for cell in scene.grid:
        b = cell.brightness
        if b > 0.3:
            size = 0.3 + b * 0.4
            cell.add_polygon(
                Polygon.hexagon(size=size),
                fill=cell.color,
                opacity=0.5,
                z_index=1,
            )

    # Layer 2: connect bright dots
    dots = {}
    for cell in scene.grid:
        if cell.brightness > 0.55:
            dot = cell.add_dot(
                radius=0.15,
                color="#ffffff",
                opacity=0.7,
                z_index=2,
            )
            dots[(cell.row, cell.col)] = dot

    conn_style = ConnectionStyle(width=0.4, color="#ffffff", opacity=0.15)
    for (r, c), dot in dots.items():
        for dr, dc in [(0, 1), (1, 0)]:
            key = (r + dr, c + dc)
            if key in dots:
                dot.connect(dots[key], style=conn_style)

    # Title overlay
    title = scene.grid.merge((0, 0), (1, scene.grid.num_columns - 1))
    title.add_fill(color="#000000", opacity=0.5, z_index=3)
    title.add_text(
        "LAYERED ART", at="center", font_size=0.45, color="#ffffff", bold=True, z_index=4
    )
    save(scene, "recipes/adv-combined.svg")
