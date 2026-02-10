"""Generate SVGs for Guide: Transforms and Layout."""

import math

from pyfreeform import (
    Scene, Palette, Polygon, EntityGroup, Dot, Line, Ellipse,
    Connection, ConnectionStyle, map_range,
)

from wiki._generator import save


def generate():
    colors = Palette.midnight()

    # --- 1. Rotation grid ---
    scene = Scene.with_grid(cols=10, rows=10, cell_size=26, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        rotation = (nx + ny) * 180
        cell.add_polygon(
            Polygon.square(size=0.6),
            fill=colors.primary,
            opacity=0.5 + nx * 0.5,
            rotation=rotation,
        )
    save(scene, "guide/transforms-rotation-grid.svg")

    # --- 2. Scale comparison ---
    scene = Scene.with_grid(cols=6, rows=1, cell_size=50, background=colors.background)
    scales = [0.2, 0.4, 0.6, 0.8, 0.9, 1.0]
    for i, cell in enumerate(scene.grid):
        s = scales[i]
        group = EntityGroup()
        group.add(Dot(0, 0, radius=15, color=colors.primary))
        group.add(Line(-10, -10, 10, 10, width=2, color=colors.accent))
        cell.add(group)
        group.fit_to_cell(s)
        cell.add_text(f"{s:.1f}", at="bottom", font_size=0.25, color="#aaaacc")
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
    save(scene, "guide/transforms-scale.svg")

    # --- 3. fit_to_cell with at= positions ---
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80, background=colors.background)
    positions = [
        ((0.15, 0.15), "top_left"),
        ((0.5, 0.5), "center"),
        ((0.85, 0.85), "bottom_right"),
    ]
    for i, cell in enumerate(scene.grid):
        at_pos, label = positions[i]
        group = EntityGroup()
        group.add(Dot(0, 0, radius=18, color=colors.primary, opacity=0.7))
        group.add(Line(-12, 0, 12, 0, width=2, color=colors.accent))
        cell.add(group)
        group.fit_to_cell(0.5, at=at_pos)
        cell.add_text(label, at="bottom", font_size=0.25, color="#aaaacc")
        cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    save(scene, "guide/transforms-fit-at.svg")

    # --- 4. Connected network ---
    colors_ocean = Palette.ocean()
    scene = Scene.with_grid(cols=6, rows=5, cell_size=40, background=colors_ocean.background)
    # Place dots in select cells and connect neighbors
    dots = {}
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            dot = cell.add_dot(radius=0.15, color=colors_ocean.primary, opacity=0.8)
            dots[(cell.row, cell.col)] = dot

    conn_style = ConnectionStyle(width=1, color=colors_ocean.line, opacity=0.4)
    for (r, c), dot in dots.items():
        # Connect to right neighbor
        if (r, c + 2) in dots:
            conn = dot.connect(dots[(r, c + 2)], shape=Line(), style=conn_style)
            scene.add(conn)
        # Connect to below neighbor
        if (r + 2, c) in dots:
            conn = dot.connect(dots[(r + 2, c)], shape=Line(), style=conn_style)
            scene.add(conn)
    save(scene, "guide/transforms-connections.svg")

    # --- 5. Arrow caps on connections ---
    scene = Scene.with_grid(cols=4, rows=3, cell_size=50, background=colors.background)
    dots_arr = {}
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            dot = cell.add_dot(radius=0.12, color=colors.accent, opacity=0.8)
            dots_arr[(cell.row, cell.col)] = dot

    arrow_style = ConnectionStyle(
        width=1.5, color=colors.primary, opacity=0.6, end_cap="arrow",
    )
    for (r, c), dot in dots_arr.items():
        if (r, c + 2) in dots_arr:
            conn = dot.connect(dots_arr[(r, c + 2)], shape=Line(), style=arrow_style)
            scene.add(conn)
        if (r + 2, c) in dots_arr:
            conn = dot.connect(dots_arr[(r + 2, c)], shape=Line(), style=arrow_style)
            scene.add(conn)
    save(scene, "guide/transforms-arrow-caps.svg")

    # --- 6. z_index layering showcase ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200, background=colors.background)
    cell = scene.grid[0, 0]
    # Layer 0: grid of faint lines
    for i in range(1, 10):
        t = i / 10
        cell.add_line(start=(t, 0), end=(t, 1), width=0.5, color=colors.grid, opacity=0.3, z_index=0)
        cell.add_line(start=(0, t), end=(1, t), width=0.5, color=colors.grid, opacity=0.3, z_index=0)
    # Layer 1: large faded ellipse
    cell.add_ellipse(
        at="center", rx=0.35, ry=0.35,
        fill=colors.primary, opacity=0.2, z_index=1,
    )
    # Layer 2: hexagon
    cell.add_polygon(
        Polygon.hexagon(size=0.4),
        fill=colors.accent, opacity=0.6, z_index=2,
    )
    # Layer 3: central dot
    cell.add_dot(at="center", radius=0.06, color="#ffffff", opacity=0.9, z_index=3)
    save(scene, "guide/transforms-z-index.svg")

    # --- 7. map_range utility ---
    colors_sunset = Palette.sunset()
    scene = Scene.with_grid(cols=15, rows=10, cell_size=20, background=colors_sunset.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        # Convert position (0–1) to visual parameters
        radius = map_range(nx, 0, 1, 2, 9)
        rotation = map_range(ny, 0, 1, 0, 90)
        cell.add_polygon(
            Polygon.diamond(size=0.6),
            fill=colors_sunset.primary,
            opacity=map_range(nx + ny, 0, 2, 0.3, 1.0),
            rotation=rotation,
        )
    save(scene, "guide/transforms-map-range.svg")
