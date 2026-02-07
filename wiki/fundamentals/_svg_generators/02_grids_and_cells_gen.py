#!/usr/bin/env python3
"""
SVG Generator for: fundamentals/02-grids-and-cells.md

Generates visual examples for grid and cell operations (~18 examples).

Corresponds to sections:
- Creating Grids
- Accessing Cells
- Cell Properties and Helpers
- Grid Iteration Patterns
- Grid Selection Methods
- Common Patterns (checkerboard, radial, wave)
"""

from pyfreeform import Scene, Grid, Palette
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile
import math

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-grids-and-cells"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_test_image() -> Path:
    """Create a simple test image"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_grids.png"
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
# SECTION: Creating Grids
# =============================================================================

def create_via_from_image():
    """Creating grids via Scene.from_image()"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Show grid structure
    for cell in scene.grid:
        cell.add_border(color="#ffffff", width=0.5)

    scene.save(OUTPUT_DIR / "create-via-from-image.svg")

def create_via_with_grid():
    """Creating grids via Scene.with_grid()"""
    scene = Scene.with_grid(cols=30, rows=30, cell_size=12)

    # Show grid structure
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "create-via-with-grid.svg")

def create_manual_grid():
    """Manual grid creation"""
    scene = Scene(width=375, height=300, background="#f8f9fa")

    grid = Grid(cols=25, rows=20, cell_size=15, origin=(0, 0))

    for cell in grid:
        cell.add_border(color="#cccccc", width=0.5)

    scene.save(OUTPUT_DIR / "create-manual-grid.svg")

# =============================================================================
# SECTION: Accessing Cells
# =============================================================================

def access_by_index():
    """Accessing cells by index"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=20)

    # Highlight specific cells
    scene.grid[10, 5].add_fill(color="#3b82f6")  # Row 10, Col 5
    scene.grid[0, 0].add_fill(color="#ef4444")    # First cell
    scene.grid[14, 14].add_fill(color="#10b981")  # Last cell

    # Show grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "access-by-index.svg")

def access_iteration():
    """Iterating over all cells"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=15)

    # Iterate all cells (row by row)
    for cell in scene.grid:
        cell.add_dot(radius=3, color="#6366f1")

    scene.save(OUTPUT_DIR / "access-iteration.svg")

# =============================================================================
# SECTION: Cell Properties - Position Helpers
# =============================================================================

def cell_position_helpers():
    """Cell position helpers visualization"""
    scene = Scene.with_grid(cols=3, rows=3, cell_size=80)
    scene.background = "#f8f9fa"

    # Show one cell's position helpers
    cell = scene.grid[1, 1]  # Center cell

    # Draw dots at each position
    positions = {
        "center": "#ef4444",
        "top_left": "#3b82f6",
        "top_right": "#10b981",
        "bottom_left": "#f59e0b",
        "bottom_right": "#8b5cf6",
        "top": "#ec4899",
        "bottom": "#14b8a6",
        "left": "#f97316",
        "right": "#84cc16",
    }

    for pos_name, color in positions.items():
        cell.add_dot(at=pos_name, radius=5, color=color)

    # Show grid
    for c in scene.grid:
        c.add_border(color="#d1d5db", width=1)

    scene.save(OUTPUT_DIR / "cell-position-helpers.svg")

def cell_named_positions():
    """Using named positions vs relative coordinates"""
    scene = Scene.with_grid(cols=4, rows=2, cell_size=60)
    scene.background = "white"

    # Row 1: Named positions
    scene.grid[0, 0].add_dot(at="center", radius=6, color="red")
    scene.grid[0, 1].add_dot(at="top_left", radius=6, color="blue")
    scene.grid[0, 2].add_dot(at="bottom_right", radius=6, color="green")
    scene.grid[0, 3].add_dot(at="right", radius=6, color="purple")

    # Row 2: Relative coordinates (equivalent)
    scene.grid[1, 0].add_dot(at=(0.5, 0.5), radius=6, color="red")
    scene.grid[1, 1].add_dot(at=(0, 0), radius=6, color="blue")
    scene.grid[1, 2].add_dot(at=(1, 1), radius=6, color="green")
    scene.grid[1, 3].add_dot(at=(1, 0.5), radius=6, color="purple")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "cell-named-positions.svg")

# =============================================================================
# SECTION: Neighbor Access
# =============================================================================

