"""Generate SVGs for Getting Started: Your First Artwork."""

import math

from pyfreeform import Scene, Palette, Polygon, map_range

from wiki._generator import save, sample_image


def generate():
    # ===== FROM AN IMAGE TAB =====

    # Step 1: Load image and add simple dots
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=35,
        cell_size=12,
    )
    for cell in scene.grid:
        cell.add_dot(radius=3, color=cell.color)
    save(scene, "getting-started/first-image-step1.svg")

    # Step 2: Size dots by brightness
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=35,
        cell_size=12,
    )
    for cell in scene.grid:
        radius = cell.brightness * 5
        if radius > 0.3:
            cell.add_dot(radius=radius, color=cell.color)
    save(scene, "getting-started/first-image-step2.svg")

    # Step 3: Final polish — add border, vary opacity
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=40,
        cell_size=11,
    )
    for cell in scene.grid:
        radius = cell.brightness * 5
        if radius > 0.3:
            cell.add_dot(
                radius=radius,
                color=cell.color,
                opacity=0.6 + cell.brightness * 0.4,
            )
    for cell in scene.grid.border():
        cell.add_border(color="#333344", width=0.3)
    save(scene, "getting-started/first-image-step3.svg")

    # ===== FROM SCRATCH TAB =====

    # Step 1: Checkerboard with fills
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=25, background=colors.background)
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.7)
        else:
            cell.add_fill(color=colors.secondary, opacity=0.3)
    save(scene, "getting-started/first-scratch-step1.svg")

    # Step 2: Add shapes based on position
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=25, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.15)
        size = 0.3 + t * 0.5
        rotation = t * 45
        cell.add_polygon(
            Polygon.diamond(size=size),
            fill=colors.accent,
            opacity=0.4 + t * 0.6,
            rotation=rotation,
        )
    save(scene, "getting-started/first-scratch-step2.svg")

    # Step 3: Layer curves on top for flow
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=25, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.1)
        size = 0.3 + t * 0.5
        rotation = t * 45
        cell.add_polygon(
            Polygon.diamond(size=size),
            fill=colors.accent,
            opacity=0.3 + t * 0.5,
            rotation=rotation,
        )
        # Add a curve for flow
        curvature = math.sin(nx * math.pi * 2) * 0.6
        cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            width=0.8,
            color=colors.line,
            opacity=0.3 + ny * 0.4,
        )
    save(scene, "getting-started/first-scratch-step3.svg")
