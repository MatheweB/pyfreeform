#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/01-anchor-system.md

Generates visual examples for the anchor system.

Corresponds to sections:
- What are Anchors?
- Using Anchors
- Why Anchors?
- Examples
"""

from pyfreeform import Scene
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-anchor-system"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: What are Anchors?
# =============================================================================

def anchors_dot():
    """Dot anchors visualization"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a dot
    dot = cell.add_dot(radius=15, color="#3b82f6")

    # Show center anchor
    center = dot.anchor("center")
    cell.add_dot(at=center, radius=4, color="#ef4444")

    # Label
    cell.add_text("center", at=(0.5, 0.75), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "01-anchors-dot.svg")

def anchors_line():
    """Line anchors visualization"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a line
    line = cell.add_line(start="left", end="right", color="#3b82f6", width=2)

    # Show anchors
    anchors = ["start", "center", "end"]
    colors = ["#ef4444", "#10b981", "#f59e0b"]

    for anchor_name, color in zip(anchors, colors):
        point = line.anchor(anchor_name)
        cell.add_dot(at=point, radius=4, color=color)

    # Labels
    cell.add_text("start", at=(0.1, 0.2), font_size=8, color="#1f2937")
    cell.add_text("center", at=(0.5, 0.2), font_size=8, color="#1f2937")
    cell.add_text("end", at=(0.9, 0.2), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "02-anchors-line.svg")

def anchors_ellipse():
    """Ellipse anchors visualization"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create an ellipse
    ellipse = cell.add_ellipse(rx=40, ry=25, fill="#3b82f6")

    # Show cardinal anchors
    anchors = ["center", "right", "top", "left", "bottom"]
    colors = ["#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]

    for anchor_name, color in zip(anchors, colors):
        point = ellipse.anchor(anchor_name)
        cell.add_dot(at=point, radius=3, color=color)

    scene.save(OUTPUT_DIR / "03-anchors-ellipse.svg")

def anchors_rectangle():
    """Rectangle anchors visualization"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a rectangle entity
    rect = cell.add_rect(width=60, height=40, fill="#3b82f6")

    # Show corner anchors
    corners = ["top_left", "top_right", "bottom_left", "bottom_right"]
    for anchor_name in corners:
        point = rect.anchor(anchor_name)
        cell.add_dot(at=point, radius=3, color="#ef4444")

    # Show side anchors
    sides = ["top", "bottom", "left", "right"]
    for anchor_name in sides:
        point = rect.anchor(anchor_name)
        cell.add_dot(at=point, radius=3, color="#10b981")

    # Show center anchor
    center = rect.anchor("center")
    cell.add_dot(at=center, radius=3, color="#f59e0b")

    scene.save(OUTPUT_DIR / "04-anchors-rectangle.svg")

def anchors_polygon():
    """Polygon anchors visualization"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a hexagon
    from pyfreeform import shapes
    poly = cell.add_polygon(shapes.hexagon(size=0.7), fill="#3b82f6")

    # Show vertex anchors
    colors = ["#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#14b8a6"]
    for i in range(6):
        point = poly.anchor(f"v{i}")
        cell.add_dot(at=point, radius=3, color=colors[i])

    # Show center
    center = poly.anchor("center")
    cell.add_dot(at=center, radius=3, color="#1f2937")

    scene.save(OUTPUT_DIR / "05-anchors-polygon.svg")

def anchors_curve():
    """Curve anchors visualization"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a curve
    curve = cell.add_curve(start="left", end="right", curvature=0.4, color="#3b82f6", width=2)

    # Show anchors
    anchors = ["start", "center", "end", "control"]
    colors = ["#ef4444", "#10b981", "#f59e0b", "#8b5cf6"]

    for anchor_name, color in zip(anchors, colors):
        point = curve.anchor(anchor_name)
        cell.add_dot(at=point, radius=3, color=color)

    scene.save(OUTPUT_DIR / "06-anchors-curve.svg")

# =============================================================================
# SECTION: Using Anchors
# =============================================================================

def using_anchors_get():
    """Getting anchor points"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Cell 1: Rectangle with center anchor
    cell1 = scene.grid[0, 0]
    rect = cell1.add_rect(width=50, height=30, fill="#3b82f6")
    center = rect.anchor("center")
    cell1.add_dot(at=center, radius=5, color="#ef4444")
    cell1.add_text("center", at=(0.5, 0.8), font_size=9, color="#1f2937")

    # Cell 2: Rectangle with top_left anchor
    cell2 = scene.grid[0, 1]
    rect2 = cell2.add_rect(width=50, height=30, fill="#3b82f6")
    top_left = rect2.anchor("top_left")
    cell2.add_dot(at=top_left, radius=5, color="#10b981")
    cell2.add_text("top_left", at=(0.5, 0.8), font_size=9, color="#1f2937")

    scene.save(OUTPUT_DIR / "07-using-anchors-get.svg")

def using_anchors_connect():
    """Connecting via anchors"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create two dots
    dot1 = cell1.add_dot(radius=8, color="#3b82f6")
    dot2 = cell2.add_dot(radius=8, color="#10b981")

    # Connect via anchors
    from pyfreeform import Connection
    connection = Connection(
        start=dot1,
        end=dot2,
        start_anchor="center",
        end_anchor="center", style={"width": 2, "color": "#94a3b8"})
    scene.add(connection)

    scene.save(OUTPUT_DIR / "08-using-anchors-connect.svg")

# =============================================================================
# SECTION: Why Anchors?
# =============================================================================

def why_anchors_named_refs():
    """Named references - no manual calculation"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Without anchors (manual calculation - shown as complex)
    rect1 = cell1.add_rect(width=40, height=30, fill="#ef4444")
    cell1.add_text("Manual calc", at=(0.5, 0.8), font_size=8, color="#1f2937")

    # With anchors (simple)
    rect2 = cell2.add_rect(width=40, height=30, fill="#10b981")
    point = rect2.anchor("bottom_right")
    cell2.add_dot(at=point, radius=4, color="#3b82f6")
    cell2.add_text("anchor('bottom_right')", at=(0.5, 0.8), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "09-why-anchors-named-refs.svg")

def why_anchors_auto_updating():
    """Auto-updating connections"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    from pyfreeform import Connection

    # Position 1: Original
    cell1 = scene.grid[0, 0]
    dot1a = cell1.add_dot(at=(0.3, 0.5), radius=6, color="#3b82f6")
    dot1b = cell1.add_dot(at=(0.7, 0.5), radius=6, color="#10b981")
    conn1 = Connection(dot1a, dot1b, "center", "center", style={"width": 2, "color": "#94a3b8"})
    scene.add(conn1)
    cell1.add_text("Original", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Position 2: Moved
    cell2 = scene.grid[0, 1]
    dot2a = cell2.add_dot(at=(0.2, 0.3), radius=6, color="#3b82f6")
    dot2b = cell2.add_dot(at=(0.8, 0.7), radius=6, color="#10b981")
    conn2 = Connection(dot2a, dot2b, "center", "center", style={"width": 2, "color": "#94a3b8"})
    scene.add(conn2)
    cell2.add_text("Moved", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Position 3: Further moved
    cell3 = scene.grid[0, 2]
    dot3a = cell3.add_dot(at=(0.5, 0.2), radius=6, color="#3b82f6")
    dot3b = cell3.add_dot(at=(0.5, 0.8), radius=6, color="#10b981")
    conn3 = Connection(dot3a, dot3b, "center", "center", style={"width": 2, "color": "#94a3b8"})
    scene.add(conn3)
    cell3.add_text("Auto-updated", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "10-why-anchors-auto-updating.svg")

def why_anchors_transform_aware():
    """Transform-aware anchors"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Normal rectangle
    cell1 = scene.grid[0, 0]
    rect1 = cell1.add_rect(width=40, height=25, fill="#3b82f6")
    for anchor in ["top_left", "top_right", "bottom_left", "bottom_right"]:
        cell1.add_dot(at=rect1.anchor(anchor), radius=3, color="#ef4444")
    cell1.add_text("Normal", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Rotated rectangle
    cell2 = scene.grid[0, 1]
    rect2 = cell2.add_rect(width=40, height=25, rotation=30, fill="#3b82f6")
    for anchor in ["top_left", "top_right", "bottom_left", "bottom_right"]:
        cell2.add_dot(at=rect2.anchor(anchor), radius=3, color="#ef4444")
    cell2.add_text("Rotated", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Scaled & rotated rectangle
    cell3 = scene.grid[0, 2]
    rect3 = cell3.add_rect(width=48, height=30, rotation=45, fill="#3b82f6")
    for anchor in ["top_left", "top_right", "bottom_left", "bottom_right"]:
        cell3.add_dot(at=rect3.anchor(anchor), radius=3, color="#ef4444")
    cell3.add_text("Scaled+Rotated", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "11-why-anchors-transform-aware.svg")

# =============================================================================
# SECTION: Examples
# =============================================================================

def example_position_relative():
    """Position relative to entity anchors"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a line
    line = cell.add_line(start="left", end="right", color="#3b82f6", width=2)

    # Add dots at line anchors
    line_start = line.anchor("start")
    cell.add_dot(at=line_start, radius=5, color="#ef4444")

    line_end = line.anchor("end")
    cell.add_dot(at=line_end, radius=5, color="#10b981")

    line_center = line.anchor("center")
    cell.add_dot(at=line_center, radius=5, color="#f59e0b")

    scene.save(OUTPUT_DIR / "12-example-position-relative.svg")

def example_dynamic_connections():
    """Dynamic connections between entities"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create a rectangle and dot
    rect = cell1.add_rect(width=40, height=30, fill="#3b82f6")
    dot = cell2.add_dot(radius=8, color="#10b981")

    # Connect them
    from pyfreeform import Connection
    connection = Connection(
        start=rect,
        end=dot,
        start_anchor="bottom_right",
        end_anchor="center", style={"width": 2, "color": "#94a3b8"})
    scene.add(connection)

    # Show the anchor points
    cell1.add_dot(at=rect.anchor("bottom_right"), radius=3, color="#ef4444", z_index=5)
    cell2.add_dot(at=dot.anchor("center"), radius=3, color="#ef4444", z_index=5)

    scene.save(OUTPUT_DIR / "13-example-dynamic-connections.svg")

def example_all_entity_types():
    """All entity types with their anchors"""
    scene = Scene.with_grid(cols=3, rows=2, cell_size=80)
    scene.background = "#f8f9fa"

    # Dot
    cell = scene.grid[0, 0]
    dot = cell.add_dot(radius=10, color="#3b82f6")
    cell.add_dot(at=dot.anchor("center"), radius=3, color="#ef4444")
    cell.add_text("Dot", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Line
    cell = scene.grid[0, 1]
    line = cell.add_line(start="left", end="right", color="#3b82f6", width=2)
    for anchor in ["start", "center", "end"]:
        cell.add_dot(at=line.anchor(anchor), radius=3, color="#ef4444")
    cell.add_text("Line", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Ellipse
    cell = scene.grid[0, 2]
    ellipse = cell.add_ellipse(rx=25, ry=15, fill="#3b82f6")
    for anchor in ["center", "right", "top", "left", "bottom"]:
        cell.add_dot(at=ellipse.anchor(anchor), radius=2, color="#ef4444")
    cell.add_text("Ellipse", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Rectangle
    cell = scene.grid[1, 0]
    rect = cell.add_rect(width=35, height=25, fill="#3b82f6")
    for anchor in ["top_left", "top_right", "bottom_left", "bottom_right", "center"]:
        cell.add_dot(at=rect.anchor(anchor), radius=2, color="#ef4444")
    cell.add_text("Rectangle", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Polygon
    cell = scene.grid[1, 1]
    from pyfreeform import shapes
    poly = cell.add_polygon(shapes.triangle(size=0.7), fill="#3b82f6")
    for i in range(3):
        cell.add_dot(at=poly.anchor(f"v{i}"), radius=2, color="#ef4444")
    cell.add_dot(at=poly.anchor("center"), radius=2, color="#10b981")
    cell.add_text("Polygon", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Curve
    cell = scene.grid[1, 2]
    curve = cell.add_curve(start="left", end="right", curvature=0.3, color="#3b82f6", width=2)
    for anchor in ["start", "center", "end"]:
        cell.add_dot(at=curve.anchor(anchor), radius=2, color="#ef4444")
    cell.add_text("Curve", at=(0.5, 0.9), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "14-example-all-entity-types.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # What are anchors?
    "01-anchors-dot": anchors_dot,
    "02-anchors-line": anchors_line,
    "03-anchors-ellipse": anchors_ellipse,
    "04-anchors-rectangle": anchors_rectangle,
    "05-anchors-polygon": anchors_polygon,
    "06-anchors-curve": anchors_curve,

    # Using anchors
    "07-using-anchors-get": using_anchors_get,
    "08-using-anchors-connect": using_anchors_connect,

    # Why anchors?
    "09-why-anchors-named-refs": why_anchors_named_refs,
    "10-why-anchors-auto-updating": why_anchors_auto_updating,
    "11-why-anchors-transform-aware": why_anchors_transform_aware,

    # Examples
    "12-example-position-relative": example_position_relative,
    "13-example-dynamic-connections": example_dynamic_connections,
    "14-example-all-entity-types": example_all_entity_types,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-anchor-system.md...")

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