def cell_neighbors():
    """Cell neighbor access visualization"""
    scene = Scene.with_grid(cols=11, rows=11, cell_size=20)
    scene.background = "#f8f9fa"

    # Center cell
    center = scene.grid[5, 5]
    center.add_fill(color="#ef4444")

    # Highlight neighbors
    if center.above:
        center.above.add_fill(color="#3b82f6")
    if center.below:
        center.below.add_fill(color="#3b82f6")
    if center.left:
        center.left.add_fill(color="#3b82f6")
    if center.right:
        center.right.add_fill(color="#3b82f6")

    # Diagonal neighbors
    if center.above_left:
        center.above_left.add_fill(color="#10b981")
    if center.above_right:
        center.above_right.add_fill(color="#10b981")
    if center.below_left:
        center.below_left.add_fill(color="#10b981")
    if center.below_right:
        center.below_right.add_fill(color="#10b981")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#d1d5db", width=0.5)

    scene.save(OUTPUT_DIR / "cell-neighbors.svg")

# =============================================================================
# SECTION: Grid Iteration Patterns
# =============================================================================

def pattern_basic_iteration():
    """Basic iteration - add dots to all cells"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid:
        cell.add_dot(color="#6366f1", radius=3)

    scene.save(OUTPUT_DIR / "pattern-basic-iteration.svg")

def pattern_position_logic():
    """Position-based logic - center cross"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid:
        # Center cross pattern
        if cell.row == scene.grid.rows // 2 or cell.col == scene.grid.cols // 2:
            cell.add_dot(color="#3b82f6", radius=5)
        else:
            cell.add_dot(color="#e0e0e0", radius=2)

    scene.save(OUTPUT_DIR / "pattern-position-logic.svg")

def pattern_using_neighbors():
    """Using neighbor access in patterns"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        # Draw only if right neighbor is bright
        if cell.right and cell.right.brightness > 0.7:
            cell.add_dot(color="#ef4444", radius=4)

    scene.save(OUTPUT_DIR / "pattern-using-neighbors.svg")

def pattern_edge_detection():
    """Edge detection pattern"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "#f8f9fa"

    for cell in scene.grid:
        is_edge = (
            cell.row == 0 or
            cell.row == scene.grid.rows - 1 or
            cell.col == 0 or
            cell.col == scene.grid.cols - 1
        )

        if is_edge:
            cell.add_fill(color="#3b82f6")
        else:
            cell.add_dot(color="#94a3b8", radius=2)

    scene.save(OUTPUT_DIR / "pattern-edge-detection.svg")

# =============================================================================
# SECTION: Grid Selection Methods
# =============================================================================

def selection_specific_row():
    """Selecting specific rows"""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=15)
    scene.background = "white"

    # Highlight row 0 (top)
    for cell in scene.grid.row(0):
        cell.add_fill(color="#ef4444")

    # Highlight row 7 (middle)
    for cell in scene.grid.row(7):
        cell.add_fill(color="#3b82f6")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "selection-specific-row.svg")

def selection_specific_column():
    """Selecting specific columns"""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=15)
    scene.background = "white"

    # Highlight columns
    for cell in scene.grid.column(5):
        cell.add_fill(color="#10b981")

    for cell in scene.grid.column(15):
        cell.add_fill(color="#f59e0b")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "selection-specific-column.svg")

def selection_checkerboard():
    """Checkerboard selection pattern"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid.checkerboard("black"):
        cell.add_fill(color="#1f2937")

    scene.save(OUTPUT_DIR / "selection-checkerboard.svg")

def selection_border():
    """Border selection pattern"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid.border(thickness=2):
        cell.add_fill(color="#3b82f6")

    scene.save(OUTPUT_DIR / "selection-border.svg")

def selection_every_nth():
    """Every nth cell selection"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid.every(n=3):
        cell.add_dot(color="#f59e0b", radius=5)

    scene.save(OUTPUT_DIR / "selection-every-nth.svg")

# =============================================================================
# SECTION: Common Patterns
# =============================================================================

def common_pattern_checkerboard():
    """Common pattern: Checkerboard"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color="#1f2937")
        else:
            cell.add_fill(color="#f8f9fa")

    scene.save(OUTPUT_DIR / "common-pattern-checkerboard.svg")

