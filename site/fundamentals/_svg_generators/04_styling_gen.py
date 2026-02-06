#!/usr/bin/env python3
"""
SVG Generator for: fundamentals/04-styling.md

Generates visual examples for styling and color systems.

Corresponds to sections:
- Color System (named colors, hex, RGB)
- Inline Styling
- Style Objects
- Palettes
- Opacity and Transparency
- Common Styling Patterns
- Stroke vs Fill
- Line Caps
"""

from pyfreeform import Scene, Palette
from pyfreeform.config import DotStyle, LineStyle, FillStyle
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "04-styling"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_styling.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Radial gradient
            dx = x - 200
            dy = y - 200
            dist = (dx*dx + dy*dy) ** 0.5
            brightness = int(255 * (1 - min(dist / 282.8, 1)))
            draw.point((x, y), fill=(brightness, brightness, brightness))

    img.save(temp_file)
    return temp_file

TEST_IMAGE = create_test_image()

# =============================================================================
# SECTION: Color System - Named Colors
# =============================================================================

def color_named_colors():
    """Named color examples"""
    scene = Scene.with_grid(cols=8, rows=1, cell_size=50)
    scene.background = "white"

    cells = list(scene.grid)
    colors = ["red", "coral", "dodgerblue", "mediumseagreen", "purple", "orange", "pink", "cyan"]

    for i, color in enumerate(colors):
        cells[i].add_dot(radius=15, color=color)

    scene.save(OUTPUT_DIR / "01-color-named-colors.svg")

# =============================================================================
# SECTION: Color System - Hex Colors
# =============================================================================

def color_hex_colors():
    """Hex color examples"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=70)
    scene.background = "white"

    cells = list(scene.grid)
    hex_colors = ["#ff5733", "#3498db", "#2ecc71", "#f39c12"]

    for i, color in enumerate(hex_colors):
        cells[i].add_dot(radius=20, color=color)

    scene.save(OUTPUT_DIR / "02-color-hex-colors.svg")

# =============================================================================
# SECTION: Color System - RGB Tuples
# =============================================================================

def color_rgb_tuples():
    """RGB tuple color examples"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=70)
    scene.background = "white"

    cells = list(scene.grid)
    rgb_colors = [(255, 87, 51), (52, 152, 219), (46, 204, 113), (243, 156, 18)]

    for i, color in enumerate(rgb_colors):
        cells[i].add_dot(radius=20, color=color)

    scene.save(OUTPUT_DIR / "03-color-rgb-tuples.svg")

# =============================================================================
# SECTION: Inline Styling - Dots
# =============================================================================

def inline_styling_dots():
    """Inline styling for dots"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=70)
    scene.background = "white"

    cells = list(scene.grid)

    cells[0].add_dot(radius=5, color="coral")
    cells[1].add_dot(radius=8, color="navy")
    cells[2].add_dot(radius=12, color="purple")
    cells[3].add_dot(radius=15, color="green")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "04-inline-styling-dots.svg")

# =============================================================================
# SECTION: Inline Styling - Lines
# =============================================================================

def inline_styling_lines():
    """Inline styling for lines"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    cells[0].add_line(start="top_left", end="bottom_right", width=1, color="navy")
    cells[1].add_line(start="top_left", end="bottom_right", width=3, color="coral")
    cells[2].add_line(start="top_left", end="bottom_right", width=5, color="purple")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "05-inline-styling-lines.svg")

# =============================================================================
# SECTION: Inline Styling - Shapes
# =============================================================================

