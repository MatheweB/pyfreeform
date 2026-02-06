#!/usr/bin/env python3
"""
SVG Generator for: api-reference/grid.md

Generates visual examples demonstrating Grid API methods and iteration patterns.
"""

from pyfreeform import Scene, Palette, shapes
from pathlib import Path


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "grid"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Simple Iteration
# =============================================================================

def example1_simple_iteration():
    """for cell in grid - Simple iteration pattern"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.ocean()

    # Iterate through all cells
    for cell in scene.grid:
        cell.add_dot(radius=5, color=colors.primary)

    scene.save(OUTPUT_DIR / "example1-simple-iteration.svg")


# =============================================================================
# Index Access
# =============================================================================

def example2_index_access():
    """grid[row, col] - Direct cell access"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    # Access specific cells
    scene.grid[0, 0].add_dot(radius=10, color="#ee4266")  # Top-left
    scene.grid[3, 5].add_dot(radius=10, color="#4ecca3")  # Middle
    scene.grid[7, 9].add_dot(radius=10, color="#ffd23f")  # Bottom-right (rows-1, cols-1)

    # Show all cells with borders
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.5)

    scene.save(OUTPUT_DIR / "example2-index-access.svg")


# =============================================================================
# Row Access
# =============================================================================

def example3_row_access():
    """grid.row(n) - Access entire rows"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.ocean()

    # Highlight specific rows
    for cell in scene.grid.row(0):
        cell.add_fill(color=colors.primary, z_index=0)

    for cell in scene.grid.row(3):
        cell.add_fill(color=colors.secondary, z_index=0)

    for cell in scene.grid.row(7):  # Last row (rows-1)
        cell.add_fill(color=colors.accent, z_index=0)

    scene.save(OUTPUT_DIR / "example3-row-access.svg")


# =============================================================================
# Column Access
# =============================================================================

def example4_column_access():
    """grid.column(n) - Access entire columns"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    # Highlight specific columns
    for cell in scene.grid.column(0):
        cell.add_fill(color=colors.primary, z_index=0)

    for cell in scene.grid.column(5):
        cell.add_fill(color=colors.secondary, z_index=0)

    for cell in scene.grid.column(9):  # Last column (cols-1)
        cell.add_fill(color=colors.accent, z_index=0)

    scene.save(OUTPUT_DIR / "example4-column-access.svg")


# =============================================================================
# where() - Conditional Selection
# =============================================================================

def example5_where():
    """grid.where() - Filter cells by condition"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.ocean()

    # Calculate distance from center
    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    # Select cells close to center
    close_cells = scene.grid.where(
        lambda c: ((c.row - center_row)**2 + (c.col - center_col)**2) ** 0.5 < 3
    )

    # Highlight selected cells
    for cell in close_cells:
        cell.add_fill(color=colors.primary, z_index=0)
        cell.add_dot(radius=6, color=colors.accent, z_index=5)

    scene.save(OUTPUT_DIR / "example5-where.svg")


# =============================================================================
# border() - Edge Cells
# =============================================================================

def example6_border():
    """grid.border() - Get all edge cells"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    # Highlight border cells
    for cell in scene.grid.border():
        cell.add_fill(color=colors.primary, z_index=0)
        cell.add_border(color=colors.accent, width=2, z_index=10)

    scene.save(OUTPUT_DIR / "example6-border.svg")


# =============================================================================
# checkerboard() - Checkerboard Pattern
# =============================================================================

def example7_checkerboard():
    """grid.checkerboard() - Alternating pattern"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.ocean()

    # Checkerboard pattern
    for cell in scene.grid.where(lambda cell: (cell.row + cell.col + 0) % 2 == 0):
        cell.add_fill(color=colors.primary, z_index=0)

    for cell in scene.grid.where(lambda cell: (cell.row + cell.col + 1) % 2 == 0):
        cell.add_fill(color=colors.secondary, z_index=0)

    scene.save(OUTPUT_DIR / "example7-checkerboard.svg")


# =============================================================================
# corners() - Corner Cells
# =============================================================================

def example8_corners():
    """Accessing corner cells - Get four corner cells"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.5)

    # Highlight corners
    grid = scene.grid
    corners = [
        grid[0, 0],                           # top-left
        grid[0, grid.cols - 1],              # top-right
        grid[grid.rows - 1, 0],              # bottom-left
        grid[grid.rows - 1, grid.cols - 1]   # bottom-right
    ]
    for cell in corners:
        cell.add_polygon(shapes.star(5), fill=colors.accent, z_index=5)

    scene.save(OUTPUT_DIR / "example8-corners.svg")


# =============================================================================
# Row-by-Row Processing
# =============================================================================

