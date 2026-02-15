"""Generate SVGs for Recipe: Geometric Patterns."""

import math

from pyfreeform import Scene, Palette, Polygon

from wiki._generator import save


def generate():
    # --- 1. Checkerboard with alternating shapes ---
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=14, rows=14, cell_size=20, background=colors.background)
    for cell in scene.grid.checkerboard("black"):
        cell.add_polygon(
            Polygon.diamond(size=0.75),
            fill=colors.primary,
            opacity=0.7,
        )
    for cell in scene.grid.checkerboard("white"):
        cell.add_polygon(
            Polygon.hexagon(size=0.6),
            fill=colors.accent,
            opacity=0.5,
        )
    save(scene, "recipes/geo-checkerboard.svg")

    # --- 2. Rotating hexagonal tiling ---
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=16, rows=16, cell_size=18, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        rotation = (nx * ny) * 120
        t = math.sqrt(nx * nx + ny * ny) / 1.414
        cell.add_polygon(
            Polygon.hexagon(size=0.8),
            fill=colors.primary,
            stroke=colors.secondary,
            stroke_width=0.5,
            opacity=0.3 + t * 0.6,
            rotation=rotation,
        )
    save(scene, "recipes/geo-rotating-hex.svg")

    # --- 3. Sine wave pattern ---
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=20, rows=15, cell_size=16, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        wave = math.sin(nx * math.pi * 4 + ny * math.pi * 2)
        size = 0.3 + abs(wave) * 0.5
        rotation = wave * 45
        cell.add_polygon(
            Polygon.diamond(size=size),
            fill=colors.primary if wave > 0 else colors.accent,
            opacity=0.4 + abs(wave) * 0.6,
            rotation=rotation,
        )
    save(scene, "recipes/geo-sine-wave.svg")

    # --- 4. Concentric rings ---
    colors = Palette.neon()
    scene = Scene.with_grid(cols=20, rows=20, cell_size=16, background=colors.background)
    center = scene.grid[10][10]
    max_d = center.distance_to(scene.grid[0][0])
    for cell in scene.grid:
        d = cell.distance_to(center)
        t = d / max_d
        ring = int(t * 8) % 2
        if ring == 0:
            cell.add_polygon(
                Polygon.hexagon(size=0.7),
                fill=colors.primary,
                opacity=0.4 + (1 - t) * 0.5,
            )
        else:
            cell.add_dot(radius=0.15 + (1 - t) * 0.20, color=colors.secondary, opacity=0.5)
    save(scene, "recipes/geo-concentric.svg")

    # --- 5. Star grid with position-driven parameters ---
    colors = Palette.forest()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=24, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        points = 4 + int(nx * 4)  # 4 to 8 points
        inner_ratio = 0.2 + ny * 0.4
        cell.add_polygon(
            Polygon.star(points=points, size=0.7, inner_ratio=inner_ratio),
            fill=colors.primary,
            opacity=0.4 + (nx + ny) / 2 * 0.6,
        )
    save(scene, "recipes/geo-star-grid.svg")
