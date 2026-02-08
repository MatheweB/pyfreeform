#!/usr/bin/env python3
"""
SVG Generator for: fundamentals/03-entities.md

Generates visual examples for entity types and operations.

Corresponds to sections:
- Entity Types
- Common Entity Behavior
- Creating Entities
- Working with Entities
- Parametric Positioning
- Entity Patterns
"""

from pyfreeform import Scene, Grid, Palette, Dot, Line, Curve, Polygon
from pyfreeform.config import DotStyle
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-entities"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_entities.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Gradient from top-left (bright) to bottom-right (dark)
            brightness = int(255 * (1 - ((x + y) / 800)))
            draw.point((x, y), fill=(brightness, brightness, brightness))

    img.save(temp_file)
    return temp_file

TEST_IMAGE = create_test_image()

# =============================================================================
# SECTION: Entity Types Overview
# =============================================================================

def entity_types_overview():
    """Show all entity types in one scene"""
    scene = Scene.with_grid(cols=7, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Dot
    cells[0].add_dot(radius=10, color="#ef4444")

    # Line
    cells[1].add_line(start="top_left", end="bottom_right", width=3, color="#3b82f6")

    # Curve
    cells[2].add_curve(start="left", end="right", curvature=0.5, width=2, color="#8b5cf6")

    # Ellipse
    cells[3].add_ellipse(rx=20, ry=15, fill="#10b981")

    # Polygon (hexagon)
    cells[4].add_polygon(Polygon.hexagon(), fill="#f59e0b", stroke="none")

    # Text
    cells[5].add_text("Hi", font_size=24, color="#ec4899")

    # Rectangle (using polygon for rectangle shape)
    rect_points = [(-25, -17.5), (25, -17.5), (25, 17.5), (-25, 17.5)]
    cells[6].add_polygon(rect_points, fill="#14b8a6")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01-entity-types-overview.svg")

# =============================================================================
# SECTION: Common Entity Behavior - Position
# =============================================================================

def entity_position():
    """Entity position properties"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Original position (center)
    dot1 = cells[0].add_dot(radius=8, color="#3b82f6")

    # Move to absolute position (top-left)
    dot2 = cells[1].add_dot(radius=8, color="#ef4444")
    dot2.move_to(cells[1].x + 15, cells[1].y + 15)

    # Move by offset (relative)
    dot3 = cells[2].add_dot(radius=8, color="#10b981")
    dot3.move_by(dx=15, dy=10)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "02-entity-position.svg")

# =============================================================================
# SECTION: Movement
# =============================================================================

def entity_movement():
    """Entity movement methods"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = list(scene.grid)[0]

    # Starting position (center)
    start_dot = cell.add_dot(at="center", radius=6, color="#94a3b8", z_index=0)

    # After move_to
    dot1 = cell.add_dot(radius=8, color="#ef4444", z_index=1)
    dot1.move_to(cell.x + 50, cell.y + 50)

    # After move_by from center
    dot2 = cell.add_dot(at="center", radius=8, color="#3b82f6", z_index=1)
    dot2.move_by(dx=40, dy=-30)

    # Show arrows/lines from origin
    cell.add_line(start="center", end=(0.25, 0.25), width=1, color="#94a3b8", z_index=0)
    cell.add_line(start="center", end=(0.7, 0.35), width=1, color="#94a3b8", z_index=0)

    scene.save(OUTPUT_DIR / "03-entity-movement.svg")

# =============================================================================
# SECTION: Transforms - Rotation and Scaling
# =============================================================================

def entity_rotation():
    """Entity rotation"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Create rectangle shape
    rect_points = [(-25, -15), (25, -15), (25, 15), (-25, 15)]

    # 0 degrees
    cells[0].add_polygon(rect_points, fill="#3b82f6", stroke="none")

    # 30 degrees
    rect1 = cells[1].add_polygon(rect_points, fill="#3b82f6", stroke="none")
    rect1.rotate(30)

    # 45 degrees
    rect2 = cells[2].add_polygon(rect_points, fill="#3b82f6", stroke="none")
    rect2.rotate(45)

    # 90 degrees
    rect3 = cells[3].add_polygon(rect_points, fill="#3b82f6", stroke="none")
    rect3.rotate(90)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "04-entity-rotation.svg")

def entity_scaling():
    """Entity scaling"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Original size
    cells[0].add_dot(radius=10, color="#8b5cf6")

    # Scale 0.5 (half size)
    dot1 = cells[1].add_dot(radius=10, color="#8b5cf6")
    dot1.scale(0.5)

    # Scale 1.5
    dot2 = cells[2].add_dot(radius=10, color="#8b5cf6")
    dot2.scale(1.5)

    # Scale 2.0 (double size)
    dot3 = cells[3].add_dot(radius=10, color="#8b5cf6")
    dot3.scale(2.0)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "05-entity-scaling.svg")

