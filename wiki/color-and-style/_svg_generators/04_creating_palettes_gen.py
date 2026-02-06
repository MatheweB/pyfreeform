#!/usr/bin/env python3
"""
SVG Generator for: color-and-style/04-creating-palettes.md

Generates visual examples demonstrating custom palette creation.

Corresponds to sections:
- Custom Palette
- From Existing Palette
- Color Theory Tips
"""

from pyfreeform import Scene, Palette, Dot, Rect
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "04-creating-palettes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Create a test gradient image for consistent examples
def create_test_gradient() -> Path:
    """Create a simple gradient image for testing"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_gradient_custom.png"

    # Create 400x400 gradient (radial)
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Radial gradient from center
            center_x, center_y = 200, 200
            distance = ((x - center_x)**2 + (y - center_y)**2) ** 0.5
            max_distance = (200**2 + 200**2) ** 0.5

            # Interpolate from bright (center) to dark (edges)
            t = min(distance / max_distance, 1.0)
            brightness = int(255 * (1 - t))

            draw.point((x, y), fill=(brightness, brightness, brightness))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_gradient()


# =============================================================================
# SECTION: Custom Palette
# =============================================================================

def example_01_custom_palette_definition():
    """
    Show a custom palette definition with color swatches
    """
    scene = Scene(width=800, height=400, background="#f5f5f5")

    # Custom palette colors
    my_palette = Palette(
        background="#1a1a2e",
        primary="#16213e",
        secondary="#0f3460",
        accent="#e94560",
        line="#533483",
        grid="#2d2d44"
    )

    # Display swatches with labels
    swatches = [
        ("background", my_palette.background, 100),
        ("primary", my_palette.primary, 240),
        ("secondary", my_palette.secondary, 380),
        ("accent", my_palette.accent, 520),
        ("line", my_palette.line, 100),
        ("grid", my_palette.grid, 240),
    ]

    for i, (label, color, x) in enumerate(swatches):
        y = 100 if i < 4 else 250
        actual_x = x if i < 4 else x + 280

        # Color swatch
        scene.add(Rect(x=actual_x, y=y, width=100, height=100, fill=color, stroke="#333333", stroke_width=2))

    scene.save(OUTPUT_DIR / "01-custom-palette-definition.svg")


def example_02_custom_palette_usage():
    """
    Use the custom palette in an actual scene
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    my_palette = Palette(
        background="#1a1a2e",
        primary="#16213e",
        secondary="#0f3460",
        accent="#e94560",
        line="#533483",
        grid="#2d2d44"
    )

    scene.background = my_palette.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=my_palette.primary, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=my_palette.secondary, radius=4)
        else:
            cell.add_dot(color=my_palette.accent, radius=3)

    scene.save(OUTPUT_DIR / "02-custom-palette-usage.svg")


def example_03_custom_palette_artistic():
    """
    Create an artistic composition using the custom palette
    """
    scene = Scene(width=600, height=600, background="#1a1a2e")

    my_palette = Palette(
        background="#1a1a2e",
        primary="#16213e",
        secondary="#0f3460",
        accent="#e94560",
        line="#533483",
        grid="#2d2d44"
    )

    # Create concentric circles with palette colors
    center_x, center_y = 300, 300

    for ring in range(8):
        radius = 50 + ring * 30
        num_dots = 6 + ring * 4
        colors = [my_palette.accent, my_palette.primary, my_palette.secondary]
        color = colors[ring % 3]

        for i in range(num_dots):
            angle = (i * 2 * math.pi) / num_dots
            x_pos = center_x + math.cos(angle) * radius
            y_pos = center_y + math.sin(angle) * radius
            dot_size = 8 - ring * 0.5
            scene.add(Dot(x=x_pos, y=y_pos, radius=max(2, dot_size), color=color))

    scene.save(OUTPUT_DIR / "03-custom-palette-artistic.svg")


# =============================================================================
# SECTION: From Existing Palette
# =============================================================================

