#!/usr/bin/env python3
"""
SVG Generator for: fundamentals/05-layering.md

Generates visual examples for z-index layering system.

Corresponds to sections:
- Understanding Z-Index
- Setting Z-Index
- Common Layering Patterns
- Practical Examples
- Z-Index Best Practices
- Advanced Layering
"""

from pyfreeform import Scene, Palette
from pyfreeform.config import DotStyle
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "05-layering"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_layering.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Diagonal gradient
            brightness = int(255 * (1 - ((x + y) / 800)))
            draw.point((x, y), fill=(brightness, brightness, brightness))

    img.save(temp_file)
    return temp_file

TEST_IMAGE = create_test_image()

# =============================================================================
# SECTION: Understanding Z-Index
# =============================================================================

def understanding_z_index():
    """Visual demonstration of z-index concept"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=250)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Bottom layer (z-index: -10)
    cell.add_ellipse(rx=80, ry=80, fill="#94a3b8", z_index=-10)
    cell.add_text("z=-10", font_size=14, color="white", z_index=-9)

    # Middle layer (z-index: 0)
    dot1 = cell.add_dot(radius=50, color="#3b82f6", z_index=0)
    dot1.move_by(dx=-30, dy=-30)

    # Top layer (z-index: 10)
    dot2 = cell.add_dot(radius=35, color="#ef4444", z_index=10)
    dot2.move_by(dx=20, dy=20)

    scene.save(OUTPUT_DIR / "01-understanding-z-index.svg")

# =============================================================================
# SECTION: Setting Z-Index - During Creation
# =============================================================================

def setting_z_index_during_creation():
    """Setting z-index during entity creation"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Background layer (z-index: 0)
    cell.add_fill(color="lightgray", z_index=0)

    # Middle layer (z-index: 1)
    cell.add_line(start="top_left", end="bottom_right", width=3, color="gray", z_index=1)

    # Foreground layer (z-index: 2)
    cell.add_dot(radius=15, color="red", z_index=2)

    scene.save(OUTPUT_DIR / "02-setting-z-index-during-creation.svg")

# =============================================================================
# SECTION: Setting Z-Index - After Creation
# =============================================================================

def setting_z_index_after_creation():
    """Modifying z-index after entity creation"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=120)
    scene.background = "white"

    cells = list(scene.grid)

    # Left: Default z-index (both at 0)
    cells[0].add_ellipse(rx=35, ry=35, fill="#3b82f6", z_index=0)
    cells[0].add_ellipse(rx=25, ry=25, fill="#ef4444", z_index=0)

    # Right: Modified z-index
    bg = cells[1].add_ellipse(rx=35, ry=35, fill="#3b82f6", z_index=0)
    fg = cells[1].add_ellipse(rx=25, ry=25, fill="#ef4444", z_index=0)
    fg.z_index = 10  # Move to top

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "03-setting-z-index-after-creation.svg")

# =============================================================================
# SECTION: Setting Z-Index - With Style Objects
# =============================================================================

def setting_z_index_with_styles():
    """Using z-index in style objects"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=120)
    scene.background = "white"

    cells = list(scene.grid)

    # Create styles with z-index
    background_style = DotStyle(radius=35, color="#94a3b8", z_index=0)
    foreground_style = DotStyle(radius=20, color="#ef4444", z_index=10)

    # Apply styles to both cells
    cells[0].add_dot(style=background_style)
    cells[0].add_dot(style=foreground_style)

    cells[1].add_dot(style=background_style)
    cells[1].add_dot(style=foreground_style)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "04-setting-z-index-with-styles.svg")

# =============================================================================
# SECTION: Common Pattern - Background → Shapes → Accents
# =============================================================================

def pattern_background_shapes_accents():
    """Common pattern: Background → Shapes → Accents"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    Z_BACKGROUND = 0
    Z_SHAPES = 1
    Z_ACCENTS = 2

    for cell in scene.grid:
        # Background
        cell.add_fill(color="#f0f0f0", z_index=Z_BACKGROUND)

        # Main shapes
        if cell.brightness > 0.5:
            cell.add_ellipse(rx=10, ry=8, fill=cell.color, z_index=Z_SHAPES)

        # Accent dots
        if cell.brightness > 0.7:
            cell.add_dot(radius=3, color="white", z_index=Z_ACCENTS)

    scene.save(OUTPUT_DIR / "05-pattern-background-shapes-accents.svg")

# =============================================================================
# SECTION: Common Pattern - Grid → Lines → Dots
# =============================================================================

def pattern_grid_lines_dots():
    """Common pattern: Grid → Lines → Dots"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
    scene.background = "white"

    Z_GRID = 0
    Z_LINES = 1
    Z_DOTS = 2

    # Grid borders (bottom layer)
    for cell in scene.grid.border(thickness=1):
        cell.add_border(color="#eeeeee", width=0.5, z_index=Z_GRID)

    # Diagonal lines (middle layer) - using start/end instead of direction
    for cell in scene.grid:
        if (cell.row + cell.col) % 3 == 0:
            cell.add_diagonal(start="bottom_left", end="top_right", color="#d1d5db", width=1, z_index=Z_LINES)

    # Dots (top layer)
    for cell in scene.grid:
        if (cell.row + cell.col) % 5 == 0:
            cell.add_dot(radius=4, color="#3b82f6", z_index=Z_DOTS)

    scene.save(OUTPUT_DIR / "06-pattern-grid-lines-dots.svg")

