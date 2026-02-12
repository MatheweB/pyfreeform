"""Generate SVGs for Guide: Drawing with Entities."""

import math

from pyfreeform import Scene, Palette, Polygon, Path

from wiki._generator import save, sample_image


def generate():
    # Each entity gets a unique, creative showcase — no repetitive patterns.

    # --- 1. Dots: brightness-driven size and opacity on gradient ---
    scene = Scene.from_image(
        sample_image("gradient.png"),
        grid_size=30,
        cell_size=12,
    )
    for cell in scene.grid:
        r = 0.083 + cell.brightness * 0.417
        cell.add_dot(
            radius=r,
            color=cell.color,
            opacity=0.4 + cell.brightness * 0.6,
        )
    save(scene, "guide/entities-dots.svg")

    # --- 2. Lines: flow direction from brightness gradient ---
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=18, rows=14, cell_size=18, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        # Angle driven by sine wave
        angle = math.sin(nx * math.pi * 2) * math.cos(ny * math.pi) * 0.4
        dx = math.cos(angle) * 0.4
        dy = math.sin(angle) * 0.4
        start = (0.5 - dx, 0.5 - dy)
        end = (0.5 + dx, 0.5 + dy)
        width = 0.5 + ny * 2
        cell.add_line(
            start=start,
            end=end,
            width=width,
            color=colors.primary,
            opacity=0.3 + nx * 0.7,
        )
    save(scene, "guide/entities-lines.svg")

    # --- 3. Curves: curvature driven by position, wave texture ---
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=16, rows=12, cell_size=20, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        curvature = math.sin(nx * math.pi * 3 + ny * 2) * 0.8
        width = 0.8 + abs(curvature) * 2
        cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=curvature,
            width=width,
            color=colors.primary,
            opacity=0.4 + ny * 0.5,
        )
    save(scene, "guide/entities-curves.svg")

    # --- 4. Ellipses: rotation moire pattern ---
    colors = Palette.neon()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=26, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        rotation = (nx + ny) * 90
        cell.add_ellipse(
            at="center",
            rx=0.4,
            ry=0.2,
            rotation=rotation,
            fill=colors.primary,
            stroke=colors.secondary,
            stroke_width=0.5,
            opacity=0.6,
        )
    save(scene, "guide/entities-ellipses.svg")

    # --- 5. Rectangles: rotation & opacity mosaic ---
    colors = Palette.forest()
    scene = Scene.with_grid(cols=14, rows=10, cell_size=22, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        rotation = t * 45
        cell.add_rect(
            at="center",
            width=0.4 + t * 0.4,
            height=0.4 + (1 - t) * 0.4,
            rotation=rotation,
            fill=colors.primary if (cell.row + cell.col) % 2 == 0 else colors.accent,
            opacity=0.3 + t * 0.6,
        )
    save(scene, "guide/entities-rects.svg")

    # --- 6. Polygons: different shapes per brightness band ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=25,
        cell_size=16,
    )
    for cell in scene.grid:
        b = cell.brightness
        size = 0.4 + b * 0.4
        if b < 0.25:
            verts = Polygon.triangle(size=size)
        elif b < 0.5:
            verts = Polygon.diamond(size=size)
        elif b < 0.75:
            verts = Polygon.hexagon(size=size)
        else:
            verts = Polygon.star(points=5, size=size, inner_ratio=0.4)
        cell.add_polygon(verts, fill=cell.color, opacity=0.7 + b * 0.3)
    save(scene, "guide/entities-polygons.svg")

    # --- 7. Text: letters from the alphabet ---
    colors = Palette.paper()
    scene = Scene.with_grid(cols=10, rows=5, cell_size=36, background=colors.background)
    alphabet = "PYFREEFORM" * 5
    for i, cell in enumerate(scene.grid):
        char = alphabet[i % len(alphabet)]
        nx, ny = cell.normalized_position
        size = 0.33 + ny * 0.39
        cell.add_text(
            char,
            at="center",
            font_size=size,
            color=colors.primary,
            bold=True,
            opacity=0.4 + nx * 0.6,
        )
    save(scene, "guide/entities-text.svg")

    # --- 8. Paths: spiral in each cell (using built-in Path.Spiral) ---

    colors = Palette.midnight()
    scene = Scene.with_grid(cols=8, rows=8, cell_size=34, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        cx, cy = cell.center
        max_r = scene.grid.cell_width * 0.4
        spiral = Path.Spiral(center=(cx, cy), end_radius=max_r, turns=2 + nx * 2)
        cell.add_path(
            spiral,
            segments=48,
            width=0.8 + ny * 1.5,
            color=colors.primary,
            opacity=0.4 + nx * 0.6,
        )
    save(scene, "guide/entities-paths.svg")