def common_pattern_radial():
    """Common pattern: Radial gradient"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=12)
    scene.background = "white"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        # Distance from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = (dr*dr + dc*dc) ** 0.5

        # Size based on distance
        max_dist = (center_row**2 + center_col**2) ** 0.5
        size = 2 + (1 - distance / max_dist) * 8

        cell.add_dot(radius=size, color="#ec4899")

    scene.save(OUTPUT_DIR / "common-pattern-radial.svg")

def common_pattern_wave():
    """Common pattern: Sinusoidal wave"""
    scene = Scene.with_grid(cols=40, rows=20, cell_size=12)
    scene.background = "white"

    for cell in scene.grid:
        # Sinusoidal wave
        wave = math.sin(cell.col / scene.grid.cols * math.pi * 4)

        # Y position based on wave
        y = 0.5 + wave * 0.3

        cell.add_dot(at=(0.5, y), radius=3, color="#3b82f6")

    scene.save(OUTPUT_DIR / "common-pattern-wave.svg")

# =============================================================================
# SECTION: Rectangular Cells
# =============================================================================

def rect_cells_comparison():
    """Square cells vs rectangular cells comparison"""
    # Left half: square cells (default)
    scene = Scene.with_grid(cols=8, rows=8, cell_size=20)
    scene.background = "#f8f9fa"

    for cell in scene.grid:
        cell.add_dot(radius=3, color="#6366f1")
        cell.add_border(color="#d1d5db", width=0.5)

    scene.save(OUTPUT_DIR / "rect-cells-square.svg")

    # Rectangular cells using cell_width / cell_height
    scene2 = Scene.with_grid(cols=8, rows=8, cell_size=20, cell_width=40, cell_height=20)
    scene2.background = "#f8f9fa"

    for cell in scene2.grid:
        cell.add_dot(radius=3, color="#6366f1")
        cell.add_border(color="#d1d5db", width=0.5)

    scene2.save(OUTPUT_DIR / "rect-cells-wide.svg")

def rect_cells_domino():
    """Domino-style cells (2:1 ratio)"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=15, cell_width=30, cell_height=15)
    scene.background = "#1e1b4b"

    colors = ["#312e81", "#3730a3", "#4338ca", "#4f46e5", "#6366f1"]
    for cell in scene.grid:
        idx = (cell.row + cell.col) % len(colors)
        cell.add_fill(color=colors[idx])
        cell.add_border(color="#1e1b4b", width=0.5)

    scene.save(OUTPUT_DIR / "rect-cells-domino.svg")

# =============================================================================
# SECTION: QoL Features
# =============================================================================

def qol_distance_to():
    """distance_to() visualization - radial gradient effect"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=12)
    scene.background = "#0f172a"

    center_cell = scene.grid[12, 12]

    for cell in scene.grid:
        dist = cell.distance_to(center_cell)
        max_dist = 15  # approximate max
        t = min(dist / max_dist, 1.0)

        # Larger dots near center, smaller far away
        radius = 5 * (1 - t) + 1

        # Color gradient from warm to cool
        r = int(239 * (1 - t) + 59 * t)
        g = int(68 * (1 - t) + 130 * t)
        b = int(68 * (1 - t) + 246 * t)

        cell.add_dot(radius=radius, color=f"rgb({r},{g},{b})")

    scene.save(OUTPUT_DIR / "qol-distance-to.svg")

def qol_normalized_position():
    """normalized_position visualization - smooth gradient"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
    scene.background = "#0f172a"

    for cell in scene.grid:
        nx, ny = cell.normalized_position

        # Map position to color
        r = int(nx * 255)
        g = int(100)
        b = int(ny * 255)

        cell.add_fill(color=f"rgb({r},{g},{b})")

    scene.save(OUTPUT_DIR / "qol-normalized-position.svg")

# =============================================================================
# SECTION: Sub-cell Sampling
# =============================================================================

def subcell_sampling():
    """Sub-cell image sampling - four corner dots per cell"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=15)

    for cell in scene.grid:
        # Sample at four corners within the cell
        corners = [(0.2, 0.2), (0.8, 0.2), (0.2, 0.8), (0.8, 0.8)]
        for rx, ry in corners:
            color = cell.sample_hex(rx, ry)
            cell.add_dot(at=(rx, ry), radius=3, color=color)

    scene.save(OUTPUT_DIR / "subcell-sampling.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Creating grids
    "create-via-from-image": create_via_from_image,
    "create-via-with-grid": create_via_with_grid,
    "create-manual-grid": create_manual_grid,

    # Accessing cells
    "access-by-index": access_by_index,
    "access-iteration": access_iteration,

    # Cell properties
    "cell-position-helpers": cell_position_helpers,
    "cell-named-positions": cell_named_positions,
    "cell-neighbors": cell_neighbors,

    # Iteration patterns
    "pattern-basic-iteration": pattern_basic_iteration,
    "pattern-position-logic": pattern_position_logic,
    "pattern-using-neighbors": pattern_using_neighbors,
    "pattern-edge-detection": pattern_edge_detection,

    # Selection methods
    "selection-specific-row": selection_specific_row,
    "selection-specific-column": selection_specific_column,
    "selection-checkerboard": selection_checkerboard,
    "selection-border": selection_border,
    "selection-every-nth": selection_every_nth,

    # Common patterns
    "common-pattern-checkerboard": common_pattern_checkerboard,
    "common-pattern-radial": common_pattern_radial,
    "common-pattern-wave": common_pattern_wave,

    # Rectangular cells
    "rect-cells-comparison": rect_cells_comparison,
    "rect-cells-domino": rect_cells_domino,

    # QoL features
    "qol-distance-to": qol_distance_to,
    "qol-normalized-position": qol_normalized_position,

    # Sub-cell sampling
    "subcell-sampling": subcell_sampling,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-grids-and-cells.md...")

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
