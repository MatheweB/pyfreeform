"""Generate SVGs for Guide: Text and Typography."""

from pyfreeform import Scene, Palette

from wiki._generator import save, sample_image


def generate():
    colors = Palette.midnight()

    # --- 1. Character grid from image ---
    chars = " .:-=+*#%@"
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=40,
        cell_size=10,
    )
    for cell in scene.grid:
        idx = int(cell.brightness * (len(chars) - 1))
        char = chars[idx]
        if char != " ":
            cell.add_text(
                char,
                at="center",
                font_size=0.90,
                color=cell.color,
                font_family="monospace",
            )
    save(scene, "guide/text-ascii-portrait.svg")

    # --- 2. Font families showcase ---
    families = ["sans-serif", "serif", "monospace"]
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120, background=colors.background)
    for i, cell in enumerate(scene.grid):
        family = families[i]
        cell.add_text(
            "PyFreeform",
            at=(0.5, 0.35),
            font_size=0.10,
            color=colors.primary,
            font_family=family,
        )
        cell.add_text(
            family,
            at=(0.5, 0.65),
            font_size=0.10,
            color="#aaaacc",
        )
        cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    save(scene, "guide/text-font-families.svg")

    # --- 3. Bold and italic ---
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background=colors.background)
    variants = [
        ("Normal", False, False),
        ("Bold", True, False),
        ("Italic", False, True),
        ("Both", True, True),
    ]
    for i, cell in enumerate(scene.grid):
        label, bold, italic = variants[i]
        cell.add_text(
            "Art",
            at=(0.5, 0.35),
            font_size=0.25,
            color=colors.primary,
            bold=bold,
            italic=italic,
        )
        cell.add_text(
            label,
            at=(0.5, 0.7),
            font_size=0.10,
            color="#aaaacc",
        )
        cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    save(scene, "guide/text-bold-italic.svg")

    # --- 4. Text along curve ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300, background=colors.background)
    cell = scene.grid[0, 0]
    curve = cell.add_curve(
        start=(0.05, 0.7),
        end=(0.95, 0.3),
        curvature=0.5,
        width=1,
        color=colors.line,
        opacity=0.2,
    )
    cell.add_text(
        "Text warps along curves beautifully",
        along=curve,
        font_size=0.05,
        color=colors.accent,
    )
    save(scene, "guide/text-along-curve.svg")

    # --- 5. Text along ellipse ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=260, background=colors.background)
    cell = scene.grid[0, 0]
    ellipse = cell.add_ellipse(
        at="center",
        rx=0.38,
        ry=0.23,
        fill="none",
        stroke=colors.line,
        stroke_width=0.5,
        opacity=0.2,
    )
    cell.add_text(
        "Text flows around an ellipse path",
        along=ellipse,
        font_size=0.05,
        color=colors.primary,
    )
    save(scene, "guide/text-along-ellipse.svg")

    # --- 6. Rotating text ---
    colors_sunset = Palette.sunset()
    scene = Scene.with_grid(cols=8, rows=6, cell_size=30, background=colors_sunset.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        rotation = (nx + ny) * 90
        cell.add_text(
            "AB",
            at="center",
            font_size=0.40,
            color=colors_sunset.primary,
            rotation=rotation,
            opacity=0.4 + nx * 0.6,
        )
    save(scene, "guide/text-rotation.svg")

    # --- 7. Title on merged CellGroup ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=30,
        cell_size=12,
    )
    for cell in scene.grid:
        r = cell.brightness * 0.45
        if r > 0.025:
            cell.add_dot(radius=r, color=cell.color, opacity=0.7)
    # Merge bottom 2 rows for title overlay
    title = scene.grid.merge(
        (scene.grid.num_rows - 3, 0),
        (scene.grid.num_rows - 1, scene.grid.num_columns - 1),
    )
    title.add_fill(color="#000000", opacity=0.5)
    title.add_text(
        "FRANK",
        at="center",
        font_size=0.55,
        color="#ffffff",
        bold=True,
    )
    save(scene, "guide/text-title-overlay.svg")