# =============================================================================
# SECTION: Practical Example - Dot on Line
# =============================================================================

def practical_dot_on_line():
    """Practical example: Dot on line"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Line behind (z-index: 0)
    line = cell.add_line(
        start="top_left",
        end="bottom_right",
        width=2,
        color="gray",
        z_index=0
    )

    # Dot on top (z-index: 1)
    cell.add_dot(
        along=line,
        t=0.5,
        radius=10,
        color="red",
        z_index=1
    )

    scene.save(OUTPUT_DIR / "07-practical-dot-on-line.svg")

# =============================================================================
# SECTION: Practical Example - Overlapping Cells
# =============================================================================

def practical_overlapping_cells():
    """Practical example: Overlapping cells"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=30)
    scene.background = "white"

    for cell in scene.grid:
        # Large background circle (might overlap neighbors)
        cell.add_ellipse(
            rx=20, ry=20,
            fill="#93c5fd",
            z_index=0
        )

        # Small foreground dot (always on top)
        cell.add_dot(
            radius=6,
            color="#1e3a8a",
            z_index=10
        )

    scene.save(OUTPUT_DIR / "08-practical-overlapping-cells.svg")

# =============================================================================
# SECTION: Practical Example - Text Overlay
# =============================================================================

def practical_text_overlay():
    """Practical example: Text overlay"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Create artwork (z-index: 0)
    for cell in scene.grid:
        radius = 2 + cell.brightness * 6
        cell.add_dot(color=cell.color, radius=radius, z_index=0)

    # Add label on top (z-index: 100) - using grid center cell
    from pyfreeform import Text
    center_cell = scene.grid[scene.grid.rows // 2, scene.grid.cols // 2]
    label = Text(
        x=scene.width // 2,
        y=scene.height // 2,
        content="OVERLAY",
        font_size=48,
        color="white",
        text_anchor="middle",
        baseline="middle",
        z_index=100
    )
    scene.add(label)

    scene.save(OUTPUT_DIR / "09-practical-text-overlay.svg")

# =============================================================================
# SECTION: Z-Index Best Practices - Named Constants
# =============================================================================

def best_practice_named_constants():
    """Best practice: Use named constants"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=25)
    scene.background = "white"

    # Define layer constants
    Z_BACKGROUND = 0
    Z_CONTENT = 5
    Z_OVERLAY = 10

    for cell in scene.grid:
        # Background
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color="#f3f4f6", z_index=Z_BACKGROUND)

        # Content
        if (cell.row + cell.col) % 3 == 0:
            cell.add_dot(radius=6, color="#6366f1", z_index=Z_CONTENT)

        # Overlay
        if cell.row == 5 and cell.col == 5:
            cell.add_dot(radius=10, color="#ef4444", z_index=Z_OVERLAY)

    scene.save(OUTPUT_DIR / "10-best-practice-named-constants.svg")

# =============================================================================
# SECTION: Z-Index Best Practices - Space Out Layers
# =============================================================================

def best_practice_space_out_layers():
    """Best practice: Space out z-index values"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Well-spaced layers
    Z_BACKGROUND = 0
    Z_LINES = 10
    Z_SHAPES = 20
    Z_ACCENTS = 30

    cell.add_fill(color="#f9fafb", z_index=Z_BACKGROUND)
    cell.add_line(start="left", end="right", width=2, color="#d1d5db", z_index=Z_LINES)
    cell.add_ellipse(rx=40, ry=40, fill="#93c5fd", z_index=Z_SHAPES)
    cell.add_dot(radius=15, color="#1e40af", z_index=Z_ACCENTS)

    scene.save(OUTPUT_DIR / "11-best-practice-space-out-layers.svg")

# =============================================================================
# SECTION: Advanced Layering - Dynamic Layer Assignment
# =============================================================================

def advanced_dynamic_layers():
    """Advanced: Dynamic layer assignment based on data"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=25)

    for cell in scene.grid:
        # Brighter cells render on top
        z = int(cell.brightness * 10)  # 0-10 range

        radius = 3 + cell.brightness * 5
        cell.add_dot(
            radius=radius,
            color=cell.color,
            z_index=z
        )

    scene.save(OUTPUT_DIR / "12-advanced-dynamic-layers.svg")

# =============================================================================
# SECTION: Advanced Layering - Layer Groups
# =============================================================================

