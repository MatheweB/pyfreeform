"""Generate SVGs for Recipe: Typographic Art."""

import math

from pyfreeform import Scene, Palette, Polygon

from wiki._generator import save, sample_image


def generate():
    # --- 1. ASCII art from image ---
    chars = " .:-=+*#%@"
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=50,
        cell_size=8,
    )
    for cell in scene.grid:
        idx = int(cell.brightness * (len(chars) - 1))
        char = chars[idx]
        if char != " ":
            cell.add_text(
                char,
                at="center",
                font_size=7,
                color="#ffffff",
                font_family="monospace",
                opacity=0.6 + cell.brightness * 0.4,
            )
    save(scene, "recipes/typo-ascii.svg")

    # --- 2. Text along curves ---
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=1, rows=1, cell_size=340, background=colors.background)
    cell = scene.grid[0, 0]
    phrases = [
        ("Create beautiful art with code", 0.4),
        ("PyFreeform makes it elegant", -0.5),
        ("Every cell tells a story", 0.6),
    ]
    for i, (text, curv) in enumerate(phrases):
        y_start = 0.2 + i * 0.25
        y_end = y_start + 0.05 * (1 if curv > 0 else -1)
        curve = cell.add_curve(
            start=(0.05, y_start), end=(0.95, y_end),
            curvature=curv,
            width=0.5, color=colors.line, opacity=0.15,
        )
        cell.add_text(
            text,
            along=curve,
            font_size=14,
            color=[colors.primary, colors.accent, colors.secondary][i],
        )
    save(scene, "recipes/typo-along-curves.svg")

    # --- 3. Letter mosaic from image ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=25,
        cell_size=16,
    )
    word = "MONSTER"
    for i, cell in enumerate(scene.grid):
        char = word[i % len(word)]
        size = 8 + cell.brightness * 8
        cell.add_text(
            char,
            at="center",
            font_size=size,
            color=cell.color,
            bold=True,
            opacity=0.5 + cell.brightness * 0.5,
        )
    save(scene, "recipes/typo-letter-mosaic.svg")

    # --- 4. Combined: dot art with text overlay ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=35,
        cell_size=12,
    )
    for cell in scene.grid:
        r = cell.brightness * scene.grid.cell_width * 0.4
        if r > 0.3:
            cell.add_dot(radius=r, color=cell.color, opacity=0.6)

    # Title overlay
    title = scene.grid.merge((0, 0), (2, scene.grid.cols - 1))
    title.add_fill(color="#000000", opacity=0.6)
    title.add_text(
        "MONA LISA",
        at="center",
        font_size=18,
        color="#ffffff",
        bold=True,
    )

    # Subtitle
    sub = scene.grid.merge((scene.grid.rows - 2, 0), (scene.grid.rows - 1, scene.grid.cols - 1))
    sub.add_fill(color="#000000", opacity=0.4)
    sub.add_text(
        "Leonardo da Vinci",
        at="center",
        font_size=11,
        color="#cccccc",
        italic=True,
    )
    save(scene, "recipes/typo-combined.svg")