# =============================================================================
# SECTION: Layering (Z-Index)
# =============================================================================

def entity_z_index():
    """Z-index layering demonstration"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=120)
    scene.background = "white"

    cells = list(scene.grid)

    # Left: Wrong order (default z-index)
    cells[0].add_ellipse(rx=30, ry=30, fill="#3b82f6", z_index=0)
    cells[0].add_ellipse(rx=20, ry=20, fill="#ef4444", z_index=0)

    # Right: Correct order (with z-index)
    cells[1].add_ellipse(rx=30, ry=30, fill="#3b82f6", z_index=0)
    cells[1].add_ellipse(rx=20, ry=20, fill="#ef4444", z_index=1)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "06-entity-z-index.svg")

# =============================================================================
# SECTION: Creating Entities - Via Cell Methods
# =============================================================================

def create_via_cell_methods():
    """Creating entities via cell methods"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Cell methods handle positioning automatically
        radius = 2 + cell.brightness * 8
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "07-create-via-cell-methods.svg")

# =============================================================================
# SECTION: Creating Entities - Direct Construction
# =============================================================================

def create_direct_construction():
    """Creating entities via direct construction"""
    scene = Scene(width=400, height=300, background="white")

    # Create entities with exact positions
    dot = Dot(x=100, y=100, radius=15, color="coral")
    line = Line(x1=50, y1=50, x2=350, y2=250, color="gray", width=2)
    curve = Curve(x1=100, y1=200, x2=300, y2=200, curvature=0.5, color="purple", width=2)

    # Add to scene (use add method)
    scene.add(dot)
    scene.add(line)
    scene.add(curve)

    scene.save(OUTPUT_DIR / "08-create-direct-construction.svg")

# =============================================================================
# SECTION: Working with Entities - Store References
# =============================================================================

def store_references():
    """Storing entity references for later manipulation"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
    scene.background = "white"

    # Store references
    dots = []
    for cell in scene.grid:
        dot = cell.add_dot(radius=4, color="#3b82f6")
        dots.append(dot)

    # Transform later - scale every 5th dot
    for i, dot in enumerate(dots):
        if i % 5 == 0:
            dot.scale(1.5)
            dot.color = "#ef4444"

    scene.save(OUTPUT_DIR / "09-store-references.svg")

# =============================================================================
# SECTION: Group Entities
# =============================================================================

def group_entities():
    """Grouping entities by criteria"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    bright_dots = []
    dark_dots = []

    for cell in scene.grid:
        dot = cell.add_dot(radius=4, color=cell.color)

        if cell.brightness > 0.5:
            bright_dots.append(dot)
        else:
            dark_dots.append(dot)

    # Bulk operations
    for dot in bright_dots:
        dot.scale(1.3)

    scene.save(OUTPUT_DIR / "10-group-entities.svg")

# =============================================================================
# SECTION: Parametric Positioning
# =============================================================================

def parametric_line():
    """Parametric positioning along a line"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=250)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Create a line
    line = cell.add_line(start="left", end="right", width=2, color="#94a3b8")

    # Position dots along the line
    for i in range(11):
        t = i / 10  # 0.0 to 1.0
        cell.add_dot(along=line, t=t, radius=5, color="#3b82f6")

    scene.save(OUTPUT_DIR / "11-parametric-line.svg")

def parametric_curve():
    """Parametric positioning along a curve"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=250)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Create a curve
    curve = cell.add_curve(start="left", end="right", curvature=0.5, width=2, color="#94a3b8")

    # Position dots along the curve
    for i in range(11):
        t = i / 10
        cell.add_dot(along=curve, t=t, radius=5, color="#8b5cf6")

    scene.save(OUTPUT_DIR / "12-parametric-curve.svg")

def parametric_ellipse():
    """Parametric positioning around an ellipse"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=250)
    scene.background = "white"

    cell = list(scene.grid)[0]

    # Create an ellipse
    ellipse = cell.add_ellipse(rx=80, ry=60, fill="none", stroke="#94a3b8", stroke_width=2)

    # Position dots around the perimeter
    for i in range(12):
        t = i / 12
        cell.add_dot(along=ellipse, t=t, radius=6, color="#10b981")

    scene.save(OUTPUT_DIR / "13-parametric-ellipse.svg")

# =============================================================================
# SECTION: Entity Patterns - Data-Driven Sizing
# =============================================================================

def pattern_data_driven_sizing():
    """Entity pattern: Data-driven sizing"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        # Size based on brightness
        radius = 2 + cell.brightness * 8
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "14-pattern-data-driven-sizing.svg")

# =============================================================================
# SECTION: Entity Patterns - Conditional Types
# =============================================================================

