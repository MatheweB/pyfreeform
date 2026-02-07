#!/usr/bin/env python3
"""
SVG Generator for: examples/intermediate/connections

Demonstrates network visualization with distance-based connections.
"""

import math
from pyfreeform import Scene, Palette, Dot, Line, Connection
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "connections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_network():
    """Network of dots connected by proximity."""
    colors = Palette.midnight()
    grid_size = 30
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=15, background=colors.background
    )

    # Collect bright cells and their dots
    dot_entries = []
    for cell in scene.grid:
        center = grid_size / 2
        distance = math.sqrt((cell.col - center) ** 2 + (cell.row - center) ** 2)
        brightness = (math.sin(distance * 0.5) + 1) / 2

        if brightness > 0.4:
            radius = 2 + brightness * 3
            dot = cell.add_dot(color=colors.secondary, radius=radius, z_index=1)
            dot_entries.append((dot, cell.row, cell.col))

    # Connect nearby dots
    max_distance = 3
    for i, (dot1, r1, c1) in enumerate(dot_entries):
        for dot2, r2, c2 in dot_entries[i + 1 : i + 4]:
            dr, dc = r1 - r2, c1 - c2
            dist = math.sqrt(dr * dr + dc * dc)
            if dist <= max_distance:
                opacity = (1 - dist / max_distance) * 0.5
                conn = Connection(
                    dot1, dot2,
                    start_anchor="center", end_anchor="center",
                    style={"width": 0.5, "color": colors.primary, "opacity": opacity},
                )
                scene.add(conn)

    scene.save(OUTPUT_DIR / "01_network.svg")


def example_02_distance_fade():
    """Connections fade with distance — radial brightness pattern."""
    colors = Palette.ocean()
    grid_size = 25
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=15, background=colors.background
    )

    center = grid_size / 2
    max_dist = math.sqrt(center**2 + center**2)
    dot_entries = []

    for cell in scene.grid:
        dist = math.sqrt((cell.col - center) ** 2 + (cell.row - center) ** 2)
        brightness = 1 - (dist / max_dist)

        if brightness > 0.4:
            dot = cell.add_dot(
                color=colors.primary, radius=2 + brightness * 4, z_index=1
            )
            dot_entries.append((dot, cell.row, cell.col))

    for i, (dot1, r1, c1) in enumerate(dot_entries):
        for dot2, r2, c2 in dot_entries[i + 1 : i + 3]:
            dr, dc = r1 - r2, c1 - c2
            dist = math.sqrt(dr * dr + dc * dc)
            if dist < 4:
                opacity = (1 - dist / 4) * 0.4
                conn = Connection(
                    dot1, dot2,
                    start_anchor="center", end_anchor="center",
                    style={"width": 0.5, "color": colors.line, "opacity": opacity},
                )
                scene.add(conn)

    scene.save(OUTPUT_DIR / "02_distance_fade.svg")


def example_03_hub_spoke():
    """Hub-and-spoke pattern: center dot connects to ring dots."""
    colors = Palette.midnight()
    scene = Scene(width=300, height=300, background=colors.background)

    # Center hub
    hub = Dot(150, 150, radius=10, color=colors.accent)
    scene.add(hub)

    # Spoke dots in a ring
    spoke_dots = []
    for i in range(12):
        angle = i * (2 * math.pi / 12)
        x = 150 + 100 * math.cos(angle)
        y = 150 + 100 * math.sin(angle)
        dot = Dot(x, y, radius=5, color=colors.primary)
        scene.add(dot)
        spoke_dots.append(dot)

    # Connect hub to each spoke
    for dot in spoke_dots:
        conn = Connection(
            hub, dot,
            start_anchor="center", end_anchor="center",
            style={"width": 1, "color": colors.line, "opacity": 0.5},
        )
        scene.add(conn)

    scene.save(OUTPUT_DIR / "03_hub_spoke.svg")


GENERATORS = {
    "01_network": example_01_network,
    "02_distance_fade": example_02_distance_fade,
    "03_hub_spoke": example_03_hub_spoke,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for connections examples...")

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
