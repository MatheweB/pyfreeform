"""Generate SVGs for Recipe: Connected Networks."""

import math

from pyfreeform import Scene, Palette, ConnectionStyle

from wiki._generator import save, sample_image


def generate():
    # --- 1. Bright dots connected to neighbors ---
    colors = Palette.midnight()
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=30,
        cell_size=14,
    )
    dots = {}
    for cell in scene.grid:
        if cell.brightness > 0.35:
            dot = cell.add_dot(
                radius=2 + cell.brightness * 3,
                color=cell.color,
                opacity=0.7,
            )
            dots[(cell.row, cell.col)] = dot

    conn_style = ConnectionStyle(width=0.5, color=colors.line, opacity=0.3)
    for (r, c), dot in dots.items():
        for dr, dc in [(0, 1), (1, 0)]:
            key = (r + dr, c + dc)
            if key in dots:
                conn = dot.connect(dots[key], style=conn_style)
                scene.add(conn)
    save(scene, "recipes/network-bright-dots.svg")

    # --- 2. Distance-based connections ---
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=12, rows=10, cell_size=26, background=colors.background)
    dots = {}
    for cell in scene.grid:
        if (cell.row + cell.col) % 3 == 0:
            dot = cell.add_dot(radius=4, color=colors.primary, opacity=0.8)
            dots[(cell.row, cell.col)] = dot

    conn_style = ConnectionStyle(width=0.8, color=colors.line, opacity=0.3)
    keys = list(dots.keys())
    for i, key1 in enumerate(keys):
        cell1 = scene.grid[key1[0], key1[1]]
        for key2 in keys[i + 1:]:
            cell2 = scene.grid[key2[0], key2[1]]
            dist = cell1.distance_to(cell2)
            if dist < 80:
                opacity = 0.6 * (1 - dist / 80)
                style = ConnectionStyle(
                    width=0.5 + (1 - dist / 80) * 1.5,
                    color=colors.secondary,
                    opacity=opacity,
                )
                conn = dots[key1].connect(dots[key2], style=style)
                scene.add(conn)
    save(scene, "recipes/network-distance.svg")

    # --- 3. Arrow-cap directed graph ---
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=8, rows=6, cell_size=36, background=colors.background)
    dots = {}
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            dot = cell.add_dot(radius=6, color=colors.accent, opacity=0.8)
            dots[(cell.row, cell.col)] = dot

    arrow_style = ConnectionStyle(
        width=1.5, color=colors.primary, opacity=0.5, end_cap="arrow",
    )
    for (r, c), dot in dots.items():
        # Connect rightward and downward
        for dr, dc in [(0, 2), (2, 0)]:
            key = (r + dr, c + dc)
            if key in dots:
                conn = dot.connect(dots[key], style=arrow_style)
                scene.add(conn)
    save(scene, "recipes/network-arrows.svg")

    # --- 4. Network overlay on image ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=25,
        cell_size=16,
    )
    # Background fills
    for cell in scene.grid:
        cell.add_fill(color=cell.color, opacity=0.3)

    # Dots on bright cells
    dots = {}
    for cell in scene.grid:
        if cell.brightness > 0.4:
            dot = cell.add_dot(
                radius=3,
                color="#ffffff",
                opacity=0.8,
            )
            dots[(cell.row, cell.col)] = dot

    conn_style = ConnectionStyle(width=0.5, color="#ffffff", opacity=0.15)
    for (r, c), dot in dots.items():
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            key = (r + dr, c + dc)
            if key in dots:
                conn = dot.connect(dots[key], style=conn_style)
                scene.add(conn)
    save(scene, "recipes/network-overlay.svg")