def inline_styling_shapes():
    """Inline styling for shapes (fill and stroke)"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Fill only
    cells[0].add_ellipse(rx=25, ry=20, fill="coral")

    # Fill and stroke
    cells[1].add_ellipse(rx=25, ry=20, fill="lightblue", stroke="navy", stroke_width=2)

    # Stroke only
    cells[2].add_ellipse(rx=25, ry=20, fill="none", stroke="purple", stroke_width=3)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "06-inline-styling-shapes.svg")

# =============================================================================
# SECTION: Style Objects - DotStyle
# =============================================================================

def style_objects_dot():
    """Using DotStyle objects"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Create reusable style
    style = DotStyle(radius=12, color="coral", z_index=0)

    # Use style
    cells[0].add_dot(style=style)

    # Override with inline
    cells[1].add_dot(style=style, color="blue")

    # Builder method
    large = style.with_radius(18)
    cells[2].add_dot(style=large)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "07-style-objects-dot.svg")

# =============================================================================
# SECTION: Style Objects - LineStyle
# =============================================================================

def style_objects_line():
    """Using LineStyle objects"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Create reusable styles
    thin_style = LineStyle(width=1, color="navy")
    medium_style = LineStyle(width=3, color="coral")
    thick_style = LineStyle(width=5, color="purple")

    cells[0].add_line(start="left", end="right", style=thin_style)
    cells[1].add_line(start="left", end="right", style=medium_style)
    cells[2].add_line(start="left", end="right", style=thick_style)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "08-style-objects-line.svg")

# =============================================================================
# SECTION: Palettes - Overview
# =============================================================================

def palettes_overview():
    """Overview of different palettes"""
    scene = Scene.with_grid(cols=8, rows=1, cell_size=50)

    palettes = [
        Palette.midnight(),
        Palette.sunset(),
        Palette.ocean(),
        Palette.forest(),
        Palette.monochrome(),
        Palette.paper(),
        Palette.neon(),
        Palette.pastel(),
    ]

    cells = list(scene.grid)

    for i, palette in enumerate(palettes):
        cells[i].add_fill(color=palette.background)
        cells[i].add_dot(radius=15, color=palette.primary)

    scene.save(OUTPUT_DIR / "09-palettes-overview.svg")

# =============================================================================
# SECTION: Palettes - Midnight
# =============================================================================

def palette_midnight():
    """Midnight palette demonstration"""
    colors = Palette.midnight()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=70)
    scene.background = colors.background

    cells = list(scene.grid)

    cells[0].add_dot(radius=20, color=colors.primary)
    cells[1].add_dot(radius=20, color=colors.secondary)
    cells[2].add_dot(radius=20, color=colors.accent)
    cells[3].add_line(start="top", end="bottom", width=3, color=colors.line)
    # Rectangle using polygon
    rect_points = [(-25, -25), (25, -25), (25, 25), (-25, 25)]
    cells[4].add_polygon(rect_points, fill="none", stroke=colors.grid, stroke_width=1)

    scene.save(OUTPUT_DIR / "10-palette-midnight.svg")

# =============================================================================
# SECTION: Palettes - Sunset
# =============================================================================

def palette_sunset():
    """Sunset palette demonstration"""
    colors = Palette.sunset()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=70)
    scene.background = colors.background

    cells = list(scene.grid)

    cells[0].add_dot(radius=20, color=colors.primary)
    cells[1].add_dot(radius=20, color=colors.secondary)
    cells[2].add_dot(radius=20, color=colors.accent)
    cells[3].add_line(start="top", end="bottom", width=3, color=colors.line)
    # Rectangle using polygon
    rect_points = [(-25, -25), (25, -25), (25, 25), (-25, 25)]
    cells[4].add_polygon(rect_points, fill="none", stroke=colors.grid, stroke_width=1)

    scene.save(OUTPUT_DIR / "11-palette-sunset.svg")

# =============================================================================
# SECTION: Palettes - Ocean
# =============================================================================

def palette_ocean():
    """Ocean palette demonstration"""
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=70)
    scene.background = colors.background

    cells = list(scene.grid)

    cells[0].add_dot(radius=20, color=colors.primary)
    cells[1].add_dot(radius=20, color=colors.secondary)
    cells[2].add_dot(radius=20, color=colors.accent)
    cells[3].add_line(start="top", end="bottom", width=3, color=colors.line)
    # Rectangle using polygon
    rect_points = [(-25, -25), (25, -25), (25, 25), (-25, 25)]
    cells[4].add_polygon(rect_points, fill="none", stroke=colors.grid, stroke_width=1)

    scene.save(OUTPUT_DIR / "12-palette-ocean.svg")

# =============================================================================
# SECTION: Opacity and Transparency
# =============================================================================

def opacity_demonstration():
    """Opacity and transparency demonstration"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Opacities: 1.0, 0.75, 0.5, 0.25 (using ellipses instead since opacity works with them)
    cells[0].add_ellipse(rx=30, ry=30, fill="blue")
    cells[1].add_ellipse(rx=30, ry=30, fill="#3b82f6")  # Using lighter blue for effect
    cells[2].add_ellipse(rx=30, ry=30, fill="#60a5fa")  # Even lighter
    cells[3].add_ellipse(rx=30, ry=30, fill="#93c5fd")  # Lightest

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "13-opacity-demonstration.svg")

