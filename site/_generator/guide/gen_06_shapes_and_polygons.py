"""Generate SVGs for Guide: Shapes and Polygons."""

import math

from pyfreeform import (
    Scene, Palette, Polygon, EntityGroup, Dot, Line, Ellipse, map_range,
)

from wiki_v2._generator import save, sample_image


def generate():
    colors = Palette.midnight()

    # --- 1. Shape classmethod gallery ---
    shapes = [
        ("triangle", Polygon.triangle(size=0.7)),
        ("square", Polygon.square(size=0.7)),
        ("diamond", Polygon.diamond(size=0.7)),
        ("hexagon", Polygon.hexagon(size=0.7)),
        ("star", Polygon.star(points=5, size=0.7)),
        ("octagon", Polygon.regular_polygon(sides=8, size=0.7)),
        ("squircle", Polygon.squircle(size=0.7)),
        ("rounded", Polygon.rounded_rect(size=0.7, corner_radius=0.25)),
    ]
    scene = Scene.with_grid(cols=8, rows=2, cell_size=50, background=colors.background)
    for i, (name, verts) in enumerate(shapes):
        cell = scene.grid[0, i]
        cell.add_polygon(verts, fill=colors.primary, opacity=0.8)
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
    for i, (name, _) in enumerate(shapes):
        cell = scene.grid[1, i]
        cell.add_text(name, at="center", font_size=9, color="#aaaacc")
    save(scene, "guide/shapes-gallery.svg")

    # --- 2. Hexagonal grid ---
    colors_ocean = Palette.ocean()
    scene = Scene.with_grid(cols=14, rows=14, cell_size=20, background=colors_ocean.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        cell.add_polygon(
            Polygon.hexagon(size=0.85),
            fill=colors_ocean.primary,
            opacity=0.2 + t * 0.6,
            stroke=colors_ocean.secondary,
            stroke_width=0.5,
        )
    save(scene, "guide/shapes-hex-grid.svg")

    # --- 3. Stars sized by brightness ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=25,
        cell_size=16,
    )
    for cell in scene.grid:
        size = 0.3 + cell.brightness * 0.5
        inner = 0.3 + cell.brightness * 0.2
        cell.add_polygon(
            Polygon.star(points=5, size=size, inner_ratio=inner),
            fill=cell.color,
            opacity=0.6 + cell.brightness * 0.4,
        )
    save(scene, "guide/shapes-stars-brightness.svg")

    # --- 4. EntityGroup: flower pattern ---
    def make_flower(petal_color, center_color):
        """Create a flower EntityGroup."""
        group = EntityGroup()
        # 6 petals around center
        for i in range(6):
            angle = i * 60 * math.pi / 180
            px, py = 12 * math.cos(angle), 12 * math.sin(angle)
            group.add(Ellipse(px, py, rx=8, ry=4, rotation=i * 60, fill=petal_color, opacity=0.7))
        # Center dot
        group.add(Dot(0, 0, radius=5, color=center_color))
        return group

    colors_pastel = Palette.pastel()
    scene = Scene.with_grid(cols=6, rows=5, cell_size=48, background=colors_pastel.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        flower = make_flower(colors_pastel.primary, colors_pastel.accent)
        cell.place(flower)
        flower.fit_to_cell(0.85)
    save(scene, "guide/shapes-entity-group.svg")

    # --- 5. fit_to_cell demo ---
    colors_sunset = Palette.sunset()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=60, background=colors_sunset.background)
    fractions = [0.3, 0.5, 0.7, 0.9, 1.0]
    for i, cell in enumerate(scene.grid):
        frac = fractions[i]
        group = EntityGroup()
        group.add(Dot(0, 0, radius=20, color=colors_sunset.primary))
        group.add(Line(-15, -15, 15, 15, width=2, color=colors_sunset.accent))
        group.add(Line(-15, 15, 15, -15, width=2, color=colors_sunset.accent))
        cell.place(group)
        group.fit_to_cell(frac)
        cell.add_text(
            f"{frac:.0%}",
            at="bottom",
            font_size=10,
            color="#aaaacc",
        )
        cell.add_border(color=colors_sunset.grid, width=0.5, opacity=0.3)
    save(scene, "guide/shapes-fit-to-cell.svg")

    # --- 6. fit_to_cell with rotation ---
    scene = Scene.with_grid(cols=6, rows=6, cell_size=40, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        rotation = (nx + ny) * 180
        group = EntityGroup()
        group.add(Dot(0, 0, radius=12, color=colors.primary, opacity=0.7))
        group.add(Line(-10, 0, 10, 0, width=2, color=colors.accent))
        group.add(Line(0, -10, 0, 10, width=2, color=colors.accent))
        cell.place(group)
        group.fit_to_cell(0.75)
        group.rotate(rotation)
    save(scene, "guide/shapes-fit-rotated.svg")
