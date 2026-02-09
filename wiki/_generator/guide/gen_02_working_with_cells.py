"""Generate SVGs for Guide: Working with Cells."""

import math

from pyfreeform import Scene, Palette, Polygon, map_range

from wiki._generator import save, sample_image


def generate():
    colors = Palette.midnight()

    # --- 1. Brightness to radius (classic dot art) ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=40,
        cell_size=10,
    )
    for cell in scene.grid:
        r = cell.brightness * 0.48
        if r > 0.03:
            cell.add_dot(radius=r, color="#ffffff")
    save(scene, "guide/cells-brightness-radius.svg")

    # --- 2. Brightness to color (gradient mapping) ---
    scene = Scene.from_image(
        sample_image("gradient.png"),
        grid_size=35,
        cell_size=10,
    )
    for cell in scene.grid:
        cell.add_fill(color=cell.color)
    save(scene, "guide/cells-color-fill.svg")

    # --- 3. Brightness driving rotation ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=30,
        cell_size=14,
    )
    for cell in scene.grid:
        rotation = cell.brightness * 90
        size = 0.4 + cell.brightness * 0.4
        cell.add_polygon(
            Polygon.square(size=size),
            fill=cell.color,
            opacity=0.7,
            rotation=rotation,
        )
    save(scene, "guide/cells-brightness-rotation.svg")

    # --- 4. Edge detection using neighbors ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=50,
        cell_size=8,
    )
    for cell in scene.grid:
        # Simple edge detection: compare brightness with right and below neighbors
        edge = 0.0
        if cell.right:
            edge += abs(cell.brightness - cell.right.brightness)
        if cell.below:
            edge += abs(cell.brightness - cell.below.brightness)
        edge = min(edge * 3, 1.0)  # Amplify
        if edge > 0.1:
            cell.add_dot(radius=edge * 0.4375, color="#00d9ff", opacity=edge)
    save(scene, "guide/cells-edge-detection.svg")

    # --- 5. Radial effect with distance_to ---
    colors_ocean = Palette.ocean()
    scene = Scene.with_grid(cols=20, rows=20, cell_size=16, background=colors_ocean.background)
    center = scene.grid[10, 10]
    max_d = center.distance_to(scene.grid[0, 0])
    for cell in scene.grid:
        d = cell.distance_to(center)
        t = 1 - (d / max_d)
        radius = t * 0.4375
        if radius > 0.03125:
            cell.add_dot(radius=radius, color=colors_ocean.primary, opacity=0.3 + t * 0.7)
    save(scene, "guide/cells-distance-radial.svg")

    # --- 6. Normalized position for gradient effects ---
    colors_sunset = Palette.sunset()
    scene = Scene.with_grid(cols=16, rows=12, cell_size=20, background=colors_sunset.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        # Create a cross-fade from primary (left) to accent (right)
        r1, g1, b1 = int(colors_sunset.primary[1:3], 16), int(colors_sunset.primary[3:5], 16), int(colors_sunset.primary[5:7], 16)
        r2, g2, b2 = int(colors_sunset.accent[1:3], 16), int(colors_sunset.accent[3:5], 16), int(colors_sunset.accent[5:7], 16)
        r = int(r1 + (r2 - r1) * nx)
        g = int(g1 + (g2 - g1) * nx)
        b = int(b1 + (b2 - b1) * nx)
        color = f"#{r:02x}{g:02x}{b:02x}"
        size = 0.3 + ny * 0.5
        cell.add_polygon(
            Polygon.diamond(size=size),
            fill=color,
            opacity=0.5 + ny * 0.5,
        )
    save(scene, "guide/cells-normalized-position.svg")

    # --- 7. Sub-cell sampling ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=25,
        cell_size=16,
    )
    for cell in scene.grid:
        # Sample 4 quadrants of each cell for higher detail
        positions = [
            ((0.25, 0.25), "top_left"),
            ((0.75, 0.25), "top_right"),
            ((0.25, 0.75), "bottom_left"),
            ((0.75, 0.75), "bottom_right"),
        ]
        for (rx, ry), pos in positions:
            try:
                color = cell.sample_hex(rx, ry)
                brightness = cell.sample_brightness(rx, ry)
                r = brightness * 0.219
                if r > 0.019:
                    cell.add_dot(at=pos, radius=r, color=color)
            except (IndexError, AttributeError):
                # Cell may not have image data
                pass
    save(scene, "guide/cells-sub-sampling.svg")

    # --- 8. Where selection with brightness threshold ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=35,
        cell_size=12,
    )
    # Dark cells get fills, bright cells get stars
    for cell in scene.grid.where(lambda c: c.brightness < 0.4):
        cell.add_fill(color=cell.color, opacity=0.5)
    for cell in scene.grid.where(lambda c: c.brightness >= 0.4):
        size = 0.3 + cell.brightness * 0.5
        cell.add_polygon(
            Polygon.star(points=4, size=size, inner_ratio=0.5),
            fill=cell.color,
            opacity=0.7,
        )
    save(scene, "guide/cells-where-threshold.svg")
