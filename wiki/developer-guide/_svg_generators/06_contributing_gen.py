#!/usr/bin/env python3
"""
SVG Generator for: developer-guide/06-contributing.md

Generates visual examples for contributing to PyFreeform.

Corresponds to sections:
- Development Setup
- Running Tests
- Code Style
- Areas for Contribution
- Pull Requests
"""

from pathlib import Path
from pyfreeform import Scene, shapes

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "06-contributing"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: Development Workflow Stages
# =============================================================================

def development_workflow():
    """Visual representation of development workflow stages"""
    scene = Scene.with_grid(cols=6, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Each stage with different visual
    # 1. Clone
    cells[0].add_polygon(shapes.square(size=0.7), fill="#3b82f6")
    cells[0].add_border(color="#3b82f6", width=2)

    # 2. Install
    cells[1].add_ellipse(rx=18, ry=18, fill="#10b981")
    cells[1].add_border(color="#10b981", width=2)

    # 3. Changes
    cells[2].add_polygon(shapes.triangle(size=0.7), fill="#f59e0b")
    cells[2].add_border(color="#f59e0b", width=2)

    # 4. Tests
    cells[3].add_polygon(shapes.hexagon(size=0.7), fill="#8b5cf6")
    cells[3].add_border(color="#8b5cf6", width=2)

    # 5. Format
    cells[4].add_polygon(shapes.star(points=5, size=0.7), fill="#ec4899")
    cells[4].add_border(color="#ec4899", width=2)

    # 6. PR
    cells[5].add_dot(radius=15, color="#06b6d4")
    cells[5].add_border(color="#06b6d4", width=2)

    scene.save(OUTPUT_DIR / "01-development-workflow.svg")

# =============================================================================
# SECTION: Code Quality Tools
# =============================================================================

def code_quality_tools():
    """Visual representation of code quality tools"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=140)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # Black - Formatting
    cells[0].add_ellipse(rx=30, ry=30, fill="#1f2937", stroke="#1f2937", stroke_width=2)
    cells[0].add_dot(radius=12, color="#1f2937")
    cells[0].add_border(color="#e5e7eb", width=1)

    # MyPy - Type Checking
    cells[1].add_polygon(shapes.hexagon(size=0.7), fill="#3b82f6", stroke="#3b82f6", stroke_width=2)
    cells[1].add_polygon(shapes.hexagon(size=0.4), fill="#3b82f6")
    cells[1].add_border(color="#e5e7eb", width=1)

    # Pytest - Testing
    cells[2].add_polygon(shapes.triangle(size=0.7), fill="#10b981", stroke="#10b981", stroke_width=2)
    cells[2].add_polygon(shapes.triangle(size=0.4), fill="#10b981")
    cells[2].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "02-code-quality-tools.svg")

# =============================================================================
# SECTION: Contribution Areas
# =============================================================================

def contribution_areas():
    """Visual representation of areas for contribution"""
    scene = Scene.with_grid(cols=3, rows=2, cell_size=120)
    scene.background = "#f8f9fa"

    areas = [
        {"pos": (0, 0), "color": "#3b82f6", "shape": "dot"},
        {"pos": (0, 1), "color": "#10b981", "shape": "triangle"},
        {"pos": (0, 2), "color": "#f59e0b", "shape": "hexagon"},
        {"pos": (1, 0), "color": "#8b5cf6", "shape": "star"},
        {"pos": (1, 1), "color": "#ec4899", "shape": "square"},
        {"pos": (1, 2), "color": "#06b6d4", "shape": "ellipse"},
    ]

    for area in areas:
        row, col = area["pos"]
        cell = scene.grid[row, col]
        cell.add_border(color="#e5e7eb", width=1)

        # Different shape for each area
        if area["shape"] == "dot":
            cell.add_dot(radius=20, color=area["color"])
        elif area["shape"] == "triangle":
            cell.add_polygon(shapes.triangle(size=0.7), fill=area["color"])
        elif area["shape"] == "hexagon":
            cell.add_polygon(shapes.hexagon(size=0.7), fill=area["color"])
        elif area["shape"] == "star":
            cell.add_polygon(shapes.star(points=5, size=0.7), fill=area["color"])
        elif area["shape"] == "square":
            cell.add_polygon(shapes.square(size=0.7), fill=area["color"])
        elif area["shape"] == "ellipse":
            cell.add_ellipse(rx=22, ry=22, fill=area["color"])

    scene.save(OUTPUT_DIR / "03-contribution-areas.svg")

# =============================================================================
# SECTION: Pull Request Process
# =============================================================================

def pull_request_process():
    """Visual representation of PR process"""
    scene = Scene.with_grid(cols=1, rows=7, cell_size=80)
    scene.background = "#ffffff"

    # Show progression with increasing complexity
    for i, cell in enumerate(scene.grid):
        # Add elements progressively
        if i >= 0:
            cell.add_dot(at=(0.3, 0.5), radius=5, color="#3b82f6")
        if i >= 1:
            cell.add_dot(at=(0.5, 0.5), radius=5, color="#10b981")
        if i >= 2:
            cell.add_dot(at=(0.7, 0.5), radius=5, color="#f59e0b")
        if i >= 3:
            cell.add_line(start=(0.3, 0.5), end=(0.5, 0.5), width=2, color="#cbd5e1")
        if i >= 4:
            cell.add_line(start=(0.5, 0.5), end=(0.7, 0.5), width=2, color="#cbd5e1")
        if i >= 5:
            cell.add_ellipse(rx=30, ry=15, fill="none", stroke="#8b5cf6", stroke_width=2)
        if i >= 6:
            cell.add_ellipse(rx=35, ry=20, fill="none", stroke="#ec4899", stroke_width=2)

        cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "04-pull-request-process.svg")

# =============================================================================
# SECTION: Testing Pyramid
# =============================================================================

def testing_pyramid():
    """Visual representation of testing approach"""
    scene = Scene.with_grid(cols=3, rows=3, cell_size=90)
    scene.background = "#ffffff"

    # Create pyramid shape
    # Top row: 1 cell (integration)
    scene.grid[0, 1].add_polygon(shapes.triangle(size=0.7), fill="#3b82f6")
    scene.grid[0, 1].add_border(color="#e5e7eb", width=1)

    # Middle row: 2 cells (component)
    scene.grid[1, 0].add_polygon(shapes.square(size=0.7), fill="#10b981")
    scene.grid[1, 1].add_polygon(shapes.square(size=0.7), fill="#10b981")
    scene.grid[1, 0].add_border(color="#e5e7eb", width=1)
    scene.grid[1, 1].add_border(color="#e5e7eb", width=1)

    # Bottom row: 3 cells (unit)
    for col in range(3):
        scene.grid[2, col].add_polygon(shapes.square(size=0.7), fill="#f59e0b")
        scene.grid[2, col].add_border(color="#e5e7eb", width=1)

    # Other cells empty with borders
    scene.grid[0, 0].add_border(color="#e5e7eb", width=1)
    scene.grid[0, 2].add_border(color="#e5e7eb", width=1)
    scene.grid[1, 2].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "05-testing-pyramid.svg")

# =============================================================================
# SECTION: Git Branching
# =============================================================================

def git_branch_strategy():
    """Visual representation of git branching strategy"""
    scene = Scene.with_grid(cols=5, rows=3, cell_size=80)
    scene.background = "#f8f9fa"

    # Main branch (middle row)
    for col in range(5):
        scene.grid[1, col].add_dot(radius=8, color="#1f2937")
        if col < 4:
            scene.grid[1, col].add_line(start=(0.5, 0.5), end=(1.5, 0.5), width=2, color="#1f2937")

    # Feature branch (top row, branch off and merge)
    scene.grid[0, 1].add_dot(radius=6, color="#3b82f6")
    scene.grid[0, 2].add_dot(radius=6, color="#3b82f6")
    scene.grid[0, 3].add_dot(radius=6, color="#3b82f6")

    # Connection lines for feature branch
    scene.grid[0, 1].add_line(start=(0.5, 1), end=(0.5, 0.5), width=1.5, color="#3b82f6")
    scene.grid[0, 1].add_line(start=(0.5, 0.5), end=(1.5, 0.5), width=1.5, color="#3b82f6")
    scene.grid[0, 2].add_line(start=(0.5, 0.5), end=(1.5, 0.5), width=1.5, color="#3b82f6")
    scene.grid[0, 3].add_line(start=(0.5, 0.5), end=(0.5, 1), width=1.5, color="#3b82f6")

    # Grid borders
    for cell in scene.grid:
        cell.add_border(color="#e5e7eb", width=0.5)

    scene.save(OUTPUT_DIR / "06-git-branch-strategy.svg")

# =============================================================================
# SECTION: Code Style (Good vs Bad)
# =============================================================================

def code_style_guidelines():
    """Visual representation of code style guidelines"""
    scene = Scene.with_grid(cols=2, rows=3, cell_size=120)
    scene.background = "#ffffff"

    # Good examples (left column)
    scene.grid[0, 0].add_polygon(shapes.hexagon(size=0.7), fill="#10b981", stroke="#10b981", stroke_width=2)
    scene.grid[1, 0].add_polygon(shapes.star(points=5, size=0.7), fill="#10b981", stroke="#10b981", stroke_width=2)
    scene.grid[2, 0].add_ellipse(rx=25, ry=25, fill="#10b981", stroke="#10b981", stroke_width=2)

    # Bad examples (right column) - less structured
    scene.grid[0, 1].add_polygon(shapes.triangle(size=0.7), fill="#ef4444", stroke="#ef4444", stroke_width=1)
    scene.grid[1, 1].add_dot(radius=20, color="#ef4444")
    scene.grid[2, 1].add_polygon(shapes.square(size=0.7), fill="#ef4444", stroke="#ef4444", stroke_width=1)

    # Borders
    for cell in scene.grid:
        cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "07-code-style-guidelines.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-development-workflow": development_workflow,
    "02-code-quality-tools": code_quality_tools,
    "03-contribution-areas": contribution_areas,
    "04-pull-request-process": pull_request_process,
    "05-testing-pyramid": testing_pyramid,
    "06-git-branch-strategy": git_branch_strategy,
    "07-code-style-guidelines": code_style_guidelines,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 06-contributing.md...")

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
