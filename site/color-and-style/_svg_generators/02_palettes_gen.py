#!/usr/bin/env python3
"""
SVG Generator for: color-and-style/02-palettes.md

Generates beautiful visual examples showcasing all available palettes.

Corresponds to sections:
- Available Palettes
- Palette Properties
- Usage
"""

from pyfreeform import Scene, Palette, Dot, Line, Rect
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-palettes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Create a test gradient image for consistent examples
def create_test_gradient() -> Path:
    """Create a simple gradient image for testing"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_gradient_palettes.png"

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
# SECTION: Available Palettes - Individual Showcases
# =============================================================================

def example_01_palette_midnight():
    """Showcase the midnight palette - dark blue theme"""
    colors = Palette.midnight()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "01-palette-midnight.svg")


def example_02_palette_sunset():
    """Showcase the sunset palette - warm oranges"""
    colors = Palette.sunset()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "02-palette-sunset.svg")


def example_03_palette_ocean():
    """Showcase the ocean palette - cool blues"""
    colors = Palette.ocean()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "03-palette-ocean.svg")


def example_04_palette_forest():
    """Showcase the forest palette - natural greens"""
    colors = Palette.forest()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "04-palette-forest.svg")


def example_05_palette_monochrome():
    """Showcase the monochrome palette - black and white"""
    colors = Palette.monochrome()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "05-palette-monochrome.svg")


def example_06_palette_paper():
    """Showcase the paper palette - beige tones"""
    colors = Palette.paper()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "06-palette-paper.svg")


def example_07_palette_neon():
    """Showcase the neon palette - vibrant colors"""
    colors = Palette.neon()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "07-palette-neon.svg")


def example_08_palette_pastel():
    """Showcase the pastel palette - soft colors"""
    colors = Palette.pastel()
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=4)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        elif cell.brightness > 0.2:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "08-palette-pastel.svg")


# =============================================================================
# SECTION: Palette Properties
# =============================================================================

def example_09_palette_properties():
    """
    Demonstrate all palette properties: background, primary, secondary, accent, line, grid
    """
    colors = Palette.ocean()
    scene = Scene(width=700, height=500, background=colors.background)

    # Create a grid pattern to show all properties
    grid_spacing = 80
    start_x = 100
    start_y = 100

    # Background (shown as scene background)
    # Primary color dots
    for i in range(3):
        for j in range(3):
            x = start_x + i * grid_spacing
            y = start_y + j * grid_spacing
            scene.add(Dot(x=x, y=y, radius=15, color=colors.primary))

    # Secondary color dots (offset pattern)
    for i in range(2):
        for j in range(2):
            x = start_x + 40 + i * grid_spacing
            y = start_y + 40 + j * grid_spacing
            scene.add(Dot(x=x, y=y, radius=12, color=colors.secondary))

    # Accent color dots (corners)
    accent_positions = [(start_x - 40, start_y - 40), (start_x + 200, start_y - 40),
                        (start_x - 40, start_y + 200), (start_x + 200, start_y + 200)]
    for x, y in accent_positions:
        scene.add(Dot(x=x, y=y, radius=20, color=colors.accent))

    # Line color - draw connecting lines
    scene.add(Line(x1=start_x, y1=start_y, x2=start_x + 160, y2=start_y, color=colors.line, width=2))
    scene.add(Line(x1=start_x, y1=start_y, x2=start_x, y2=start_y + 160, color=colors.line, width=2))

    # Grid color - draw a border box
    box_x, box_y = 400, 100
    box_size = 200
    for i in range(5):
        for j in range(5):
            x = box_x + i * (box_size / 4)
            y = box_y + j * (box_size / 4)
            scene.add(Dot(x=x, y=y, radius=3, color=colors.grid))

    scene.save(OUTPUT_DIR / "09-palette-properties.svg")


# =============================================================================
# SECTION: Usage Example
# =============================================================================

def example_10_usage_before_palette():
    """Before applying palette - original image colors"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=cell.color, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=cell.color, radius=3)
        else:
            cell.add_dot(color=cell.color, radius=2)

    scene.save(OUTPUT_DIR / "10-usage-before-palette.svg")


