"""Generate SVGs for Guide: Paths and Parametric Positioning."""

import math

from pyfreeform import Scene, Palette, Polygon

from wiki._generator import save, sample_image


def generate():
    colors = Palette.midnight()

    # --- 1. Dot sliding along a diagonal (brightness-driven t) ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=25,
        cell_size=16,
    )
    for cell in scene.grid:
        diag = cell.add_diagonal(
            width=0.5,
            color=colors.line,
            opacity=0.3,
        )
        cell.add_dot(
            along=diag,
            t=cell.brightness,
            radius=0.15 + cell.brightness * 0.25,
            color=cell.color,
        )
    save(scene, "guide/paths-along-diagonal.svg")

    # --- 2. Dots along a curve ---
    colors_ocean = Palette.ocean()
    scene = Scene.with_grid(cols=14, rows=10, cell_size=22, background=colors_ocean.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.6,
            width=0.5,
            color=colors_ocean.line,
            opacity=0.2,
        )
        # Place 3 dots along the curve
        for t_val in [0.25, 0.5, 0.75]:
            r = 0.05 + (nx + t_val) * 0.10
            cell.add_dot(
                along=curve,
                t=t_val,
                radius=r,
                color=colors_ocean.primary,
                opacity=0.5 + ny * 0.5,
            )
    save(scene, "guide/paths-along-curve.svg")

    # --- 3. Dots orbiting along ellipses ---
    colors_sunset = Palette.sunset()
    scene = Scene.with_grid(cols=10, rows=10, cell_size=28, background=colors_sunset.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        ellipse = cell.add_ellipse(
            at="center",
            rx=0.4,
            ry=0.25,
            rotation=nx * 60,
            fill="none",
            stroke=colors_sunset.line,
            stroke_width=0.5,
            opacity=0.3,
        )
        # Place dot at position driven by ny
        cell.add_dot(
            along=ellipse,
            t=ny,
            radius=0.10,
            color=colors_sunset.accent,
            opacity=0.8,
        )
    save(scene, "guide/paths-along-ellipse.svg")

    # --- 4. Multiple t-values visualized on one path ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=280, background=colors.background)
    cell = scene.grid[0, 0]
    curve = cell.add_curve(
        start=(0.1, 0.8),
        end=(0.9, 0.2),
        curvature=0.7,
        width=2,
        color=colors.line,
        opacity=0.5,
    )
    # Show dots at t = 0, 0.25, 0.5, 0.75, 1.0
    t_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    for t_val in t_values:
        cell.add_dot(
            along=curve,
            t=t_val,
            radius=0.05,
            color=colors.primary,
            opacity=0.8,
        )
        pt = curve.point_at(t_val)
        cell.add_text(
            f"t={t_val:.2f}",
            at=((pt.x - cell.x) / cell.width, (pt.y - cell.y) / cell.height + 0.06),
            font_size=0.04,
            color="#aaaacc",
        )
    save(scene, "guide/paths-t-values.svg")

    # --- 5. Custom pathable: Wave (using built-in Path.Wave) ---
    from pyfreeform import Path

    colors_neon = Palette.neon()
    scene = Scene.with_grid(cols=10, rows=8, cell_size=30, background=colors_neon.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        cx, cy = cell.center
        w, h = cell.width, cell.height
        wave = Path.Wave(
            start=(cx - w * 0.4, cy),
            end=(cx + w * 0.4, cy),
            amplitude=h * 0.3,
            frequency=1 + nx * 3,
        )
        cell.add_path(
            wave,
            segments=32,
            width=1 + ny * 2,
            color=colors_neon.primary,
            opacity=0.5 + nx * 0.5,
        )
    save(scene, "guide/paths-custom-wave.svg")

    # --- 6. Sub-paths / arcs (start_t / end_t) ---
    colors_forest = Palette.forest()
    scene = Scene.with_grid(cols=8, rows=8, cell_size=32, background=colors_forest.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        ellipse = cell.add_ellipse(
            at="center",
            rx=0.4,
            ry=0.4,
            fill="none",
            stroke=colors_forest.grid,
            stroke_width=0.3,
            opacity=0.2,
        )
        # Render only a portion of the ellipse as a path
        start_t = nx * 0.5
        end_t = start_t + 0.3 + ny * 0.3
        cell.add_path(
            ellipse,
            start_t=start_t,
            end_t=min(end_t, 1.0),
            segments=24,
            width=2,
            color=colors_forest.primary,
            opacity=0.6 + ny * 0.4,
        )
    save(scene, "guide/paths-arcs.svg")

    # --- 7. TextPath: text along a curve ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=280, background=colors.background)
    cell = scene.grid[0, 0]
    curve = cell.add_curve(
        start=(0.05, 0.7),
        end=(0.95, 0.3),
        curvature=0.5,
        width=1,
        color=colors.line,
        opacity=0.3,
    )
    cell.add_text(
        "Text flows along any path in PyFreeform",
        along=curve,
        font_size=0.05,
        color=colors.accent,
    )
    save(scene, "guide/paths-textpath.svg")

    # --- 8. Filled Lissajous curves ---
    scene = Scene(400, 400, background="#0a0a1a")
    cx, cy = 200, 200
    curves = [
        (3, 2, math.pi / 2, 150, "#4a90d9", "#6ab0ff", 0.25),
        (5, 4, math.pi / 3, 130, "#d94a6b", "#ff6a8b", 0.20),
        (3, 4, math.pi / 4, 110, "#4ad9a7", "#6affcf", 0.30),
    ]
    for a, b, delta, size, fill, stroke, opacity in curves:
        liss = Path.Lissajous(center=(cx, cy), a=a, b=b, delta=delta, size=size)
        path = Path(
            liss,
            closed=True,
            fill=fill,
            color=stroke,
            width=1.2,
            fill_opacity=opacity,
            stroke_opacity=0.7,
            segments=128,
        )
        scene.place(path)
    save(scene, "guide/paths-filled-lissajous.svg")

    # --- 9. align=True: entity rotated to follow path ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=280, background=colors.background)
    cell = scene.grid[0, 0]
    curve = cell.add_curve(
        start=(0.1, 0.8),
        end=(0.9, 0.2),
        curvature=0.6,
        width=1.5,
        color=colors.line,
        opacity=0.4,
    )
    for t_val in [i / 10.0 for i in range(11)]:
        cell.add_polygon(
            Polygon.triangle(size=0.06),
            along=curve,
            t=t_val,
            align=True,
            fill=colors.primary,
            opacity=0.6 + t_val * 0.4,
        )
    save(scene, "guide/paths-align.svg")
