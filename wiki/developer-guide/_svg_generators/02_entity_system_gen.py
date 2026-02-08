#!/usr/bin/env python3
"""
SVG Generator for: developer-guide/02-entity-system.md

Generates visual examples for the entity system internals.

Corresponds to sections:
- Entity Base Class
- Entity Lifecycle
"""

from pyfreeform import Scene, Polygon
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-entity-system"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: Entity Properties Visualization
# =============================================================================

def entity_properties_visual():
    """Visual representation of entity properties"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # Position property
    cells[0].add_dot(at=(0.6, 0.4), radius=12, color="#3b82f6")
    cells[0].add_dot(at="center", radius=3, color="#cbd5e1")
    cells[0].add_line(start="center", end=(0.6, 0.4), width=1, color="#cbd5e1")
    cells[0].add_border(color="#e5e7eb", width=1)

    # Z-index property (layering)
    cells[1].add_ellipse(rx=25, ry=25, fill="#10b981", z_index=0)
    cells[1].add_dot(radius=12, color="#3b82f6", z_index=1)
    cells[1].add_border(color="#e5e7eb", width=1)

    # Data property (metadata)
    dot = cells[2].add_dot(radius=12, color="#f59e0b")
    dot.data["category"] = "special"
    cells[2].add_ellipse(rx=20, ry=20, fill="none", stroke="#f59e0b", stroke_width=2)
    cells[2].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "01-entity-properties-visual.svg")

# =============================================================================
# SECTION: Abstract Methods - Anchors
# =============================================================================

def abstract_methods_anchors():
    """Illustration of anchor points on entities"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Dot anchors
    cells[0].add_dot(radius=15, color="#3b82f6")
    cells[0].add_dot(at="top", radius=3, color="#ef4444")
    cells[0].add_dot(at="bottom", radius=3, color="#ef4444")
    cells[0].add_border(color="#e5e7eb", width=1)

    # Line anchors
    line = cells[1].add_line(start="top_left", end="bottom_right", width=2, color="#10b981")
    cells[1].add_dot(along=line, t=0, radius=3, color="#ef4444")
    cells[1].add_dot(along=line, t=0.5, radius=3, color="#ef4444")
    cells[1].add_dot(along=line, t=1, radius=3, color="#ef4444")
    cells[1].add_border(color="#e5e7eb", width=1)

    # Ellipse anchors
    ellipse = cells[2].add_ellipse(rx=25, ry=20, fill="#f59e0b")
    for t in [0, 0.25, 0.5, 0.75]:
        cells[2].add_dot(along=ellipse, t=t, radius=3, color="#ef4444")
    cells[2].add_border(color="#e5e7eb", width=1)

    # Polygon anchors
    poly = cells[3].add_polygon(Polygon.hexagon(size=0.7), fill="#8b5cf6")
    cells[3].add_dot(at="center", radius=3, color="#ef4444")
    cells[3].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "02-abstract-methods-anchors.svg")

# =============================================================================
# SECTION: Entity Lifecycle - Construction to Rendering
# =============================================================================

def entity_lifecycle():
    """Entity lifecycle stages"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # 1. Construction - empty cell
    cells[0].add_border(color="#3b82f6", width=2)

    # 2. Registration - entity added
    cells[1].add_dot(radius=8, color="#10b981")
    cells[1].add_border(color="#10b981", width=2)

    # 3. Transformation - rotated
    rect = cells[2].add_polygon(Polygon.square(size=0.7), fill="#f59e0b")
    rect.rotate(45)
    cells[2].add_border(color="#f59e0b", width=2)

    # 4. Rendering - styled
    cells[3].add_ellipse(rx=15, ry=15, fill="#8b5cf6", stroke="#1f2937", stroke_width=2)
    cells[3].add_border(color="#8b5cf6", width=2)

    # 5. Cleanup - references cleared (show faded)
    cells[4].add_dot(radius=8, color="#cbd5e1")
    cells[4].add_border(color="#cbd5e1", width=2)

    scene.save(OUTPUT_DIR / "03-entity-lifecycle.svg")

# =============================================================================
# SECTION: Transformation Examples
# =============================================================================

def lifecycle_transformation():
    """Transformation stage visualization"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Original
    cells[0].add_polygon(Polygon.square(size=0.7), fill="#3b82f6")
    cells[0].add_border(color="#e5e7eb", width=1)

    # After rotate
    rect2 = cells[1].add_polygon(Polygon.square(size=0.7), fill="#3b82f6")
    rect2.rotate(45)
    cells[1].add_border(color="#e5e7eb", width=1)

    # After scale
    rect3 = cells[2].add_polygon(Polygon.square(size=0.7), fill="#3b82f6")
    rect3.scale(0.6)
    cells[2].add_border(color="#e5e7eb", width=1)

    # Combined
    rect4 = cells[3].add_polygon(Polygon.square(size=0.7), fill="#3b82f6")
    rect4.rotate(30)
    rect4.scale(0.8)
    cells[3].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "04-lifecycle-transformation.svg")

