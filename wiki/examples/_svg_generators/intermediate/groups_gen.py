#!/usr/bin/env python3
"""
SVG Generator for: examples/intermediate/groups

Demonstrates EntityGroup — reusable composite shapes that behave
like normal entities.
"""

import math
from pathlib import Path

from pyfreeform import Scene, Palette, EntityGroup, Dot, Line


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "groups"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# REUSABLE SHAPE FACTORIES
# =============================================================================

def make_flower(color="coral", petal_color="gold", petal_count=8):
    """Create a flower EntityGroup."""
    g = EntityGroup()
    g.add(Dot(0, 0, radius=10, color=color, opacity=0.9))
    for i in range(petal_count):
        angle = i * (2 * math.pi / petal_count)
        x = 15 * math.cos(angle)
        y = 15 * math.sin(angle)
        g.add(Dot(x, y, radius=6, color=petal_color, opacity=0.8))
    return g


def make_star_burst(count=12, radius=20, color="white"):
    """Create a radial burst of dots."""
    g = EntityGroup()
    g.add(Dot(0, 0, radius=3, color=color))
    for i in range(count):
        angle = i * (2 * math.pi / count)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        g.add(Dot(x, y, radius=2, color=color, opacity=0.6))
    return g


def make_ring(radius=20, count=8, dot_radius=3, color="teal"):
    """Create a ring of dots."""
    g = EntityGroup()
    for i in range(count):
        angle = i * (2 * math.pi / count)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        g.add(Dot(x, y, radius=dot_radius, color=color))
    return g


def make_crosshair(size=15, color="white", width=1):
    """Create a crosshair marker."""
    g = EntityGroup()
    g.add(Line(-size, 0, size, 0, width=width, color=color, opacity=0.5))
    g.add(Line(0, -size, 0, size, width=width, color=color, opacity=0.5))
    g.add(Dot(0, 0, radius=3, color=color))
    return g


# =============================================================================
# SVG GENERATORS
# =============================================================================

def example_01_flower_pattern():
    """Defining and placing a reusable EntityGroup at multiple positions."""
    colors = Palette.midnight()
    scene = Scene(width=350, height=250, background=colors.background)

    # Place the same shape at different positions with different styles
    f1 = make_flower(color=colors.primary, petal_color=colors.secondary)
    scene.add(f1.move_to(80, 80))

    f2 = make_flower(color=colors.secondary, petal_color=colors.accent)
    scene.add(f2.move_to(260, 80))

    f3 = make_flower(
        color=colors.accent, petal_color=colors.primary, petal_count=12
    )
    scene.add(f3.move_to(170, 180))

    scene.save(OUTPUT_DIR / "01_flower_pattern.svg")


def example_02_shape_library():
    """Multiple shape factory functions composed together."""
    colors = Palette.ocean()
    scene = Scene(width=400, height=280, background=colors.background)

    # Flowers in a row
    for i, color in enumerate([colors.primary, colors.secondary, colors.accent]):
        f = make_flower(color=color, petal_color=colors.line)
        scene.add(f.move_to(80 + i * 120, 70))

    # Star bursts below
    for i in range(4):
        sb = make_star_burst(count=8 + i * 4, radius=15 + i * 5, color=colors.accent)
        scene.add(sb.move_to(60 + i * 100, 170))

    # Rings at bottom
    for i in range(3):
        r = make_ring(
            radius=12, count=6, dot_radius=2,
            color=[colors.primary, colors.secondary, colors.accent][i],
        )
        scene.add(r.move_to(100 + i * 100, 240))

    scene.save(OUTPUT_DIR / "02_shape_library.svg")


def example_03_grid_stamps():
    """Stamp EntityGroups across grid cells with fit_to_cell."""
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=8, rows=6, cell_size=40)
    scene.background = colors.background
    grid = scene.grid

    accent_colors = [colors.primary, colors.secondary, colors.accent]

    for cell in grid:
        # Pick shape based on position
        idx = (cell.row + cell.col) % 3

        if idx == 0:
            shape = make_flower(
                color=accent_colors[0],
                petal_color=accent_colors[1],
                petal_count=6,
            )
        elif idx == 1:
            shape = make_ring(
                radius=15, count=6, dot_radius=2,
                color=accent_colors[idx],
            )
        else:
            shape = make_star_burst(
                count=8, radius=12, color=accent_colors[idx],
            )

        # Place and auto-fit to cell
        cell.place(shape)
        shape.fit_to_cell(0.75)

    scene.save(OUTPUT_DIR / "03_grid_stamps.svg")


def example_04_nested_groups():
    """EntityGroup containing other EntityGroups."""
    colors = Palette.sunset()
    scene = Scene(width=400, height=300, background=colors.background)

    # Build a "bouquet" from smaller flower groups
    def make_bouquet(center_color, petal_colors):
        bouquet = EntityGroup()

        # Center flower
        center = make_flower(color=center_color, petal_color=petal_colors[0])
        bouquet.add(center)

        # Surrounding flowers (smaller, offset)
        for i in range(5):
            angle = i * (2 * math.pi / 5)
            outer = make_flower(
                color=petal_colors[i % len(petal_colors)],
                petal_color=center_color,
                petal_count=6,
            )
            outer.scale(0.6)
            outer.move_to(45 * math.cos(angle), 45 * math.sin(angle))
            bouquet.add(outer)

        return bouquet

    # Place bouquets
    b1 = make_bouquet(
        colors.primary,
        [colors.secondary, colors.accent, "#64ffda"],
    )
    scene.add(b1.move_to(130, 150))

    b2 = make_bouquet(
        colors.accent,
        [colors.primary, colors.secondary, "#ff9f43"],
    )
    b2.scale(0.7)
    scene.add(b2.move_to(310, 130))

    scene.save(OUTPUT_DIR / "04_nested_groups.svg")


GENERATORS = {
    "01_flower_pattern": example_01_flower_pattern,
    "02_shape_library": example_02_shape_library,
    "03_grid_stamps": example_03_grid_stamps,
    "04_nested_groups": example_04_nested_groups,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for groups examples...")

    for name, func in GENERATORS.items():
        try:
            func()
            print(f"  ✓ {name}.svg")
        except Exception as e:
            print(f"  ✗ {name}.svg - ERROR: {e}")

    print(f"Complete! Generated to {OUTPUT_DIR}/")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        generate_all()
