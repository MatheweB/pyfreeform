#!/usr/bin/env python3
"""
SVG Generator for: developer-guide/03-creating-entities.md

Generates visual examples for creating custom entities.

Corresponds to sections:
- Minimal Entity
- Usage
"""

from pathlib import Path
import math
from pyfreeform import Scene, shapes, Color
from pyfreeform.core.entity import Entity
from pyfreeform.core.point import Point

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-creating-entities"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: Custom Entity - Star Implementation
# =============================================================================

class Star(Entity):
    """5-pointed star entity (complete implementation)"""

    def __init__(self, x, y, size=20, color="gold", z_index=0):
        super().__init__(x, y, z_index)
        self.size = size
        self._color = Color(color)

    @property
    def anchor_names(self) -> list[str]:
        return ["center"] + [f"point{i}" for i in range(5)]

    def anchor(self, name: str) -> Point:
        if name == "center":
            return self.position

        # Calculate star points
        if name.startswith("point"):
            try:
                point_num = int(name[5:])
                if 0 <= point_num < 5:
                    angle = (point_num * 72 - 90) * math.pi / 180
                    x = self.x + self.size * math.cos(angle)
                    y = self.y + self.size * math.sin(angle)
                    return Point(x, y)
            except (ValueError, IndexError):
                pass

        raise ValueError(f"Unknown anchor: {name}")

    def bounds(self) -> tuple[float, float, float, float]:
        return (
            self.x - self.size,
            self.y - self.size,
            self.x + self.size,
            self.y + self.size
        )

    def to_svg(self) -> str:
        # Generate star path
        points = []
        for i in range(5):
            # Outer point
            outer_angle = (i * 72 - 90) * math.pi / 180
            outer_x = self.x + self.size * math.cos(outer_angle)
            outer_y = self.y + self.size * math.sin(outer_angle)
            points.append(f"{outer_x},{outer_y}")

            # Inner point
            inner_angle = ((i * 72 + 36) - 90) * math.pi / 180
            inner_x = self.x + (self.size * 0.4) * math.cos(inner_angle)
            inner_y = self.y + (self.size * 0.4) * math.sin(inner_angle)
            points.append(f"{inner_x},{inner_y}")

        path = f'<polygon points="{" ".join(points)}" fill="{self._color.to_hex()}" />'
        return path

def custom_star_entity():
    """Show custom Star entity"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Different sizes of stars
    star1 = Star(cells[0].center[0], cells[0].center[1], size=18, color="gold")
    scene.add(star1)

    star2 = Star(cells[1].center[0], cells[1].center[1], size=24, color="#f59e0b")
    scene.add(star2)

    star3 = Star(cells[2].center[0], cells[2].center[1], size=30, color="#fbbf24")
    scene.add(star3)

    star4 = Star(cells[3].center[0], cells[3].center[1], size=36, color="#fde68a")
    scene.add(star4)

    # Grid
    for cell in cells:
        cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "01-custom-star-entity.svg")

# =============================================================================
# SECTION: Star Entity Anchors
# =============================================================================

def star_entity_anchors():
    """Show star entity anchor points"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Create star
    star = Star(cell.center[0], cell.center[1], size=60, color="gold")
    scene.add(star)

    # Show anchor points with small dots
    # Center
    cell.add_dot(at=star.anchor("center"), radius=4, color="#ef4444")

    # Point anchors
    for i in range(5):
        anchor_point = star.anchor(f"point{i}")
        cell.add_dot(at=anchor_point, radius=3, color="#3b82f6")

    scene.save(OUTPUT_DIR / "02-star-entity-anchors.svg")

# =============================================================================
# SECTION: Using Custom Entity in Grid
# =============================================================================

def using_custom_entity():
    """Show usage of custom entity in a grid"""
    scene = Scene.with_grid(cols=5, rows=4, cell_size=70)
    scene.background = "#f8f9fa"

    # Create stars in a pattern
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            size = 12 + ((cell.row * 5 + cell.col) % 3) * 4
            colors = ["gold", "#f59e0b", "#fbbf24"]
            color = colors[(cell.row + cell.col) % 3]
            star = Star(cell.center[0], cell.center[1], size=size, color=color)
            scene.add(star)
        else:
            cell.add_dot(radius=6, color="#cbd5e1")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e5e7eb", width=0.5)

    scene.save(OUTPUT_DIR / "03-using-custom-entity.svg")

# =============================================================================
# SECTION: Custom Entity with Transformations
# =============================================================================