def advanced_layer_groups():
    """Advanced: Layer groups with ranges"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
    scene.background = "white"

    # Define layer ranges
    LAYER_BACKGROUND = range(-10, 0)
    LAYER_CONTENT = range(0, 10)
    LAYER_FOREGROUND = range(10, 20)

    for cell in scene.grid:
        # Background layer
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color="#f3f4f6", z_index=LAYER_BACKGROUND.start)

        # Content layer
        cell.add_dot(radius=4, color="#6366f1", z_index=LAYER_CONTENT.start)

        # Foreground layer (corners)
        if (cell.row == 0 or cell.row == scene.grid.rows - 1) and \
           (cell.col == 0 or cell.col == scene.grid.cols - 1):
            cell.add_dot(radius=7, color="#ef4444", z_index=LAYER_FOREGROUND.start)

    scene.save(OUTPUT_DIR / "13-advanced-layer-groups.svg")

# =============================================================================
# SECTION: Complex Multi-Layer Example
# =============================================================================

def complex_multi_layer_example():
    """Complex multi-layer composition"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=25)
    colors = Palette.midnight()
    scene.background = colors.background

    # Define layers
    Z_GRID = 1
    Z_LINES = 2
    Z_DOTS_MAIN = 3
    Z_DOTS_HIGHLIGHT = 4

    # Layer 1: Subtle grid
    for cell in scene.grid.border(thickness=1):
        cell.add_border(color=colors.grid, width=0.5, z_index=Z_GRID)

    # Layer 2: Diagonal lines in medium brightness
    for cell in scene.grid:
        if 0.3 < cell.brightness < 0.7:
            cell.add_diagonal(
                start="bottom_left",
                end="top_right",
                color=colors.line,
                width=1,
                z_index=Z_LINES
            )

    # Layer 3: Main dots based on brightness
    for cell in scene.grid:
        size = 2 + cell.brightness * 6
        cell.add_dot(
            radius=size,
            color=cell.color,
            z_index=Z_DOTS_MAIN
        )

    # Layer 4: Highlight dots for bright areas
    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(
                radius=4,
                color=colors.accent,
                z_index=Z_DOTS_HIGHLIGHT
            )

    scene.save(OUTPUT_DIR / "14-complex-multi-layer-example.svg")

# =============================================================================
# SECTION: Debugging - Hidden Element
# =============================================================================

def debugging_hidden_element():
    """Debugging: Element hidden behind others"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=120)
    scene.background = "white"

    cells = list(scene.grid)

    # Left: Problem - red dot hidden (same z-index)
    cells[0].add_ellipse(rx=40, ry=40, fill="#3b82f6", z_index=0)
    cells[0].add_dot(radius=15, color="#ef4444", z_index=0)

    # Right: Fixed - red dot visible (higher z-index)
    cells[1].add_ellipse(rx=40, ry=40, fill="#3b82f6", z_index=0)
    dot = cells[1].add_dot(radius=15, color="#ef4444", z_index=0)
    dot.z_index = 10  # Fix

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "15-debugging-hidden-element.svg")

# =============================================================================
# SECTION: Comparison - With and Without Z-Index
# =============================================================================

def comparison_with_without_z_index():
    """Side-by-side comparison with and without proper z-index"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=150)
    scene.background = "white"

    cells = list(scene.grid)

    # Left: Without z-index management (messy)
    cells[0].add_ellipse(rx=50, ry=50, fill="#93c5fd")
    cells[0].add_ellipse(rx=35, ry=35, fill="#60a5fa")
    cells[0].add_ellipse(rx=20, ry=20, fill="#3b82f6")

    # Right: With proper z-index (clean layers)
    cells[1].add_ellipse(rx=50, ry=50, fill="#93c5fd", z_index=0)
    cells[1].add_ellipse(rx=35, ry=35, fill="#60a5fa", z_index=1)
    cells[1].add_ellipse(rx=20, ry=20, fill="#3b82f6", z_index=2)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "16-comparison-with-without-z-index.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Understanding z-index
    "01-understanding-z-index": understanding_z_index,

    # Setting z-index
    "02-setting-z-index-during-creation": setting_z_index_during_creation,
    "03-setting-z-index-after-creation": setting_z_index_after_creation,
    "04-setting-z-index-with-styles": setting_z_index_with_styles,

    # Common patterns
    "05-pattern-background-shapes-accents": pattern_background_shapes_accents,
    "06-pattern-grid-lines-dots": pattern_grid_lines_dots,

    # Practical examples
    "07-practical-dot-on-line": practical_dot_on_line,
    "08-practical-overlapping-cells": practical_overlapping_cells,
    "09-practical-text-overlay": practical_text_overlay,

    # Best practices
    "10-best-practice-named-constants": best_practice_named_constants,
    "11-best-practice-space-out-layers": best_practice_space_out_layers,

    # Advanced layering
    "12-advanced-dynamic-layers": advanced_dynamic_layers,
    "13-advanced-layer-groups": advanced_layer_groups,
    "14-complex-multi-layer-example": complex_multi_layer_example,

    # Debugging and comparison
    "15-debugging-hidden-element": debugging_hidden_element,
    "16-comparison-with-without-z-index": comparison_with_without_z_index,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 05-layering.md...")

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
