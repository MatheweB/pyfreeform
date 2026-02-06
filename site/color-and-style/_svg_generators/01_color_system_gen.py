#!/usr/bin/env python3
"""
SVG Generator for: color-and-style/01-color-system.md

Generates beautiful visual examples demonstrating different color formats.

Corresponds to sections:
- Named Colors
- Hex Colors
- RGB Tuples
- Color Class
"""

import math
from pathlib import Path
from pyfreeform import Scene, Color, Dot


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-color-system"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: Named Colors
# =============================================================================

def example_01_named_colors():
    """
    Demonstrate named colors: red, coral, dodgerblue
    Show dots in a beautiful arrangement
    """
    scene = Scene(width=600, height=200, background="#f8f9fa")

    # Create three columns of dots
    colors = [
        ("red", 100),
        ("coral", 300),
        ("dodgerblue", 500)
    ]

    for color_name, x in colors:
        # Large center dot
        scene.add(Dot(x=x, y=100, radius=40, color=color_name))

        # Smaller surrounding dots in a circle
        for i in range(8):
            angle = (i * math.pi * 2) / 8
            offset_x = math.cos(angle) * 60
            offset_y = math.sin(angle) * 60
            scene.add(Dot(
                x=x + offset_x,
                y=100 + offset_y,
                radius=12,
                color=color_name
            ))

    scene.save(OUTPUT_DIR / "01-named-colors.svg")


def example_02_named_colors_variety():
    """
    Show a variety of named colors in a grid
    """
    scene = Scene(width=700, height=300, background="#ffffff")

    named_colors = [
        "red", "coral", "tomato", "crimson",
        "orange", "gold", "yellow", "khaki",
        "lime", "green", "teal", "cyan",
        "dodgerblue", "blue", "navy", "purple",
        "magenta", "pink", "maroon", "brown"
    ]

    cols = 5
    x_spacing = 140
    y_spacing = 75

    for i, color_name in enumerate(named_colors):
        row = i // cols
        col = i % cols
        x = 70 + col * x_spacing
        y = 75 + row * y_spacing

        scene.add(Dot(x=x, y=y, radius=25, color=color_name))

    scene.save(OUTPUT_DIR / "02-named-colors-variety.svg")


# =============================================================================
# SECTION: Hex Colors
# =============================================================================

def example_03_hex_colors():
    """
    Demonstrate hex colors: #ff5733 and short form #f57
    """
    scene = Scene(width=500, height=200, background="#f8f9fa")

    # Long form hex color
    x1 = 150
    scene.add(Dot(x=x1, y=100, radius=50, color="#ff5733"))

    # Create a ring pattern with variations
    for i in range(8):
        angle = (i * math.pi * 2) / 8
        offset_x = math.cos(angle) * 70
        offset_y = math.sin(angle) * 70
        scene.add(Dot(
            x=x1 + offset_x,
            y=100 + offset_y,
            radius=10,
            color="#ff5733"
        ))

    # Short form hex color
    x2 = 350
    scene.add(Dot(x=x2, y=100, radius=50, color="#f57"))

    # Create a ring pattern with variations
    for i in range(8):
        angle = (i * math.pi * 2) / 8
        offset_x = math.cos(angle) * 70
        offset_y = math.sin(angle) * 70
        scene.add(Dot(
            x=x2 + offset_x,
            y=100 + offset_y,
            radius=10,
            color="#f57"
        ))

    scene.save(OUTPUT_DIR / "03-hex-colors.svg")


def example_04_hex_color_spectrum():
    """
    Create a beautiful color spectrum using hex colors
    """
    scene = Scene(width=800, height=200, background="#1a1a2e")

    # Rainbow spectrum
    hex_colors = [
        "#ff0000", "#ff4500", "#ff8c00", "#ffd700",
        "#ffff00", "#adff2f", "#00ff00", "#00fa9a",
        "#00ffff", "#1e90ff", "#0000ff", "#4b0082",
        "#8b00ff", "#ff00ff", "#ff1493", "#ff69b4"
    ]

    x_spacing = 50
    start_x = 25

    for i, color in enumerate(hex_colors):
        x = start_x + i * x_spacing
        scene.add(Dot(x=x, y=100, radius=20, color=color))

    scene.save(OUTPUT_DIR / "04-hex-color-spectrum.svg")