def example_04_existing_palette_base():
    """
    Show the base ocean palette before modification
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.ocean()

    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=4)
        else:
            cell.add_dot(color=colors.accent, radius=3)

    scene.save(OUTPUT_DIR / "04-existing-palette-base.svg")


def example_05_modified_palette():
    """
    Show the modified palette with custom red primary color
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Start with existing
    colors = Palette.ocean()

    # Modify
    custom = Palette(
        background=colors.background,
        primary="#ff0000",  # Custom red
        secondary=colors.secondary,
        accent=colors.accent,
        line=colors.line,
        grid=colors.grid
    )

    scene.background = custom.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=custom.primary, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=custom.secondary, radius=4)
        else:
            cell.add_dot(color=custom.accent, radius=3)

    scene.save(OUTPUT_DIR / "05-modified-palette.svg")


def example_06_palette_comparison():
    """
    Side-by-side comparison of original and modified
    """
    # Left: Original ocean palette
    scene = Scene(width=900, height=450, background="#f5f5f5")

    colors_ocean = Palette.ocean()
    custom = Palette(
        background=colors_ocean.background,
        primary="#ff0000",
        secondary=colors_ocean.secondary,
        accent=colors_ocean.accent,
        line=colors_ocean.line,
        grid=colors_ocean.grid
    )

    # Create pattern with original palette
    for i in range(5):
        for j in range(5):
            x = 80 + i * 70
            y = 80 + j * 70
            brightness = (i + j) / 9.0

            if brightness > 0.7:
                scene.add(Dot(x=x, y=y, radius=15, color=colors_ocean.primary))
            elif brightness > 0.4:
                scene.add(Dot(x=x, y=y, radius=12, color=colors_ocean.secondary))
            else:
                scene.add(Dot(x=x, y=y, radius=10, color=colors_ocean.accent))

    # Create pattern with modified palette
    for i in range(5):
        for j in range(5):
            x = 500 + i * 70
            y = 80 + j * 70
            brightness = (i + j) / 9.0

            if brightness > 0.7:
                scene.add(Dot(x=x, y=y, radius=15, color=custom.primary))
            elif brightness > 0.4:
                scene.add(Dot(x=x, y=y, radius=12, color=custom.secondary))
            else:
                scene.add(Dot(x=x, y=y, radius=10, color=custom.accent))

    scene.save(OUTPUT_DIR / "06-palette-comparison.svg")


# =============================================================================
# SECTION: Color Theory Tips
# =============================================================================

def example_07_complementary_colors():
    """
    Demonstrate complementary colors (opposite on color wheel)
    Blue and orange example
    """
    scene = Scene(width=700, height=350, background="#f8f9fa")

    # Blue and orange are complementary
    blue = "#1e90ff"
    orange = "#ff8c00"

    # Create alternating pattern
    for i in range(12):
        x = 80 + i * 50
        color = blue if i % 2 == 0 else orange

        # Create vertical column
        for j in range(5):
            y = 75 + j * 50
            scene.add(Dot(x=x, y=y, radius=18, color=color))

    scene.save(OUTPUT_DIR / "07-complementary-colors.svg")


