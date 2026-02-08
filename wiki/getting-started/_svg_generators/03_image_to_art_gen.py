#!/usr/bin/env python3
"""
SVG Generator for: getting-started/03-image-to-art.md

Generates visual examples for transforming images into generative art.

Corresponds to sections:
- Size-based on brightness
- Conditional rendering
- Different shapes by brightness
- Position along paths
- Complete Examples (Halftone, Color Threshold, Flow Fields)
- Background variations
- Palette usage
- Layering examples
"""

from pyfreeform import Scene, Palette, Polygon, map_range
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-image-to-art"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Create a test gradient image for consistent examples
def create_test_gradient() -> Path:
    """Create a simple gradient image for testing"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_image_to_art.png"

    # Create 400x400 gradient (radial with some variation)
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Radial gradient from center with diagonal bias
            center_x, center_y = 200, 200
            distance = ((x - center_x)**2 + (y - center_y)**2) ** 0.5
            max_distance = (200**2 + 200**2) ** 0.5

            # Add diagonal component
            diagonal = (x + y) / 800

            # Combine radial and diagonal
            t = min(distance / max_distance * 0.7 + diagonal * 0.3, 1.0)

            # Color interpolation (purple to yellow)
            r = int(100 + t * 155)
            g = int(80 + t * 175)
            b = int(200 - t * 150)

            draw.point((x, y), fill=(r, g, b))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_gradient()


# =============================================================================
# SECTION: Size-Based on Brightness
# =============================================================================

def example_01_size_based_brightness():
    """
    Map brightness (0-1) to radius (2-10)
    Shows how brightness drives dot size
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Map brightness (0-1) to radius (2-10)
        radius = 2 + cell.brightness * 8
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "01-size-based-brightness.svg")


# =============================================================================
# SECTION: Conditional Rendering
# =============================================================================

def example_02_conditional_bright_only():
    """Only draw in bright areas (brightness > 0.6)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Only bright areas
        if cell.brightness > 0.6:
            cell.add_dot(radius=8, color=cell.color)

    scene.save(OUTPUT_DIR / "02-conditional-bright-only.svg")


def example_03_conditional_dark_only():
    """Only draw in dark areas (brightness < 0.3)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "white"

    for cell in scene.grid:
        # Only dark areas
        if cell.brightness < 0.3:
            cell.add_border(color="black", width=1)

    scene.save(OUTPUT_DIR / "03-conditional-dark-only.svg")


def example_04_conditional_combined():
    """Combined conditional rendering with both bright and dark"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "#f5f5f5"

    for cell in scene.grid:
        # Bright areas: large dots
        if cell.brightness > 0.6:
            cell.add_dot(radius=8, color=cell.color)
        # Dark areas: borders
        elif cell.brightness < 0.3:
            cell.add_border(color="black", width=1)

    scene.save(OUTPUT_DIR / "04-conditional-combined.svg")


# =============================================================================
# SECTION: Different Shapes by Brightness
# =============================================================================

def example_05_shapes_by_brightness():
    """Use different shapes based on brightness levels"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "#fafafa"

    for cell in scene.grid:
        if cell.brightness > 0.7:
            # Bright: Hexagons
            cell.add_polygon(Polygon.hexagon(), fill=cell.color)

        elif cell.brightness > 0.4:
            # Medium: Curves
            curve = cell.add_curve(curvature=0.5, color=cell.color)
            cell.add_dot(along=curve, t=cell.brightness, radius=3)

        else:
            # Dark: Small dots
            cell.add_dot(radius=2, color=cell.color)

    scene.save(OUTPUT_DIR / "05-shapes-by-brightness.svg")


# =============================================================================
# SECTION: Position Along Paths
# =============================================================================

def example_06_position_along_diagonal():
    """Position dots along diagonal lines based on brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    scene.background = "#f8f8f8"

    for cell in scene.grid:
        # Create a diagonal line
        line = cell.add_diagonal(start="bottom_left", end="top_right", color="gray", width=0.5)

        # Position dot along line based on brightness
        # 0.0 = bottom-left, 1.0 = top-right
        cell.add_dot(
            along=line,
            t=cell.brightness,
            radius=4,
            color=cell.color
        )

    scene.save(OUTPUT_DIR / "06-position-along-diagonal.svg")


def example_07_position_along_curves():
    """Position dots along curves based on brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        # Create curved path
        curve = cell.add_curve(
            start="left",
            end="right",
            curvature=0.5,
            color="#cccccc",
            width=0.8
        )

        # Position multiple dots along the curve
        cell.add_dot(
            along=curve,
            t=cell.brightness,
            radius=5,
            color=cell.color
        )

    scene.save(OUTPUT_DIR / "07-position-along-curves.svg")


# =============================================================================
# SECTION: Halftone Effect
# =============================================================================