# =============================================================================
# SECTION: RGB Tuples
# =============================================================================

def example_05_rgb_tuples():
    """
    Demonstrate RGB tuple: (255, 87, 51)
    """
    scene = Scene(width=600, height=250, background="#f8f9fa")

    # Show the RGB color
    scene.add(Dot(x=300, y=125, radius=60, color=(255, 87, 51)))

    # Break down the components visually
    # Red component
    scene.add(Dot(x=100, y=125, radius=30, color=(255, 0, 0)))

    # Green component
    scene.add(Dot(x=500, y=125, radius=30, color=(0, 87, 0)))

    # Blue component (very small since it's only 51)
    scene.add(Dot(x=300, y=50, radius=15, color=(0, 0, 51)))

    scene.save(OUTPUT_DIR / "05-rgb-tuples.svg")


def example_06_rgb_gradient():
    """
    Create a smooth gradient using RGB tuples
    """
    scene = Scene(width=800, height=200, background="#ffffff")

    # Gradient from blue to orange
    steps = 20
    for i in range(steps):
        t = i / (steps - 1)

        # Interpolate between (30, 144, 255) and (255, 165, 0)
        r = int(30 + t * (255 - 30))
        g = int(144 + t * (165 - 144))
        b = int(255 + t * (0 - 255))

        x = 40 + i * 36
        scene.add(Dot(x=x, y=100, radius=25, color=(r, g, b)))

    scene.save(OUTPUT_DIR / "06-rgb-gradient.svg")


# =============================================================================
# SECTION: Color Class
# =============================================================================

def example_07_color_class():
    """
    Demonstrate the Color class with different input formats
    """
    scene = Scene(width=700, height=250, background="#f8f9fa")

    # Create colors using different formats
    colors = [
        (Color("red"), 120),
        (Color("#ff0000"), 300),
        (Color((255, 0, 0)), 480)
    ]

    for color_obj, x in colors:
        # All should produce the same red color
        scene.add(Dot(x=x, y=125, radius=45, color=color_obj.to_hex()))

        # Add smaller accent dots
        scene.add(Dot(x=x - 30, y=80, radius=15, color=color_obj.to_hex()))
        scene.add(Dot(x=x + 30, y=80, radius=15, color=color_obj.to_hex()))
        scene.add(Dot(x=x - 30, y=170, radius=15, color=color_obj.to_hex()))
        scene.add(Dot(x=x + 30, y=170, radius=15, color=color_obj.to_hex()))

    scene.save(OUTPUT_DIR / "07-color-class.svg")


def example_08_color_formats_comparison():
    """
    Side-by-side comparison of all color formats producing the same result
    """
    scene = Scene(width=800, height=350, background="#ffffff")

    # Three different representations of the same color
    representations = [
        ('Named: "dodgerblue"', "dodgerblue", 200),
        ('Hex: "#1e90ff"', "#1e90ff", 400),
        ('RGB: (30, 144, 255)', (30, 144, 255), 600)
    ]

    for _label, color, x in representations:
        # Large dot
        scene.add(Dot(x=x, y=175, radius=50, color=color))

        # Create a decorative pattern around it
        for ring in range(2):
            radius_offset = 70 + ring * 20
            num_dots = 6 + ring * 2
            dot_size = 10 - ring * 3

            for i in range(num_dots):
                angle = (i * math.pi * 2) / num_dots
                offset_x = math.cos(angle) * radius_offset
                offset_y = math.sin(angle) * radius_offset
                scene.add(Dot(
                    x=x + offset_x,
                    y=175 + offset_y,
                    radius=dot_size,
                    color=color
                ))

    scene.save(OUTPUT_DIR / "08-color-formats-comparison.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-named-colors": example_01_named_colors,
    "02-named-colors-variety": example_02_named_colors_variety,
    "03-hex-colors": example_03_hex_colors,
    "04-hex-color-spectrum": example_04_hex_color_spectrum,
    "05-rgb-tuples": example_05_rgb_tuples,
    "06-rgb-gradient": example_06_rgb_gradient,
    "07-color-class": example_07_color_class,
    "08-color-formats-comparison": example_08_color_formats_comparison,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-color-system.md...")

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
        # Generate specific image
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            print("Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        # Generate all
        generate_all()