def example_08_analogous_colors():
    """
    Demonstrate analogous colors (adjacent colors)
    Blue, cyan, teal example
    """
    scene = Scene(width=700, height=350, background="#f8f9fa")

    # Analogous colors
    colors = ["#0000ff", "#00bfff", "#008b8b"]  # Blue, cyan, teal

    # Create gradient pattern
    for i in range(15):
        x = 60 + i * 42
        color_idx = (i // 5) % 3

        for j in range(5):
            y = 75 + j * 50
            scene.add(Dot(x=x, y=y, radius=16, color=colors[color_idx]))

    scene.save(OUTPUT_DIR / "08-analogous-colors.svg")


def example_09_triadic_colors():
    """
    Demonstrate triadic colors (evenly spaced)
    Red, yellow, blue example
    """
    scene = Scene(width=700, height=350, background="#f8f9fa")

    # Triadic colors
    red = "#ff0000"
    yellow = "#ffff00"
    blue = "#0000ff"
    colors = [red, yellow, blue]

    # Create triangular pattern
    center_x, center_y = 350, 175

    for ring in range(5):
        radius = 40 + ring * 30
        num_dots = 3  # Always 3 for triadic

        for i in range(num_dots):
            angle = (i * 2 * math.pi / 3) - math.pi / 2  # Start from top
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            scene.add(Dot(x=x, y=y, radius=20 - ring * 2, color=colors[i]))

    scene.save(OUTPUT_DIR / "09-triadic-colors.svg")


def example_10_monochromatic_colors():
    """
    Demonstrate monochromatic (shades of one color)
    """
    scene = Scene(width=700, height=350, background="#f8f9fa")

    # Monochromatic shades of blue
    shades = ["#000033", "#000066", "#000099", "#0000cc", "#0000ff",
              "#3333ff", "#6666ff", "#9999ff", "#ccccff"]

    for i, shade in enumerate(shades):
        x = 70 + i * 70

        for j in range(5):
            y = 75 + j * 50
            scene.add(Dot(x=x, y=y, radius=16, color=shade))

    scene.save(OUTPUT_DIR / "10-monochromatic-colors.svg")


def example_11_color_harmony_palette():
    """
    Create a complete custom palette using color theory
    Using a complementary + analogous scheme
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Create palette with color harmony in mind
    # Base: Deep blue
    # Analogous: Blue-purple
    # Complementary: Orange
    harmony_palette = Palette(
        background="#0a0e27",      # Very dark blue
        primary="#1e3a8a",         # Deep blue
        secondary="#4c1d95",       # Blue-purple (analogous)
        accent="#fb923c",          # Orange (complementary)
        line="#312e81",            # Purple-blue
        grid="#1e293b"             # Dark blue-gray
    )

    scene.background = harmony_palette.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=harmony_palette.accent, radius=5)
        elif cell.brightness > 0.5:
            cell.add_dot(color=harmony_palette.primary, radius=4)
        elif cell.brightness > 0.3:
            cell.add_dot(color=harmony_palette.secondary, radius=3)

    scene.save(OUTPUT_DIR / "11-color-harmony-palette.svg")


def example_12_warm_vs_cool_palettes():
    """
    Compare warm and cool color palettes
    """
    scene = Scene(width=900, height=450, background="#f5f5f5")

    # Warm palette (left side)
    warm_palette = Palette(
        background="#2d1b00",
        primary="#ff6b35",
        secondary="#f7931e",
        accent="#ffd700",
        line="#ff4500",
        grid="#4a2511"
    )

    # Cool palette (right side)
    cool_palette = Palette(
        background="#001a33",
        primary="#00bfff",
        secondary="#4682b4",
        accent="#87ceeb",
        line="#1e90ff",
        grid="#0d3d56"
    )

    # Draw warm pattern on left
    for i in range(5):
        for j in range(5):
            x = 80 + i * 70
            y = 80 + j * 70
            brightness = (i + j) / 9.0

            if brightness > 0.7:
                scene.add(Dot(x=x, y=y, radius=15, color=warm_palette.accent))
            elif brightness > 0.4:
                scene.add(Dot(x=x, y=y, radius=12, color=warm_palette.primary))
            else:
                scene.add(Dot(x=x, y=y, radius=10, color=warm_palette.secondary))

    # Draw cool pattern on right
    for i in range(5):
        for j in range(5):
            x = 500 + i * 70
            y = 80 + j * 70
            brightness = (i + j) / 9.0

            if brightness > 0.7:
                scene.add(Dot(x=x, y=y, radius=15, color=cool_palette.accent))
            elif brightness > 0.4:
                scene.add(Dot(x=x, y=y, radius=12, color=cool_palette.primary))
            else:
                scene.add(Dot(x=x, y=y, radius=10, color=cool_palette.secondary))

    scene.save(OUTPUT_DIR / "12-warm-vs-cool-palettes.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Custom Palette
    "01-custom-palette-definition": example_01_custom_palette_definition,
    "02-custom-palette-usage": example_02_custom_palette_usage,
    "03-custom-palette-artistic": example_03_custom_palette_artistic,

    # From Existing Palette
    "04-existing-palette-base": example_04_existing_palette_base,
    "05-modified-palette": example_05_modified_palette,
    "06-palette-comparison": example_06_palette_comparison,

    # Color Theory
    "07-complementary-colors": example_07_complementary_colors,
    "08-analogous-colors": example_08_analogous_colors,
    "09-triadic-colors": example_09_triadic_colors,
    "10-monochromatic-colors": example_10_monochromatic_colors,
    "11-color-harmony-palette": example_11_color_harmony_palette,
    "12-warm-vs-cool-palettes": example_12_warm_vs_cool_palettes,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 04-creating-palettes.md...")

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
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        # Generate all
        generate_all()
