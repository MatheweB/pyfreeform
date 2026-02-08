#!/usr/bin/env python3
"""
SVG Generator for: developer-guide/01-architecture.md

Generates visual examples for PyFreeform's architecture overview.

Corresponds to sections:
- Package Structure
- Key Design Patterns
"""

from pyfreeform import Scene, Grid, Text, Dot, Line, Ellipse, Polygon
from pyfreeform.core.entity import Entity
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-architecture"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: Entity-Component Pattern Example
# =============================================================================

def design_pattern_entity_component():
    """Entity-Component pattern visualization using actual entities"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Show different entity types - all inherit from Entity base
    cells[0].add_dot(radius=12, color="#ef4444")
    cells[1].add_line(start="top_left", end="bottom_right", width=3, color="#10b981")
    cells[2].add_curve(start="left", end="right", curvature=0.5, width=2, color="#8b5cf6")
    cells[3].add_ellipse(rx=15, ry=15, fill="#f59e0b")
    cells[4].add_polygon(Polygon.hexagon(size=0.7), fill="#3b82f6")

    # Add borders
    for cell in cells:
        cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "01-entity-component-pattern.svg")

# =============================================================================
# SECTION: Builder Pattern Example
# =============================================================================

def design_pattern_builder():
    """Builder pattern visualization - method chaining"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # Show progression: create -> configure -> transform
    # Step 1: Create
    cells[0].add_dot(radius=8, color="#3b82f6")
    cells[0].add_border(color="#cbd5e1", width=1)

    # Step 2: Configure (add more)
    cells[1].add_dot(radius=8, color="#3b82f6")
    cells[1].add_ellipse(rx=15, ry=15, fill="none", stroke="#10b981", stroke_width=2)
    cells[1].add_border(color="#cbd5e1", width=1)

    # Step 3: Transform (scale up)
    dot = cells[2].add_dot(radius=8, color="#3b82f6")
    dot.scale(1.5)
    ell = cells[2].add_ellipse(rx=15, ry=15, fill="none", stroke="#10b981", stroke_width=2)
    ell.scale(1.5)
    cells[2].add_border(color="#cbd5e1", width=1)

    scene.save(OUTPUT_DIR / "02-builder-pattern.svg")

# =============================================================================
# SECTION: Protocol-Based Design (Pathable)
# =============================================================================

def design_pattern_protocol():
    """Protocol-based design - all work with along="""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Line - pathable
    cell1 = scene.grid[0, 0]
    line = cell1.add_line(start="left", end="right", color="#3b82f6", width=2)
    for t in [0.0, 0.5, 1.0]:
        cell1.add_dot(along=line, t=t, radius=4, color="#ef4444")
    cell1.add_border(color="#e5e7eb", width=1)

    # Curve - pathable
    cell2 = scene.grid[0, 1]
    curve = cell2.add_curve(start="left", end="right", curvature=0.5, color="#3b82f6", width=2)
    for t in [0.0, 0.5, 1.0]:
        cell2.add_dot(along=curve, t=t, radius=4, color="#ef4444")
    cell2.add_border(color="#e5e7eb", width=1)

    # Ellipse - pathable
    cell3 = scene.grid[0, 2]
    ellipse = cell3.add_ellipse(rx=35, ry=25, fill="#3b82f6")
    for t in [0.0, 0.5, 1.0]:
        cell3.add_dot(along=ellipse, t=t, radius=4, color="#ef4444")
    cell3.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "03-protocol-pattern.svg")

# =============================================================================
# SECTION: Immutable Point Pattern
# =============================================================================

def design_pattern_immutable_point():
    """Immutable Point - safe coordinates"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # Show points as dots
    for i, cell in enumerate(cells):
        # Multiple entities can share point references safely
        cell.add_dot(at=(0.5, 0.3), radius=5, color="#3b82f6")
        cell.add_dot(at=(0.5, 0.7), radius=5, color="#10b981")

        # Connect them
        cell.add_line(start=(0.5, 0.3), end=(0.5, 0.7), width=2, color="#cbd5e1")

        cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "04-immutable-point.svg")

# =============================================================================
# SECTION: Architecture Layering
# =============================================================================

def architecture_layering():
    """Show layering from data to output"""
    scene = Scene.with_grid(cols=1, rows=5, cell_size=100)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Layer 1: Data/Image (simple gradient pattern)
    for i in range(5):
        cells[0].add_dot(at=(0.2 + i*0.15, 0.5), radius=2 + i, color="#ef4444")

    # Layer 2: Grid (show structure)
    cells[1].add_border(color="#f59e0b", width=2)
    for i in range(3):
        for j in range(3):
            x = 0.25 + j * 0.25
            y = 0.25 + i * 0.25
            cells[1].add_dot(at=(x, y), radius=2, color="#f59e0b")

    # Layer 3: Cell builders (show positioned elements)
    cells[2].add_ellipse(rx=20, ry=20, fill="#10b981")
    cells[2].add_dot(radius=8, color="#10b981")

    # Layer 4: Entities (show variety)
    cells[3].add_polygon(Polygon.star(points=5, size=0.7), fill="#3b82f6")

    # Layer 5: SVG output (final composition)
    cells[4].add_curve(start="left", end="right", curvature=0.5, width=3, color="#8b5cf6")
    cells[4].add_dot(at=(0.25, 0.5), radius=6, color="#8b5cf6")
    cells[4].add_dot(at=(0.75, 0.5), radius=6, color="#8b5cf6")

    # Add borders to all
    for cell in cells:
        if cell != cells[1]:  # Already has border
            cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "05-architecture-layering.svg")

# =============================================================================
# SECTION: Component Composition
# =============================================================================

def component_composition():
    """Show how components compose"""
    scene = Scene.with_grid(cols=4, rows=4, cell_size=60)
    scene.background = "#ffffff"

    # Create a pattern showing composition
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            # Primary entities
            cell.add_dot(radius=5, color="#3b82f6")
        else:
            # Composed entities (multiple elements)
            cell.add_ellipse(rx=12, ry=12, fill="none", stroke="#10b981", stroke_width=1.5)
            cell.add_dot(radius=3, color="#10b981")

        cell.add_border(color="#f3f4f6", width=0.5)

    scene.save(OUTPUT_DIR / "06-component-composition.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-entity-component-pattern": design_pattern_entity_component,
    "02-builder-pattern": design_pattern_builder,
    "03-protocol-pattern": design_pattern_protocol,
    "04-immutable-point": design_pattern_immutable_point,
    "05-architecture-layering": architecture_layering,
    "06-component-composition": component_composition,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-architecture.md...")

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
