"""Generate SVGs for the Home page."""

import math

from pyfreeform import Scene, Palette, Polygon, map_range

from wiki._generator import save, sample_image


def generate():
    # --- Hero: Mona Lisa dot art with color ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=50,
        cell_size=10,
    )
    for cell in scene.grid:
        r = cell.brightness * 0.48
        if r > 0.05:
            cell.add_dot(radius=r, color=cell.color)
    save(scene, "home/hero-mona-lisa.svg")

    # --- Snippet 1: Geometric pattern (hexagons with rotation) ---
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=30, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        hue_shift = t
        fill = colors.primary if (cell.row + cell.col) % 3 == 0 else colors.secondary
        rotation = t * 60
        cell.add_polygon(
            Polygon.hexagon(size=0.75),
            fill=fill,
            opacity=0.5 + t * 0.5,
            rotation=rotation,
        )
    save(scene, "home/snippet-hexagons.svg")

    # --- Snippet 2: Flowing curves ---
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=20, rows=15, cell_size=18, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        curvature = math.sin(nx * math.pi * 3) * 0.8
        width = 1 + ny * 2
        cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=curvature,
            width=width,
            color=colors.primary,
            opacity=0.4 + nx * 0.6,
        )
    save(scene, "home/snippet-curves.svg")

    # --- Snippet 3: Stars sized by distance from center ---
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=15, rows=15, cell_size=24, background=colors.background)
    center_cell = scene.grid[scene.grid.rows // 2, scene.grid.cols // 2]
    max_dist = center_cell.distance_to(scene.grid[0, 0])
    for cell in scene.grid:
        d = cell.distance_to(center_cell)
        t = 1 - (d / max_dist)  # 1 at center, 0 at corners
        size = 0.3 + t * 0.6
        cell.add_polygon(
            Polygon.star(points=5, size=size, inner_ratio=0.4),
            fill=colors.primary if t > 0.5 else colors.accent,
            opacity=0.3 + t * 0.7,
        )
    save(scene, "home/snippet-stars.svg")