def custom_entity_transformations():
    """Show transformations on custom entity"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # Original
    star1 = Star(cells[0].center[0], cells[0].center[1], size=28, color="gold")
    scene.add(star1)
    cells[0].add_border(color="#e5e7eb", width=1)

    # Rotated
    star2 = Star(cells[1].center[0], cells[1].center[1], size=28, color="gold")
    star2.rotate(36)
    scene.add(star2)
    cells[1].add_border(color="#e5e7eb", width=1)

    # Scaled
    star3 = Star(cells[2].center[0], cells[2].center[1], size=28, color="gold")
    star3.scale(1.4)
    scene.add(star3)
    cells[2].add_border(color="#e5e7eb", width=1)

    # Combined
    star4 = Star(cells[3].center[0], cells[3].center[1], size=28, color="gold")
    star4.rotate(18)
    star4.scale(0.8)
    scene.add(star4)
    cells[3].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "04-custom-entity-transformations.svg")

# =============================================================================
# SECTION: Comparing Built-in vs Custom Entities
# =============================================================================

def builtin_vs_custom():
    """Compare built-in and custom entities"""
    scene = Scene.with_grid(cols=4, rows=2, cell_size=90)
    scene.background = "#f8f9fa"

    # Row 1: Built-in entities
    scene.grid[0, 0].add_dot(radius=15, color="#3b82f6")
    scene.grid[0, 1].add_polygon(shapes.triangle(size=0.7), fill="#10b981")
    scene.grid[0, 2].add_ellipse(rx=18, ry=18, fill="#f59e0b")
    scene.grid[0, 3].add_polygon(shapes.hexagon(size=0.7), fill="#8b5cf6")

    # Row 2: Custom star entities
    for col in range(4):
        cell = scene.grid[1, col]
        star = Star(cell.center[0], cell.center[1], size=20, color=["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"][col])
        scene.add(star)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "05-builtin-vs-custom.svg")

# =============================================================================
# SECTION: Implementation Requirements
# =============================================================================

def implementation_requirements():
    """Show what needs to be implemented"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=90)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # 1. __init__
    cells[0].add_ellipse(rx=20, ry=20, fill="#3b82f6", stroke="#3b82f6", stroke_width=2)
    cells[0].add_border(color="#e5e7eb", width=1)

    # 2. anchor_names
    cells[1].add_dot(radius=8, color="#10b981")
    cells[1].add_dot(at=(0.3, 0.3), radius=3, color="#10b981")
    cells[1].add_dot(at=(0.7, 0.3), radius=3, color="#10b981")
    cells[1].add_dot(at=(0.3, 0.7), radius=3, color="#10b981")
    cells[1].add_dot(at=(0.7, 0.7), radius=3, color="#10b981")
    cells[1].add_border(color="#e5e7eb", width=1)

    # 3. anchor()
    poly = cells[2].add_polygon(shapes.hexagon(size=0.7), fill="#f59e0b")
    cells[2].add_dot(at="center", radius=4, color="#f59e0b")
    cells[2].add_border(color="#e5e7eb", width=1)

    # 4. bounds()
    cells[3].add_polygon(shapes.star(points=5, size=0.7), fill="#8b5cf6")
    cells[3].add_polygon(shapes.square(size=0.85), fill="none", stroke="#ef4444", stroke_width=1)
    cells[3].add_border(color="#e5e7eb", width=1)

    # 5. to_svg()
    star = Star(cells[4].center[0], cells[4].center[1], size=20, color="#ec4899")
    scene.add(star)
    cells[4].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "06-implementation-requirements.svg")

# =============================================================================
# SECTION: Entity Integration
# =============================================================================

def entity_integration():
    """Custom entity integrated with built-in entities"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=250)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Mix custom stars with built-in entities
    # Stars
    star1 = Star(cell.center[0], cell.center[1] - 40, size=25, color="gold")
    star2 = Star(cell.center[0] - 60, cell.center[1] + 30, size=18, color="#f59e0b")
    star3 = Star(cell.center[0] + 60, cell.center[1] + 30, size=18, color="#fbbf24")
    scene.add(star1)
    scene.add(star2)
    scene.add(star3)

    # Built-in entities
    cell.add_ellipse(rx=80, ry=80, fill="none", stroke="#cbd5e1", stroke_width=2)
    cell.add_dot(at=(0.3, 0.3), radius=8, color="#3b82f6")
    cell.add_dot(at=(0.7, 0.3), radius=8, color="#10b981")

    scene.save(OUTPUT_DIR / "07-entity-integration.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-custom-star-entity": custom_star_entity,
    "02-star-entity-anchors": star_entity_anchors,
    "03-using-custom-entity": using_custom_entity,
    "04-custom-entity-transformations": custom_entity_transformations,
    "05-builtin-vs-custom": builtin_vs_custom,
    "06-implementation-requirements": implementation_requirements,
    "07-entity-integration": entity_integration,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-creating-entities.md...")

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