def example9_row_by_row():
    """Process grid row by row with different colors"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")

    # Different color for each row
    row_colors = ["#ee4266", "#4ecca3", "#ffd23f", "#64ffda", "#9b59b6", "#e67e22", "#3498db", "#e74c3c"]

    for row_idx in range(scene.grid.rows):
        color = row_colors[row_idx % len(row_colors)]
        for cell in scene.grid.row(row_idx):
            cell.add_dot(radius=6, color=color)

    scene.save(OUTPUT_DIR / "example9-row-by-row.svg")


# =============================================================================
# Distance from Center Pattern
# =============================================================================

def example10_distance_pattern():
    """Create pattern based on distance from center"""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=30, background="#1a1a2e")
    colors = Palette.ocean()

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        # Calculate distance
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = (dr*dr + dc*dc) ** 0.5

        # Size based on distance
        max_distance = 8
        if distance < max_distance:
            radius = 2 + (max_distance - distance) * 1.2
            cell.add_dot(radius=radius, color=colors.primary)

    scene.save(OUTPUT_DIR / "example10-distance-pattern.svg")


# =============================================================================
# Grid Properties
# =============================================================================

def example11_properties():
    """Grid properties - rows, cols, dimensions"""
    scene = Scene.with_grid(cols=12, rows=8, cell_size=35, background="#1a1a2e")
    colors = Palette.midnight()

    # Show grid structure
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.5)

    # Add labels showing properties
    from pyfreeform import Text
    info = Text(
        x=scene.width // 2,
        y=20,
        content=f"Grid: {scene.grid.rows} rows × {scene.grid.cols} cols",
        font_size=14,
        color=colors.accent,
        text_anchor="middle"
    )
    scene.add(info)

    scene.save(OUTPUT_DIR / "example11-properties.svg")


# =============================================================================
# merge() - Cell Merging
# =============================================================================

def example12_merge():
    """grid.merge() - Merge cells into a virtual surface"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#0f172a")
    colors = Palette.ocean()

    # Show all cells
    for cell in scene.grid:
        cell.add_border(color="#1e293b", width=0.5)

    # Merge a 3x4 region into a single surface
    group = scene.grid.merge(row_start=2, row_end=5, col_start=3, col_end=7)
    group.add_fill(color=colors.primary, opacity=0.3)
    group.add_border(color=colors.accent, width=2)
    group.add_text("Merged Region", at="center", font_size=14, color="white")

    scene.save(OUTPUT_DIR / "example12-merge.svg")


def example13_merge_row():
    """grid.merge_row() - Merge a full row into a header"""
    scene = Scene.with_grid(cols=12, rows=8, cell_size=35, background="#0f172a")
    colors = Palette.midnight()

    # Regular cells
    for cell in scene.grid:
        if cell.row > 1:
            cell.add_dot(radius=4, color=colors.primary, opacity=0.5)

    # Merge top two rows into a header
    header = scene.grid.merge(row_start=0, row_end=2)
    header.add_fill(color="#1e293b")
    header.add_text("Title Bar", at="center", font_size=16, color=colors.accent)

    scene.save(OUTPUT_DIR / "example13-merge-row.svg")


def example14_merge_col():
    """grid.merge_col() - Merge a full column into a sidebar"""
    scene = Scene.with_grid(cols=12, rows=8, cell_size=35, background="#0f172a")
    colors = Palette.ocean()

    # Regular cells
    for cell in scene.grid:
        if cell.col > 1:
            cell.add_dot(radius=3, color=colors.primary, opacity=0.4)

    # Merge left two columns into a sidebar
    sidebar = scene.grid.merge(col_start=0, col_end=2)
    sidebar.add_fill(color="#1e293b")
    sidebar.add_text("Sidebar", at="center", font_size=12, color=colors.accent,
                     rotation=-90)

    scene.save(OUTPUT_DIR / "example14-merge-col.svg")


# =============================================================================
# Complete Example: Combined Selections
# =============================================================================

def example15_combined():
    """Combine multiple grid selection methods"""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=30, background="#1a1a2e")
    colors = Palette.ocean()

    # Border cells
    for cell in scene.grid.border():
        cell.add_border(color=colors.accent, width=2, z_index=10)

    # Checkerboard in interior
    interior = scene.grid.where(lambda c: c.row > 0 and c.row < 11 and c.col > 0 and c.col < 14)
    for cell in interior:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, z_index=0)

    # Highlight corners
    grid = scene.grid
    corners = [
        grid[0, 0],                           # top-left
        grid[0, grid.cols - 1],              # top-right
        grid[grid.rows - 1, 0],              # bottom-left
        grid[grid.rows - 1, grid.cols - 1]   # bottom-right
    ]
    for cell in corners:
        cell.add_polygon(shapes.star(5), fill="#ffd23f", z_index=15)

    scene.save(OUTPUT_DIR / "example15-combined.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-simple-iteration": example1_simple_iteration,
    "example2-index-access": example2_index_access,
    "example3-row-access": example3_row_access,
    "example4-column-access": example4_column_access,
    "example5-where": example5_where,
    "example6-border": example6_border,
    "example7-checkerboard": example7_checkerboard,
    "example8-corners": example8_corners,
    "example9-row-by-row": example9_row_by_row,
    "example10-distance-pattern": example10_distance_pattern,
    "example11-properties": example11_properties,
    "example12-merge": example12_merge,
    "example13-merge-row": example13_merge_row,
    "example14-merge-col": example14_merge_col,
    "example15-combined": example15_combined,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for grid.md...")

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