# =============================================================================
# SECTION: Common Styling Patterns - Consistent Palette
# =============================================================================

def pattern_consistent_palette():
    """Common pattern: Using a consistent palette"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=colors.primary, radius=6)
        elif cell.brightness > 0.4:
            cell.add_dot(color=colors.secondary, radius=4)
        else:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "14-pattern-consistent-palette.svg")

# =============================================================================
# SECTION: Common Styling Patterns - Style Reuse
# =============================================================================

def pattern_style_reuse():
    """Common pattern: Reusing styles"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
    scene.background = "white"

    # Define styles once
    large_style = DotStyle(radius=6, color="coral")
    small_style = DotStyle(radius=2, color="navy")

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(style=large_style)
        else:
            cell.add_dot(style=small_style)

    scene.save(OUTPUT_DIR / "15-pattern-style-reuse.svg")

# =============================================================================
# SECTION: Common Styling Patterns - Data-Driven Colors
# =============================================================================

def pattern_data_driven_colors():
    """Common pattern: Data-driven colors"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        # Use actual image color
        radius = 3 + cell.brightness * 5
        cell.add_dot(color=cell.color, radius=radius)

    scene.save(OUTPUT_DIR / "16-pattern-data-driven-colors.svg")

# =============================================================================
# SECTION: Common Styling Patterns - Gradient Effect
# =============================================================================

def pattern_gradient_effect():
    """Common pattern: Gradient effect"""
    scene = Scene.with_grid(cols=30, rows=20, cell_size=15)
    scene.background = "white"

    for cell in scene.grid:
        # Interpolate between colors based on position
        t = cell.col / scene.grid.cols

        # Simple red-to-blue gradient
        r = int(255 * (1 - t))
        b = int(255 * t)
        color = (r, 0, b)

        cell.add_dot(color=color, radius=5)

    scene.save(OUTPUT_DIR / "17-pattern-gradient-effect.svg")

# =============================================================================
# SECTION: Stroke vs Fill - Fill Only
# =============================================================================

def stroke_fill_only():
    """Shapes with fill only"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    cells[0].add_ellipse(rx=25, ry=20, fill="coral")
    rect_points = [(-25, -20), (25, -20), (25, 20), (-25, 20)]
    cells[1].add_polygon(rect_points, fill="lightblue")
    cells[2].add_polygon([(0, -20), (20, 15), (-20, 15)], fill="lightgreen")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "18-stroke-fill-only.svg")

# =============================================================================
# SECTION: Stroke vs Fill - Stroke Only
# =============================================================================

