"""
Entity Groups SVG generator.

Generates reference images for the EntityGroup entity page.
"""

import math
from pathlib import Path

from pyfreeform import Scene, Palette, EntityGroup, Dot, Line

OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "08-entity-groups"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SHARED FACTORIES
# =============================================================================

def make_flower(color="coral", petal_color="gold", petal_count=8, petal_radius=6, center_radius=10, ring_radius=15):
    """Create a flower EntityGroup."""
    g = EntityGroup()
    g.add(Dot(0, 0, radius=center_radius, color=color))
    for i in range(petal_count):
        angle = i * (2 * math.pi / petal_count)
        g.add(Dot(
            ring_radius * math.cos(angle),
            ring_radius * math.sin(angle),
            radius=petal_radius, color=petal_color,
        ))
    return g


def make_crosshair(size=15, color="white", dot_radius=3):
    """Create a crosshair EntityGroup."""
    g = EntityGroup()
    g.add(Line(-size, 0, size, 0, width=1, color=color, opacity=0.5))
    g.add(Line(0, -size, 0, size, width=1, color=color, opacity=0.5))
    g.add(Dot(0, 0, radius=dot_radius, color=color))
    return g


# =============================================================================
# 01 — What is an EntityGroup (hero image)
# =============================================================================

def generate_01_what_is():
    """Show a flower EntityGroup placed at three positions."""
    scene = Scene(350, 180)
    scene.background = "#1a1a2e"

    positions = [(80, 90), (175, 90), (270, 90)]
    colors = [("#ff6b6b", "#4ecdc4"), ("#4ecdc4", "#ffe66d"), ("#ffe66d", "#ff6b6b")]
    counts = [6, 8, 10]

    for (x, y), (c, pc), count in zip(positions, colors, counts):
        flower = make_flower(color=c, petal_color=pc, petal_count=count)
        scene.add(flower.move_to(x, y))

    scene.save(str(OUTPUT_DIR / "01_what_is.svg"))


# =============================================================================
# 02 — Creating an EntityGroup (step by step)
# =============================================================================

def generate_02_creating():
    """Show group construction: center dot + petals."""
    scene = Scene(400, 180)
    scene.background = "#2d1b4e"

    # Step 1: Just the center dot
    center_only = EntityGroup()
    center_only.add(Dot(0, 0, radius=10, color="#ff6b35"))
    scene.add(center_only.move_to(70, 90))

    # Step 2: Center + 4 petals
    partial = EntityGroup()
    partial.add(Dot(0, 0, radius=10, color="#ff6b35"))
    for i in range(4):
        angle = i * (2 * math.pi / 4)
        partial.add(Dot(15 * math.cos(angle), 15 * math.sin(angle), radius=6, color="#f7c59f"))
    scene.add(partial.move_to(200, 90))

    # Step 3: Complete flower
    full = make_flower(color="#ff6b35", petal_color="#f7c59f", petal_count=8)
    scene.add(full.move_to(330, 90))

    # Labels
    from pyfreeform import Text
    scene.add(Text(70, 160, "1. Center", font_size=11, color="#aaa"))
    scene.add(Text(200, 160, "2. Add petals", font_size=11, color="#aaa"))
    scene.add(Text(330, 160, "3. Complete", font_size=11, color="#aaa"))

    scene.save(str(OUTPUT_DIR / "02_creating.svg"))


# =============================================================================
# 03 — Placement methods
# =============================================================================

def generate_03_placement():
    """Show scene.add, cell.place, cell.add_entity."""
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=6, rows=3, cell_size=50)
    scene.background = colors.background

    for cell in scene.grid:
        flower = make_flower(
            color=colors.primary,
            petal_color=colors.accent,
            petal_count=6,
        )
        cell.place(flower)
        flower.fit_to_cell(0.7)

    scene.save(str(OUTPUT_DIR / "03_placement.svg"))


# =============================================================================
# 04 — fit_to_cell with varying fractions
# =============================================================================

def generate_04_fit_to_cell():
    """Show fit_to_cell at different scale fractions."""
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=70)
    scene.background = colors.background

    fractions = [0.3, 0.5, 0.7, 0.85, 1.0]
    for cell in scene.grid:
        frac = fractions[cell.col]
        flower = make_flower(color=colors.primary, petal_color=colors.accent, petal_count=8)
        cell.place(flower)
        flower.fit_to_cell(frac)

    scene.save(str(OUTPUT_DIR / "04_fit_to_cell.svg"))


# =============================================================================
# 05 — Complete example (grid with varied groups)
# =============================================================================

def generate_05_complete():
    """Grid stamps with data-driven variation."""
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=8, rows=5, cell_size=45)
    scene.background = colors.background

    for cell in scene.grid:
        petal_count = 4 + (cell.col % 4) * 2  # 4, 6, 8, 10
        flower = make_flower(
            color=colors.primary,
            petal_color=colors.accent,
            petal_count=petal_count,
        )
        cell.place(flower)
        flower.fit_to_cell(0.75)

    scene.save(str(OUTPUT_DIR / "05_complete.svg"))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    generate_01_what_is()
    generate_02_creating()
    generate_03_placement()
    generate_04_fit_to_cell()
    generate_05_complete()
    print(f"Generated EntityGroup entity images in {OUTPUT_DIR}")
