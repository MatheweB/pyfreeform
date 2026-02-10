"""Generate SVGs for Guide: Colors, Styles & Palettes."""

import math

from pyfreeform import (
    Scene, Palette, Polygon, DotStyle, LineStyle, ShapeStyle, map_range,
)

from wiki._generator import save, sample_image


def generate():
    # --- 1. All 8 palettes applied to the same pattern ---
    palette_names = [
        ("midnight", Palette.midnight),
        ("sunset", Palette.sunset),
        ("ocean", Palette.ocean),
        ("forest", Palette.forest),
        ("monochrome", Palette.monochrome),
        ("paper", Palette.paper),
        ("neon", Palette.neon),
        ("pastel", Palette.pastel),
    ]
    for name, palette_fn in palette_names:
        colors = palette_fn()
        scene = Scene.with_grid(cols=8, rows=8, cell_size=22, background=colors.background)
        for cell in scene.grid:
            nx, ny = cell.normalized_position
            t = (nx + ny) / 2
            if (cell.row + cell.col) % 2 == 0:
                cell.add_polygon(
                    Polygon.hexagon(size=0.6 + t * 0.3),
                    fill=colors.primary,
                    opacity=0.5 + t * 0.5,
                )
            else:
                cell.add_dot(
                    radius=0.10 + t * 0.25,
                    color=colors.accent,
                    opacity=0.4 + t * 0.6,
                )
        for cell in scene.grid.border():
            cell.add_border(color=colors.grid, width=0.5)
        save(scene, f"guide/styles-palette-{name}.svg")

    # --- 2. Opacity layering demo ---
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=1, rows=1, cell_size=220, background=colors.background)
    cell = scene.grid[0, 0]
    # Stack semi-transparent circles
    offsets = [(-30, -20), (30, -20), (0, 25)]
    palette_colors = [colors.primary, colors.secondary, colors.accent]
    for (dx, dy), fill in zip(offsets, palette_colors):
        cx, cy = cell.center
        cell.add_ellipse(
            at=(0.5 + dx / cell.width, 0.5 + dy / cell.height),
            rx=0.25, ry=0.25,
            fill=fill,
            opacity=0.5,
        )
    save(scene, "guide/styles-opacity-layers.svg")

    # --- 3. fill= vs color= demo ---
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=6, rows=2, cell_size=44, background=colors.background)

    # Row 0: entities that use color=
    labels_color = ["Dot", "Line", "Curve", "Text", "Fill", "Border"]
    for i, cell in enumerate(scene.grid.row(0)):
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
        if i == 0:
            cell.add_dot(radius=0.25, color=colors.primary)
        elif i == 1:
            cell.add_line(start="bottom_left", end="top_right", width=3, color=colors.primary)
        elif i == 2:
            cell.add_curve(start="bottom_left", end="top_right", curvature=0.5, width=2, color=colors.primary)
        elif i == 3:
            cell.add_text("Aa", at="center", font_size=0.45, color=colors.primary, bold=True)
        elif i == 4:
            cell.add_fill(color=colors.primary, opacity=0.5)
        elif i == 5:
            cell.add_border(color=colors.primary, width=2)
        cell.add_text(labels_color[i], at="bottom", font_size=0.20, color="#aaaacc", baseline="auto", fit=True)

    # Row 1: entities that use fill=
    labels_fill = ["Rect", "Ellipse", "Polygon", "  ", "  ", "  "]
    for i, cell in enumerate(scene.grid.row(1)):
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
        if i == 0:
            cell.add_rect(at="center", width=0.68, height=0.55, fill=colors.accent)
        elif i == 1:
            cell.add_ellipse(at="center", rx=0.36, ry=0.27, fill=colors.accent)
        elif i == 2:
            cell.add_polygon(Polygon.hexagon(size=0.6), fill=colors.accent)
        cell.add_text(labels_fill[i], at="bottom", font_size=0.20, color="#aaaacc", baseline="auto", fit=True)
    save(scene, "guide/styles-fill-vs-color.svg")

    # --- 4. Style reuse example ---
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=12, rows=8, cell_size=22, background=colors.background)

    # Define reusable styles
    dot_small = DotStyle(color=colors.primary, opacity=0.6)
    dot_large = DotStyle(color=colors.accent, opacity=0.9)
    line_thin = LineStyle(width=1, color=colors.line, opacity=0.4)
    shape_hex = ShapeStyle(color=colors.secondary, opacity=0.5)

    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        # Apply different styles based on position
        if t < 0.33:
            cell.add_dot(radius=0.15, style=dot_small)
            cell.add_line(start="top_left", end="bottom_right", style=line_thin)
        elif t < 0.66:
            cell.add_polygon(Polygon.hexagon(size=0.5), style=shape_hex)
        else:
            cell.add_dot(radius=0.30, style=dot_large)
    save(scene, "guide/styles-reuse.svg")

    # --- 5. fill_opacity vs stroke_opacity ---
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=60, background=colors.background)
    opacities = [0.2, 0.4, 0.6, 0.8, 1.0]
    for i, cell in enumerate(scene.grid):
        op = opacities[i]
        cell.add_ellipse(
            at="center",
            rx=0.37, ry=0.37,
            fill=colors.primary,
            stroke=colors.accent,
            stroke_width=3,
            fill_opacity=op,
            stroke_opacity=1.0,
        )
        cell.add_text(
            f"{op:.1f}",
            at="bottom",
            font_size=0.15,
            color="#aaaacc",
            baseline="auto",
        )
    save(scene, "guide/styles-fill-stroke-opacity.svg")