def example_11_usage_with_midnight():
    """After applying midnight palette"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        else:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "11-usage-with-midnight.svg")


def example_12_usage_with_ocean():
    """Try different palette - ocean"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        else:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "12-usage-with-ocean.svg")


def example_13_usage_with_sunset():
    """Try different palette - sunset"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=3)
        else:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "13-usage-with-sunset.svg")


# =============================================================================
# SECTION: Palette Comparison Grid
# =============================================================================

def example_14_all_palettes_comparison():
    """
    Create a beautiful comparison showing all palettes side by side
    """
    palette_list = [
        ("midnight", Palette.midnight()),
        ("sunset", Palette.sunset()),
        ("ocean", Palette.ocean()),
        ("forest", Palette.forest()),
        ("monochrome", Palette.monochrome()),
        ("paper", Palette.paper()),
        ("neon", Palette.neon()),
        ("pastel", Palette.pastel()),
    ]

    scene = Scene(width=900, height=600, background="#f5f5f5")

    # Create color swatches for each palette
    cols = 4
    swatch_width = 180
    swatch_height = 120
    margin = 30

    for idx, (_name, colors) in enumerate(palette_list):
        row = idx // cols
        col = idx % cols

        x_base = margin + col * swatch_width
        y_base = margin + row * swatch_height

        # Background swatch
        scene.add(Rect(
            x=x_base,
            y=y_base,
            width=swatch_width - 20,
            height=swatch_height - 20,
            fill=colors.background
        ))

        # Color dots arranged in a pattern
        center_x = x_base + (swatch_width - 20) / 2
        center_y = y_base + (swatch_height - 20) / 2

        # Primary (large center)
        scene.add(Dot(x=center_x, y=center_y, radius=18, color=colors.primary))

        # Secondary (medium, four corners)
        offset = 25
        scene.add(Dot(x=center_x - offset, y=center_y - offset, radius=10, color=colors.secondary))
        scene.add(Dot(x=center_x + offset, y=center_y - offset, radius=10, color=colors.secondary))
        scene.add(Dot(x=center_x - offset, y=center_y + offset, radius=10, color=colors.secondary))
        scene.add(Dot(x=center_x + offset, y=center_y + offset, radius=10, color=colors.secondary))

        # Accent (small, sides)
        scene.add(Dot(x=center_x - offset, y=center_y, radius=6, color=colors.accent))
        scene.add(Dot(x=center_x + offset, y=center_y, radius=6, color=colors.accent))
        scene.add(Dot(x=center_x, y=center_y - offset, radius=6, color=colors.accent))
        scene.add(Dot(x=center_x, y=center_y + offset, radius=6, color=colors.accent))

    scene.save(OUTPUT_DIR / "14-all-palettes-comparison.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Individual palette showcases
    "01-palette-midnight": example_01_palette_midnight,
    "02-palette-sunset": example_02_palette_sunset,
    "03-palette-ocean": example_03_palette_ocean,
    "04-palette-forest": example_04_palette_forest,
    "05-palette-monochrome": example_05_palette_monochrome,
    "06-palette-paper": example_06_palette_paper,
    "07-palette-neon": example_07_palette_neon,
    "08-palette-pastel": example_08_palette_pastel,

    # Palette properties
    "09-palette-properties": example_09_palette_properties,

    # Usage examples
    "10-usage-before-palette": example_10_usage_before_palette,
    "11-usage-with-midnight": example_11_usage_with_midnight,
    "12-usage-with-ocean": example_12_usage_with_ocean,
    "13-usage-with-sunset": example_13_usage_with_sunset,

    # Comparison
    "14-all-palettes-comparison": example_14_all_palettes_comparison,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-palettes.md...")

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