def example_08_halftone_effect():
    """Classic halftone pattern with inverted brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=50)
    scene.background = "white"

    for cell in scene.grid:
        # Invert brightness for halftone effect
        size = (1 - cell.brightness) * 8
        cell.add_dot(radius=size, color="black")

    scene.save(OUTPUT_DIR / "08-halftone-effect.svg")


def example_09_halftone_colored():
    """Halftone with original colors"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=50)
    scene.background = "white"

    for cell in scene.grid:
        # Inverted brightness but keep colors
        size = (1 - cell.brightness) * 6
        if size > 0.5:  # Only render if size is significant
            cell.add_dot(radius=size, color=cell.color)

    scene.save(OUTPUT_DIR / "09-halftone-colored.svg")


# =============================================================================
# SECTION: Color Threshold
# =============================================================================

def example_10_color_threshold():
    """Artistic color separation with palette"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(radius=6, color=colors.primary)
        elif cell.brightness > 0.4:
            cell.add_dot(radius=4, color=colors.secondary)
        elif cell.brightness > 0.2:
            cell.add_dot(radius=2, color=colors.accent)

    scene.save(OUTPUT_DIR / "10-color-threshold.svg")


def example_11_color_threshold_ocean():
    """Color threshold with ocean palette"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(radius=7, color=colors.primary)
        elif cell.brightness > 0.4:
            cell.add_dot(radius=5, color=colors.secondary)
        elif cell.brightness > 0.2:
            cell.add_dot(radius=3, color=colors.accent)

    scene.save(OUTPUT_DIR / "11-color-threshold-ocean.svg")


# =============================================================================
# SECTION: Flow Fields
# =============================================================================

def example_12_flow_fields():
    """Flowing curves based on image brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        # Curvature driven by brightness
        curvature = (cell.brightness - 0.5) * 2  # Range: -1 to 1

        curve = cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            color=cell.color,
            width=2
        )

        # Add dots along curves
        for t in [0.25, 0.5, 0.75]:
            cell.add_dot(
                along=curve,
                t=t,
                radius=2,
                color=cell.color
            )

    scene.save(OUTPUT_DIR / "12-flow-fields.svg")


def example_13_flow_fields_varied():
    """Flow fields with varied curvature and thickness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=25)
    scene.background = "#1a1a1a"

    for cell in scene.grid:
        # More extreme curvature
        curvature = (cell.brightness - 0.5) * 3

        # Width based on brightness
        width = 1 + cell.brightness * 2

        curve = cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            color=cell.color,
            width=width
        )

    scene.save(OUTPUT_DIR / "13-flow-fields-varied.svg")


# =============================================================================
# SECTION: Background Variations
# =============================================================================

def example_14_background_white():
    """Clean, minimalist white background"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "white"

    for cell in scene.grid:
        radius = 2 + cell.brightness * 6
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "14-background-white.svg")


def example_15_background_black():
    """Dramatic, bold black background"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "black"

    for cell in scene.grid:
        radius = 2 + cell.brightness * 6
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "15-background-black.svg")


def example_16_background_palette():
    """Palette-integrated background"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        radius = 2 + cell.brightness * 6
        # Use palette colors instead of image colors
        if cell.brightness > 0.7:
            color = colors.primary
        elif cell.brightness > 0.4:
            color = colors.secondary
        else:
            color = colors.accent
        cell.add_dot(radius=radius, color=color)

    scene.save(OUTPUT_DIR / "16-background-palette.svg")


# =============================================================================
# SECTION: Palette Usage
# =============================================================================

def example_17_palette_mapping():
    """Map brightness to palette colors"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Map brightness to palette colors
        if cell.brightness > 0.7:
            color = colors.primary
        elif cell.brightness > 0.4:
            color = colors.secondary
        else:
            color = colors.accent

        cell.add_dot(color=color, radius=5)

    scene.save(OUTPUT_DIR / "17-palette-mapping.svg")


def example_18_palette_forest():
    """Forest palette with brightness mapping"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.forest()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.6:
            color = colors.primary
        elif cell.brightness > 0.3:
            color = colors.secondary
        else:
            color = colors.accent

        radius = 2 + cell.brightness * 5
        cell.add_dot(color=color, radius=radius)

    scene.save(OUTPUT_DIR / "18-palette-forest.svg")


# =============================================================================
# SECTION: Layering Examples
# =============================================================================

def example_19_layering_basic():
    """Basic layering with z-index"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    Z_BACKGROUND = 0
    Z_SHAPES = 1
    Z_ACCENTS = 2

    for cell in scene.grid:
        # Background layer
        cell.add_fill(color=cell.color, z_index=Z_BACKGROUND)

        # Shape layer
        if cell.brightness > 0.5:
            cell.add_ellipse(
                rx=8, ry=6,
                fill="white",
                z_index=Z_SHAPES
            )

        # Accent layer
        cell.add_dot(
            radius=2,
            color="black",
            z_index=Z_ACCENTS
        )

    scene.save(OUTPUT_DIR / "19-layering-basic.svg")