def pattern_conditional_types():
    """Entity pattern: Conditional entity types"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_ellipse(rx=10, ry=8, fill=cell.color)
        elif cell.brightness > 0.4:
            cell.add_curve(start="left", end="right", curvature=0.5, color=cell.color)
        else:
            cell.add_dot(radius=3, color=cell.color)

    scene.save(OUTPUT_DIR / "15-pattern-conditional-types.svg")

# =============================================================================
# SECTION: Entity Patterns - Progressive Transformation
# =============================================================================

def pattern_progressive_transformation():
    """Entity pattern: Progressive transformation"""
    scene = Scene.with_grid(cols=20, rows=10, cell_size=20)
    scene.background = "white"

    dots = []
    for cell in scene.grid:
        dot = cell.add_dot(radius=6, color="#3b82f6")
        dots.append(dot)

    # Apply progressive rotation
    for i, dot in enumerate(dots):
        angle = (i / len(dots)) * 360
        dot.rotate(angle)

    scene.save(OUTPUT_DIR / "16-pattern-progressive-transformation.svg")

# =============================================================================
# SECTION: Entity-Specific Features - Dots
# =============================================================================

def entity_specific_dots():
    """Dot-specific features"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=60)
    scene.background = "white"

    cells = list(scene.grid)

    # Different sizes
    cells[0].add_dot(radius=3, color="coral")
    cells[1].add_dot(radius=6, color="coral")
    cells[2].add_dot(radius=9, color="coral")
    cells[3].add_dot(radius=12, color="coral")
    cells[4].add_dot(radius=15, color="coral")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "17-entity-specific-dots.svg")

# =============================================================================
# SECTION: Entity-Specific Features - Lines
# =============================================================================

def entity_specific_lines():
    """Line-specific features"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Different directions
    cells[0].add_line(start="top_left", end="bottom_right", width=2, color="#3b82f6")
    cells[1].add_line(start="top", end="bottom", width=2, color="#3b82f6")
    cells[2].add_line(start="left", end="right", width=2, color="#3b82f6")

    # Show midpoint with dot
    line = cells[1].add_line(start="left", end="right", width=1, color="#94a3b8", z_index=0)
    cells[1].add_dot(along=line, t=0.5, radius=4, color="#ef4444", z_index=1)

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "18-entity-specific-lines.svg")

# =============================================================================
# SECTION: Entity-Specific Features - Curves
# =============================================================================

def entity_specific_curves():
    """Curve-specific features"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80)
    scene.background = "white"

    cells = list(scene.grid)

    # Different curvatures
    cells[0].add_curve(start="left", end="right", curvature=-0.5, width=2, color="#8b5cf6")
    cells[1].add_curve(start="left", end="right", curvature=0, width=2, color="#8b5cf6")
    cells[2].add_curve(start="left", end="right", curvature=0.5, width=2, color="#8b5cf6")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "19-entity-specific-curves.svg")

# =============================================================================
# SECTION: Entity-Specific Features - Polygons
# =============================================================================

def entity_specific_polygons():
    """Polygon-specific features"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=60)
    scene.background = "white"

    cells = list(scene.grid)

    # Different built-in shapes
    cells[0].add_polygon(Polygon.triangle(), fill="#8b5cf6")
    cells[1].add_polygon(Polygon.square(), fill="#8b5cf6")
    cells[2].add_polygon(Polygon.regular_polygon(sides=5), fill="#8b5cf6")  # Pentagon
    cells[3].add_polygon(Polygon.hexagon(), fill="#8b5cf6")
    cells[4].add_polygon(Polygon.star(points=5), fill="#8b5cf6")

    # Grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "20-entity-specific-polygons.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Entity types overview
    "01-entity-types-overview": entity_types_overview,

    # Common behavior
    "02-entity-position": entity_position,
    "03-entity-movement": entity_movement,
    "04-entity-rotation": entity_rotation,
    "05-entity-scaling": entity_scaling,
    "06-entity-z-index": entity_z_index,

    # Creating entities
    "07-create-via-cell-methods": create_via_cell_methods,
    "08-create-direct-construction": create_direct_construction,

    # Working with entities
    "09-store-references": store_references,
    "10-group-entities": group_entities,

    # Parametric positioning
    "11-parametric-line": parametric_line,
    "12-parametric-curve": parametric_curve,
    "13-parametric-ellipse": parametric_ellipse,

    # Entity patterns
    "14-pattern-data-driven-sizing": pattern_data_driven_sizing,
    "15-pattern-conditional-types": pattern_conditional_types,
    "16-pattern-progressive-transformation": pattern_progressive_transformation,

    # Entity-specific features
    "17-entity-specific-dots": entity_specific_dots,
    "18-entity-specific-lines": entity_specific_lines,
    "19-entity-specific-curves": entity_specific_curves,
    "20-entity-specific-polygons": entity_specific_polygons,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-entities.md...")

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
