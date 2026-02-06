from pyfreeform.config import FillStyle
#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/06-grid-selections.md

Generates visual examples for grid selection methods.

Corresponds to sections:
- Selection Methods (Rows, Columns, Patterns, Regions, Conditional)
- Examples (Checkerboard, Border, Conditional, Center Cross)
- Chaining Patterns
"""

from pyfreeform import Scene
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "06-grid-selections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_test_image() -> Path:
    """Create a simple test image"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_selections.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            t = ((x - 200)**2 + (y - 200)**2) ** 0.5 / 282.8
            r = int(100 + t * 155)
            g = int(150 + t * 105)
            b = int(200 - t * 100)
            draw.point((x, y), fill=(r, g, b))

    img.save(temp_file)
    return temp_file

TEST_IMAGE = create_test_image()

# =============================================================================
# SECTION: Selection Methods - Rows and Columns
# =============================================================================

def selection_single_row():
    """Selecting a single row"""
    scene = Scene.with_grid(cols=15, rows=10, cell_size=20)
    scene.background = "#f8f9fa"

    # Highlight row 3
    for cell in scene.grid.row(3):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "01-selection-single-row.svg")

def selection_multiple_rows():
    """Selecting multiple rows"""
    scene = Scene.with_grid(cols=15, rows=10, cell_size=20)
    scene.background = "#f8f9fa"

    # Highlight rows 2, 5, 8
    for row_idx in [2, 5, 8]:
        for cell in scene.grid.row(row_idx):
            cell.add_fill(style=FillStyle(color="#10b981"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "02-selection-multiple-rows.svg")

def selection_single_column():
    """Selecting a single column"""
    scene = Scene.with_grid(cols=15, rows=10, cell_size=20)
    scene.background = "#f8f9fa"

    # Highlight column 7
    for cell in scene.grid.column(7):
        cell.add_fill(style=FillStyle(color="#f59e0b"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "03-selection-single-column.svg")

def selection_multiple_columns():
    """Selecting multiple columns"""
    scene = Scene.with_grid(cols=15, rows=10, cell_size=20)
    scene.background = "#f8f9fa"

    # Highlight columns 3, 7, 11
    for col_idx in [3, 7, 11]:
        for cell in scene.grid.column(col_idx):
            cell.add_fill(style=FillStyle(color="#ef4444"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "04-selection-multiple-columns.svg")

# =============================================================================
# SECTION: Selection Methods - Patterns
# =============================================================================

def selection_checkerboard_black():
    """Checkerboard pattern - black squares"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    for cell in scene.grid.checkerboard("black"):
        cell.add_fill(style=FillStyle(color="#1f2937"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "05-selection-checkerboard-black.svg")

def selection_checkerboard_white():
    """Checkerboard pattern - white squares"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#1f2937"

    for cell in scene.grid.checkerboard("white"):
        cell.add_fill(style=FillStyle(color="#f8f9fa"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#666666", width=0.3)

    scene.save(OUTPUT_DIR / "06-selection-checkerboard-white.svg")

def selection_border_thin():
    """Border selection - thin border"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    for cell in scene.grid.border(thickness=1):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "07-selection-border-thin.svg")

def selection_border_thick():
    """Border selection - thick border"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    for cell in scene.grid.border(thickness=3):
        cell.add_fill(style=FillStyle(color="#10b981"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "08-selection-border-thick.svg")

def selection_every_nth():
    """Every nth cell selection"""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=12)
    scene.background = "#f8f9fa"

    for cell in scene.grid.every(n=3):
        cell.add_dot(radius=4, color="#f59e0b")

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "09-selection-every-nth.svg")

def selection_every_nth_comparison():
    """Comparison of different every(n) values"""
    scene = Scene.with_grid(cols=20, rows=10, cell_size=8)
    scene.background = "#f8f9fa"

    # Show every(n=3) pattern
    for cell in scene.grid.every(n=3):
        cell.add_fill(color="#3b82f6")

    # Show grid lines
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "10-selection-every-nth-comparison.svg")

# =============================================================================
# SECTION: Selection Methods - Regions
# =============================================================================

def selection_region_basic():
    """Basic region selection"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    # Select region
    for cell in scene.grid.region(row_start=5, row_end=10, col_start=5, col_end=10):
        cell.add_fill(style=FillStyle(color="#8b5cf6"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "11-selection-region-basic.svg")

def selection_region_multiple():
    """Multiple region selections"""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=12)
    scene.background = "#f8f9fa"

    # Top-left region
    for cell in scene.grid.region(row_start=2, row_end=6, col_start=2, col_end=6):
        cell.add_fill(style=FillStyle(color="#ef4444"))

    # Top-right region
    for cell in scene.grid.region(row_start=2, row_end=6, col_start=14, col_end=18):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Bottom-center region
    for cell in scene.grid.region(row_start=9, row_end=13, col_start=8, col_end=12):
        cell.add_fill(style=FillStyle(color="#10b981"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "12-selection-region-multiple.svg")

# =============================================================================
# SECTION: Selection Methods - Conditional (where)
# =============================================================================

def selection_where_brightness():
    """Conditional selection based on brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Select bright cells
    for cell in scene.grid.where(lambda c: c.brightness > 0.7):
        cell.add_dot(radius=6, color="#f59e0b")

    scene.save(OUTPUT_DIR / "13-selection-where-brightness.svg")

def selection_where_position():
    """Conditional selection based on position"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "#f8f9fa"

    # Select cells in top-left quadrant
    for cell in scene.grid.where(lambda c: c.row < 10 and c.col < 10):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "14-selection-where-position.svg")

def selection_where_distance():
    """Conditional selection based on distance from center"""
    scene = Scene.with_grid(cols=21, rows=21, cell_size=12)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    # Select cells within certain distance from center
    def is_in_circle(cell):
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < 7

    for cell in scene.grid.where(is_in_circle):
        cell.add_fill(style=FillStyle(color="#10b981"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "15-selection-where-distance.svg")

# =============================================================================
# SECTION: Examples
# =============================================================================

def example_checkerboard_full():
    """Full checkerboard pattern"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid.checkerboard("black"):
        cell.add_fill(color="#1f2937")

    for cell in scene.grid.checkerboard("white"):
        cell.add_fill(color="#f8f9fa")

    scene.save(OUTPUT_DIR / "16-example-checkerboard-full.svg")

def example_border_highlight():
    """Border highlight with thick border"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "#f8f9fa"

    for cell in scene.grid.border(thickness=2):
        cell.add_border(color="#f59e0b", width=3)

    # Show other cells
    for cell in scene.grid:
        if cell not in scene.grid.border(thickness=2):
            cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "17-example-border-highlight.svg")

def example_conditional_brightness():
    """Conditional selection - bright areas only"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Bright areas with yellow dots
    for cell in scene.grid.where(lambda c: c.brightness > 0.6):
        cell.add_dot(radius=8, color="#f59e0b")

    scene.save(OUTPUT_DIR / "18-example-conditional-brightness.svg")

def example_center_cross():
    """Center cross pattern"""
    scene = Scene.with_grid(cols=21, rows=21, cell_size=12)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    # Horizontal line
    for cell in scene.grid.row(center_row):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Vertical line
    for cell in scene.grid.column(center_col):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "19-example-center-cross.svg")

def example_diagonal_lines():
    """Diagonal lines using conditional selection"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "#f8f9fa"

    # Main diagonal
    for cell in scene.grid.where(lambda c: c.row == c.col):
        cell.add_fill(style=FillStyle(color="#10b981"))

    # Anti-diagonal
    for cell in scene.grid.where(lambda c: c.row + c.col == scene.grid.rows - 1):
        cell.add_fill(style=FillStyle(color="#ef4444"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "20-example-diagonal-lines.svg")

# =============================================================================
# SECTION: Chaining Patterns
# =============================================================================

def chaining_bright_border():
    """Bright cells in border only"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Get border cells that are bright
    bright_border = [
        cell for cell in scene.grid.border()
        if cell.brightness > 0.5
    ]

    for cell in bright_border:
        cell.add_dot(color="#f59e0b", radius=8, z_index=10)

    scene.save(OUTPUT_DIR / "21-chaining-bright-border.svg")

def chaining_checkerboard_conditional():
    """Checkerboard with conditional modification"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    # Standard checkerboard
    for cell in scene.grid.checkerboard("black"):
        cell.add_fill(color="#1f2937")

    # Highlight center cells with dots
    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid.where(lambda c: abs(c.row - center_row) < 3 and abs(c.col - center_col) < 3):
        cell.add_dot(radius=4, color="#f59e0b", z_index=10)

    scene.save(OUTPUT_DIR / "22-chaining-checkerboard-conditional.svg")

def chaining_border_and_cross():
    """Border and center cross combined"""
    scene = Scene.with_grid(cols=21, rows=21, cell_size=12)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    # Border
    for cell in scene.grid.border(thickness=2):
        cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Center cross
    for cell in scene.grid.row(center_row):
        cell.add_fill(style=FillStyle(color="#10b981"))

    for cell in scene.grid.column(center_col):
        cell.add_fill(style=FillStyle(color="#10b981"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "23-chaining-border-and-cross.svg")

def chaining_complex_pattern():
    """Complex pattern with multiple selections"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=10)
    scene.background = "#f8f9fa"

    # Outer border
    for cell in scene.grid.border(thickness=1):
        cell.add_fill(style=FillStyle(color="#ef4444"))

    # Inner border
    for cell in scene.grid.border(thickness=2):
        if cell not in scene.grid.border(thickness=1):
            cell.add_fill(style=FillStyle(color="#f59e0b"))

    # Checkerboard in center
    center_cells = scene.grid.region(row_start=8, row_end=17, col_start=8, col_end=17)
    for cell in center_cells:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.2)

    scene.save(OUTPUT_DIR / "24-chaining-complex-pattern.svg")

def chaining_conditional_regions():
    """Multiple conditional selections"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    # Top-left quadrant
    for cell in scene.grid.where(lambda c: c.row < center_row and c.col < center_col):
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(style=FillStyle(color="#ef4444"))

    # Top-right quadrant
    for cell in scene.grid.where(lambda c: c.row < center_row and c.col >= center_col):
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(style=FillStyle(color="#3b82f6"))

    # Bottom-left quadrant
    for cell in scene.grid.where(lambda c: c.row >= center_row and c.col < center_col):
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(style=FillStyle(color="#10b981"))

    # Bottom-right quadrant
    for cell in scene.grid.where(lambda c: c.row >= center_row and c.col >= center_col):
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(style=FillStyle(color="#f59e0b"))

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "25-chaining-conditional-regions.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Rows and columns
    "01-selection-single-row": selection_single_row,
    "02-selection-multiple-rows": selection_multiple_rows,
    "03-selection-single-column": selection_single_column,
    "04-selection-multiple-columns": selection_multiple_columns,

    # Patterns
    "05-selection-checkerboard-black": selection_checkerboard_black,
    "06-selection-checkerboard-white": selection_checkerboard_white,
    "07-selection-border-thin": selection_border_thin,
    "08-selection-border-thick": selection_border_thick,
    "09-selection-every-nth": selection_every_nth,
    "10-selection-every-nth-comparison": selection_every_nth_comparison,

    # Regions
    "11-selection-region-basic": selection_region_basic,
    "12-selection-region-multiple": selection_region_multiple,

    # Conditional (where)
    "13-selection-where-brightness": selection_where_brightness,
    "14-selection-where-position": selection_where_position,
    "15-selection-where-distance": selection_where_distance,

    # Examples
    "16-example-checkerboard-full": example_checkerboard_full,
    "17-example-border-highlight": example_border_highlight,
    "18-example-conditional-brightness": example_conditional_brightness,
    "19-example-center-cross": example_center_cross,
    "20-example-diagonal-lines": example_diagonal_lines,

    # Chaining
    "21-chaining-bright-border": chaining_bright_border,
    "22-chaining-checkerboard-conditional": chaining_checkerboard_conditional,
    "23-chaining-border-and-cross": chaining_border_and_cross,
    "24-chaining-complex-pattern": chaining_complex_pattern,
    "25-chaining-conditional-regions": chaining_conditional_regions,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 06-grid-selections.md...")

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
