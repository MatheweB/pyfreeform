#!/usr/bin/env python3
"""
SVG Generator for: api-reference/scene.md

Generates visual examples demonstrating Scene API methods and properties.
"""

from pyfreeform import Scene, Palette, Dot, Line, Connection, CellGroup
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "scene"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_scene_test.png"

    img = Image.new('RGB', (400, 300))
    draw = ImageDraw.Draw(img)

    # Simple gradient
    for y in range(300):
        for x in range(400):
            t = x / 400
            r = int(100 + t * 100)
            g = int(150 + t * 50)
            b = int(200 - t * 50)
            draw.point((x, y), fill=(r, g, b))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_image()


# =============================================================================
# Constructor Example
# =============================================================================

def example1_constructor():
    """Scene(width, height, background) - Basic constructor with builder methods"""
    scene = Scene(width=400, height=300, background="#1a1a2e")

    # Scene is a Surface — use builder methods directly!
    scene.add_line(start=(0.25, 0.33), end=(0.75, 0.67), color="#ffd23f", width=2)
    scene.add_dot(at=(0.25, 0.33), radius=15, color="#4ecca3", z_index=1)
    scene.add_dot(at=(0.75, 0.67), radius=15, color="#ee4266", z_index=1)

    scene.save(OUTPUT_DIR / "example1-constructor.svg")


# =============================================================================
# Factory Method: from_image
# =============================================================================

def example2_from_image():
    """Scene.from_image() - Load image with grid"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Show grid structure
    for cell in scene.grid:
        cell.add_border(color="#ffffff", width=0.5)

        # Add dots based on brightness
        if cell.brightness > 0.5:
            cell.add_dot(color=cell.color, radius=3)

    scene.save(OUTPUT_DIR / "example2-from-image.svg")


# =============================================================================
# Factory Method: with_grid
# =============================================================================

def example3_with_grid():
    """Scene.with_grid() - Create scene with empty grid"""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=15, background="#1a1a2e")
    colors = Palette.ocean()

    # Simple pattern
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color=colors.primary, radius=5)

    scene.save(OUTPUT_DIR / "example3-with-grid.svg")


# =============================================================================
# Properties: Scene dimensions and background
# =============================================================================

def example4_properties():
    """Scene properties - width, height, background — using scene builders"""
    scene = Scene(width=500, height=400, background="#f0f9ff")

    # Scene builder methods — no manual coordinate math!
    scene.add_border(color="#3b82f6", width=2)
    scene.add_text(
        f"width = {scene.width}",
        at=(0.5, 0.07), font_size=16, color="#3b82f6"
    )
    scene.add_text(
        f"height = {scene.height}",
        at=(0.06, 0.5), font_size=16, color="#3b82f6", rotation=-90
    )

    scene.save(OUTPUT_DIR / "example4-properties.svg")


# =============================================================================
# Methods: add_entity
# =============================================================================

def example5_scene_builders():
    """Scene builder methods — same API as cells"""
    scene = Scene(width=400, height=300, background="#0f172a")

    # Scene-level curve with along= positioning
    curve = scene.add_curve(
        start="left", end="right",
        curvature=0.4, color="#334155", width=2
    )

    # Place dots along the curve — works at scene level!
    colors = ["#f43f5e", "#f97316", "#eab308", "#22c55e", "#3b82f6", "#8b5cf6"]
    for i, color in enumerate(colors):
        t = (i + 0.5) / len(colors)
        scene.add_dot(along=curve, t=t, radius=12, color=color, z_index=1)

    # Labels at named positions
    scene.add_text("scene.add_dot(along=curve, t=...)",
                   at=(0.5, 0.15), font_size=13, color="#94a3b8")

    scene.save(OUTPUT_DIR / "example5-scene-builders.svg")


# =============================================================================
# Methods: add_connection
# =============================================================================

def example6_add_connection():
    """scene.add_connection() - Add connections between entities"""
    scene = Scene(width=400, height=300, background="#1a1a2e")

    # Create dots
    dot1 = Dot(100, 100, radius=15, color="#ee4266")
    dot2 = Dot(300, 100, radius=15, color="#4ecca3")
    dot3 = Dot(200, 200, radius=15, color="#ffd23f")

    scene.add(dot1)
    scene.add(dot2)
    scene.add(dot3)

    # Create connections
    conn1 = Connection(dot1, dot2, "center", "center", style={"width": 2, "color": "#888888"})
    conn2 = Connection(dot2, dot3, "center", "center", style={"width": 2, "color": "#888888"})
    conn3 = Connection(dot1, dot3, "center", "center", style={"width": 2, "color": "#888888"})

    scene.add(conn1)
    scene.add(conn2)
    scene.add(conn3)

    scene.save(OUTPUT_DIR / "example6-add-connection.svg")


# =============================================================================
# Complete Example: Grid + Entities
# =============================================================================

def example7_complete():
    """Complete scene - Grid with scene-level overlay using builders"""
    scene = Scene.with_grid(cols=15, rows=10, cell_size=20, background="#1a1a2e")
    colors = Palette.midnight()

    # Grid-based elements
    for cell in scene.grid:
        cell.add_dot(color=colors.primary, radius=2)

    # Scene-level overlay — same builder API as cells!
    scene.add_text("Scene API Demo", at=(0.5, 0.12),
                   font_size=18, color=colors.accent)

    # Decorative scene-level curve
    curve = scene.add_curve(
        start="bottom_left", end="bottom_right",
        curvature=-0.3, color=colors.secondary, width=2
    )
    for i in range(5):
        scene.add_dot(along=curve, t=(i + 0.5) / 5,
                      radius=4, color=colors.accent, z_index=1)

    scene.save(OUTPUT_DIR / "example7-complete.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-constructor": example1_constructor,
    "example2-from-image": example2_from_image,
    "example3-with-grid": example3_with_grid,
    "example4-properties": example4_properties,
    "example5-scene-builders": example5_scene_builders,
    "example6-add-connection": example6_add_connection,
    "example7-complete": example7_complete,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for scene.md...")

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
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        generate_all()