def example_20_layering_complex():
    """Complex multi-layer composition"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=35)
    colors = Palette.midnight()
    scene.background = colors.background

    Z_BACKGROUND = 0
    Z_SHAPES = 1
    Z_ACCENTS = 2

    for cell in scene.grid:
        # Background fill layer
        if cell.brightness < 0.4:
            cell.add_fill(color=cell.color, z_index=Z_BACKGROUND)

        # Shape layer - curves
        if cell.brightness > 0.5:
            curve = cell.add_curve(
                start="bottom_left",
                end="top_right",
                curvature=0.6,
                color=colors.secondary,
                width=1.5,
                z_index=Z_SHAPES
            )

        # Accent layer - dots
        if cell.brightness > 0.7:
            cell.add_dot(
                radius=4,
                color=colors.primary,
                z_index=Z_ACCENTS
            )
        elif cell.brightness > 0.3:
            cell.add_dot(
                radius=2,
                color=colors.accent,
                z_index=Z_ACCENTS
            )

    scene.save(OUTPUT_DIR / "20-layering-complex.svg")


# =============================================================================
# SECTION: Advanced Techniques
# =============================================================================

def example_21_inverting_brightness():
    """Inverting brightness for light-on-dark effects"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "black"

    for cell in scene.grid:
        inverted = 1 - cell.brightness
        radius = 2 + inverted * 6
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "21-inverting-brightness.svg")


def example_22_mapping_ranges():
    """Use map_range to convert brightness to custom ranges"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Map brightness (0-1) to size (5-20)
        size = map_range(cell.brightness, 0, 1, 5, 20)
        cell.add_dot(radius=size, color=cell.color)

    scene.save(OUTPUT_DIR / "22-mapping-ranges.svg")


def example_23_neighbor_comparison():
    """Edge detection using neighbor comparisons"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    scene.background = "white"

    for cell in scene.grid:
        # Basic dot for all cells
        cell.add_dot(radius=3, color=cell.color)

        # Check right neighbor
        if cell.right:
            # Large difference = edge
            diff = abs(cell.brightness - cell.right.brightness)
            if diff > 0.3:
                cell.add_line(
                    start="center",
                    end="right",
                    width=2,
                    color="black"
                )

        # Check below neighbor
        if cell.below:
            diff = abs(cell.brightness - cell.below.brightness)
            if diff > 0.3:
                cell.add_line(
                    start="center",
                    end="bottom",
                    width=2,
                    color="black"
                )

    scene.save(OUTPUT_DIR / "23-neighbor-comparison.svg")


def example_24_mixed_techniques():
    """Combine multiple techniques in one artwork"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=35)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        # Size based on brightness
        size = 2 + cell.brightness * 7

        # Shape based on brightness
        if cell.brightness > 0.8:
            # Very bright: hexagons
            cell.add_polygon(Polygon.hexagon(), fill=colors.primary)

        elif cell.brightness > 0.6:
            # Bright: large dots
            cell.add_dot(radius=size, color=colors.primary)

        elif cell.brightness > 0.4:
            # Medium: curved paths with dots
            curve = cell.add_curve(
                start="bottom_left",
                end="top_right",
                curvature=(cell.brightness - 0.5) * 2,
                color=colors.secondary,
                width=1
            )
            cell.add_dot(
                along=curve,
                t=cell.brightness,
                radius=3,
                color=colors.accent
            )

        else:
            # Dark: small dots
            cell.add_dot(radius=2, color=colors.accent)

    scene.save(OUTPUT_DIR / "24-mixed-techniques.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Size-based on brightness
    "01-size-based-brightness": example_01_size_based_brightness,

    # Conditional rendering
    "02-conditional-bright-only": example_02_conditional_bright_only,
    "03-conditional-dark-only": example_03_conditional_dark_only,
    "04-conditional-combined": example_04_conditional_combined,

    # Different shapes by brightness
    "05-shapes-by-brightness": example_05_shapes_by_brightness,

    # Position along paths
    "06-position-along-diagonal": example_06_position_along_diagonal,
    "07-position-along-curves": example_07_position_along_curves,

    # Halftone effect
    "08-halftone-effect": example_08_halftone_effect,
    "09-halftone-colored": example_09_halftone_colored,

    # Color threshold
    "10-color-threshold": example_10_color_threshold,
    "11-color-threshold-ocean": example_11_color_threshold_ocean,

    # Flow fields
    "12-flow-fields": example_12_flow_fields,
    "13-flow-fields-varied": example_13_flow_fields_varied,

    # Background variations
    "14-background-white": example_14_background_white,
    "15-background-black": example_15_background_black,
    "16-background-palette": example_16_background_palette,

    # Palette usage
    "17-palette-mapping": example_17_palette_mapping,
    "18-palette-forest": example_18_palette_forest,

    # Layering examples
    "19-layering-basic": example_19_layering_basic,
    "20-layering-complex": example_20_layering_complex,

    # Advanced techniques
    "21-inverting-brightness": example_21_inverting_brightness,
    "22-mapping-ranges": example_22_mapping_ranges,
    "23-neighbor-comparison": example_23_neighbor_comparison,
    "24-mixed-techniques": example_24_mixed_techniques,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-image-to-art.md...")

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