# =============================================================================
# SECTION: Weak References Visualization
# =============================================================================

def weak_references_explanation():
    """Weak references - connections between entities"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Central entity
    center_dot = cell.add_dot(radius=12, color="#3b82f6")

    # Connected entities (simulate weak references)
    positions = [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7)]
    for pos in positions:
        # Connected dot
        cell.add_dot(at=pos, radius=6, color="#10b981")
        # Connection line (dashed to show "weak")
        cell.add_line(start="center", end=pos, width=1, color="#cbd5e1")

    scene.save(OUTPUT_DIR / "05-weak-references-explanation.svg")

# =============================================================================
# SECTION: Bounds Method
# =============================================================================

def bounds_method_visual():
    """Visual representation of bounds() method"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    # Dot with bounds
    cells[0].add_dot(radius=20, color="#3b82f6")
    # Can't actually draw the bounding box, but show the concept with a square
    cells[0].add_polygon(Polygon.square(size=0.7), fill="none", stroke="#ef4444", stroke_width=1)
    cells[0].add_border(color="#e5e7eb", width=1)

    # Ellipse with bounds
    cells[1].add_ellipse(rx=25, ry=18, fill="#10b981")
    cells[1].add_polygon(Polygon.square(size=0.85), fill="none", stroke="#ef4444", stroke_width=1)
    cells[1].add_border(color="#e5e7eb", width=1)

    # Polygon with bounds
    cells[2].add_polygon(Polygon.star(points=5, size=0.6), fill="#f59e0b")
    cells[2].add_polygon(Polygon.square(size=0.75), fill="none", stroke="#ef4444", stroke_width=1)
    cells[2].add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "06-bounds-method-visual.svg")

# =============================================================================
# SECTION: Entity Inheritance Pattern
# =============================================================================

def entity_inheritance_pattern():
    """Show variety of entities (all inherit from Entity)"""
    scene = Scene.with_grid(cols=7, rows=1, cell_size=70)
    scene.background = "#ffffff"

    cells = list(scene.grid)

    # All these inherit from Entity base class
    cells[0].add_dot(radius=10, color="#ef4444")
    cells[1].add_line(start="top_left", end="bottom_right", width=3, color="#f59e0b")
    cells[2].add_curve(start="left", end="right", curvature=0.5, width=2, color="#fbbf24")
    cells[3].add_ellipse(rx=15, ry=15, fill="#10b981")
    cells[4].add_polygon(Polygon.triangle(size=0.7), fill="#3b82f6")
    cells[5].add_polygon(Polygon.hexagon(size=0.7), fill="#8b5cf6")
    cells[6].add_polygon(Polygon.star(points=5, size=0.7), fill="#ec4899")

    for cell in cells:
        cell.add_border(color="#f3f4f6", width=0.5)

    scene.save(OUTPUT_DIR / "07-entity-inheritance-pattern.svg")

# =============================================================================
# SECTION: Opacity
# =============================================================================

def opacity_showcase():
    """Overlapping translucent shapes demonstrating opacity blending"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "#1e1e2e"

    cell = list(scene.grid)[0]

    # Three overlapping translucent circles (RGB light model)
    cell.add_ellipse(at=(0.38, 0.42), rx=55, ry=55, fill="#ff3366", opacity=0.55)
    cell.add_ellipse(at=(0.62, 0.42), rx=55, ry=55, fill="#33cc66", opacity=0.55)
    cell.add_ellipse(at=(0.50, 0.62), rx=55, ry=55, fill="#3388ff", opacity=0.55)

    # Solid-stroke, translucent-fill rect framing the composition
    cell.add_rect(
        width=200, height=140,
        fill="#ffffff", stroke="#ffffff", stroke_width=1,
        fill_opacity=0.06, stroke_opacity=0.25,
    )

    # Scattered dots at varying opacities
    import random
    rng = random.Random(42)
    for _ in range(18):
        x = rng.uniform(0.1, 0.9)
        y = rng.uniform(0.1, 0.9)
        op = rng.uniform(0.15, 0.7)
        cell.add_dot(at=(x, y), radius=rng.uniform(2, 5), color="#ffffff", opacity=op)

    # Label
    cell.add_text("opacity", at=(0.50, 0.12), font_size=14,
                  color="#ffffff", opacity=0.35)

    scene.save(OUTPUT_DIR / "08-opacity-showcase.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-entity-properties-visual": entity_properties_visual,
    "02-abstract-methods-anchors": abstract_methods_anchors,
    "03-entity-lifecycle": entity_lifecycle,
    "04-lifecycle-transformation": lifecycle_transformation,
    "05-weak-references-explanation": weak_references_explanation,
    "06-bounds-method-visual": bounds_method_visual,
    "07-entity-inheritance-pattern": entity_inheritance_pattern,
    "08-opacity-showcase": opacity_showcase,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-entity-system.md...")

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