def stroke_stroke_only():
    """Shapes with stroke only"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    cells[0].add_ellipse(rx=25, ry=20, fill="none", stroke="coral", stroke_width=2)
    rect_points = [(-25, -20), (25, -20), (25, 20), (-25, 20)]
    cells[1].add_polygon(rect_points, fill="none", stroke="navy", stroke_width=2)
    cells[2].add_polygon([(0, -20), (20, 15), (-20, 15)], fill="none", stroke="green", stroke_width=2)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "19-stroke-stroke-only.svg")

# =============================================================================
# SECTION: Stroke vs Fill - Both
# =============================================================================

def stroke_both_fill_and_stroke():
    """Shapes with both fill and stroke"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    cells[0].add_ellipse(rx=25, ry=20, fill="coral", stroke="darkred", stroke_width=2)
    rect_points = [(-25, -20), (25, -20), (25, 20), (-25, 20)]
    cells[1].add_polygon(rect_points, fill="lightblue", stroke="navy", stroke_width=2)
    cells[2].add_polygon([(0, -20), (20, 15), (-20, 15)], fill="lightgreen", stroke="darkgreen", stroke_width=2)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "20-stroke-both-fill-and-stroke.svg")

# =============================================================================
# SECTION: Line Caps
# =============================================================================

def line_caps():
    """Line cap styles"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Round caps
    round_style = LineStyle(width=8, color="navy", cap="round")
    cells[0].add_line(start="left", end="right", style=round_style)

    # Square caps
    square_style = LineStyle(width=8, color="navy", cap="square")
    cells[1].add_line(start="left", end="right", style=square_style)

    # Butt caps
    butt_style = LineStyle(width=8, color="navy", cap="butt")
    cells[2].add_line(start="left", end="right", style=butt_style)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "21-line-caps.svg")

# =============================================================================
# SECTION: Font Styling
# =============================================================================

def font_styling():
    """Font styling options"""
    scene = Scene.with_grid(cols=3, rows=2, cell_size=100)
    scene.background = "white"

    cells = list(scene.grid)

    # Font sizes
    cells[0].add_text("Small", font_size=12, color="black")
    cells[1].add_text("Medium", font_size=18, color="black")
    cells[2].add_text("Large", font_size=24, color="black")

    # Font families
    cells[3].add_text("Sans", font_size=16, font_family="sans-serif", color="black")
    cells[4].add_text("Serif", font_size=16, font_family="serif", color="black")
    cells[5].add_text("Mono", font_size=16, font_family="monospace", color="black")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "22-font-styling.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Color system
    "01-color-named-colors": color_named_colors,
    "02-color-hex-colors": color_hex_colors,
    "03-color-rgb-tuples": color_rgb_tuples,

    # Inline styling
    "04-inline-styling-dots": inline_styling_dots,
    "05-inline-styling-lines": inline_styling_lines,
    "06-inline-styling-shapes": inline_styling_shapes,

    # Style objects
    "07-style-objects-dot": style_objects_dot,
    "08-style-objects-line": style_objects_line,

    # Palettes
    "09-palettes-overview": palettes_overview,
    "10-palette-midnight": palette_midnight,
    "11-palette-sunset": palette_sunset,
    "12-palette-ocean": palette_ocean,

    # Opacity
    "13-opacity-demonstration": opacity_demonstration,

    # Common patterns
    "14-pattern-consistent-palette": pattern_consistent_palette,
    "15-pattern-style-reuse": pattern_style_reuse,
    "16-pattern-data-driven-colors": pattern_data_driven_colors,
    "17-pattern-gradient-effect": pattern_gradient_effect,

    # Stroke vs Fill
    "18-stroke-fill-only": stroke_fill_only,
    "19-stroke-stroke-only": stroke_stroke_only,
    "20-stroke-both-fill-and-stroke": stroke_both_fill_and_stroke,

    # Line caps and fonts
    "21-line-caps": line_caps,
    "22-font-styling": font_styling,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 04-styling.md...")

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
            print(f"Available: {', '.join(sorted(GENERATORS.keys()))}")
    else:
        generate_all()
