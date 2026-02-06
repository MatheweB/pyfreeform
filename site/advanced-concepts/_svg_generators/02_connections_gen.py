#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/02-connections.md

Generates visual examples for connections between entities.

Corresponds to sections:
- What is a Connection?
- Creating Connections
- Auto-Updating
- Connection Styling
- Common Patterns
"""

from pyfreeform import Scene, Connection
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-connections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_test_image() -> Path:
    """Create a simple test image"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_connections.png"
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
# SECTION: What is a Connection?
# =============================================================================

def what_is_connection_basic():
    """Basic connection between two entities"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create two dots
    dot1 = cell1.add_dot(radius=10, color="#ef4444")
    dot2 = cell2.add_dot(radius=10, color="#3b82f6")

    # Create connection
    connection = Connection(
        start=dot1,
        end=dot2,
        start_anchor="center",
        end_anchor="center", style={"width": 2, "color": "#94a3b8"})
    scene.add(connection)

    scene.save(OUTPUT_DIR / "01-what-is-connection-basic.svg")

def what_is_connection_labeled():
    """Connection with labeled anchors"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create rectangle and ellipse
    from pyfreeform import Rect
    rect = Rect(cell1.center.x - 20.0, cell1.center.y - 15.0, 40, 30, fill="#ef4444")
    rect.cell = cell1
    cell1._entities.append(rect)
    ellipse = cell2.add_ellipse(rx=20, ry=15, fill="#3b82f6")

    # Create connection
    connection = Connection(
        start=rect,
        end=ellipse,
        start_anchor="right",
        end_anchor="left", style={"width": 2, "color": "#94a3b8"})
    scene.add(connection)

    # Show anchor points
    cell1.add_dot(at=rect.anchor("right"), radius=3, color="#10b981", z_index=5)
    cell2.add_dot(at=ellipse.anchor("left"), radius=3, color="#10b981", z_index=5)

    # Labels
    cell1.add_text("anchor: 'right'", at=(0.5, 0.85), font_size=7, color="#1f2937")
    cell2.add_text("anchor: 'left'", at=(0.5, 0.85), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "02-what-is-connection-labeled.svg")

# =============================================================================
# SECTION: Creating Connections
# =============================================================================

def creating_connection_simple():
    """Simple connection creation"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create dots
    dot1 = cell1.add_dot(radius=8, color="#ef4444")
    dot2 = cell2.add_dot(radius=8, color="#3b82f6")

    # Create connection
    connection = Connection(
        start=dot1,
        end=dot2,
        start_anchor="center",
        end_anchor="center", style={"width": 2, "color": "#94a3b8"})
    scene.add(connection)

    scene.save(OUTPUT_DIR / "03-creating-connection-simple.svg")

def creating_connection_styled():
    """Connection with custom styling"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create dots
    dot1 = cell1.add_dot(radius=8, color="#ef4444")
    dot2 = cell2.add_dot(radius=8, color="#3b82f6")

    # Create styled connection
    connection = Connection(
        start=dot1,
        end=dot2,
        start_anchor="center",
        end_anchor="center", style={"width": 4, "color": "#8b5cf6"})
    scene.add(connection)

    scene.save(OUTPUT_DIR / "04-creating-connection-styled.svg")

# =============================================================================
# SECTION: Auto-Updating
# =============================================================================

def auto_updating_positions():
    """Connection automatically updates when entities move"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Position 1: Close together
    cell1 = scene.grid[0, 0]
    dot1a = cell1.add_dot(at=(0.4, 0.5), radius=6, color="#ef4444")
    dot1b = cell1.add_dot(at=(0.6, 0.5), radius=6, color="#3b82f6")
    conn1 = Connection(dot1a, dot1b, "center", "center", style={"width": 2, "color": "#94a3b8"})
    scene.add(conn1)
    cell1.add_text("Original", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Position 2: Moved apart
    cell2 = scene.grid[0, 1]
    dot2a = cell2.add_dot(at=(0.2, 0.3), radius=6, color="#ef4444")
    dot2b = cell2.add_dot(at=(0.8, 0.7), radius=6, color="#3b82f6")
    conn2 = Connection(dot2a, dot2b, "center", "center", style={"width": 2, "color": "#94a3b8"})
    scene.add(conn2)
    cell2.add_text("Moved", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Position 3: Diagonal
    cell3 = scene.grid[0, 2]
    dot3a = cell3.add_dot(at=(0.2, 0.2), radius=6, color="#ef4444")
    dot3b = cell3.add_dot(at=(0.8, 0.8), radius=6, color="#3b82f6")
    conn3 = Connection(dot3a, dot3b, "center", "center", style={"width": 2, "color": "#94a3b8"})
    scene.add(conn3)
    cell3.add_text("Auto-adjusted", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "05-auto-updating-positions.svg")

def auto_updating_demonstration():
    """Demonstrating dynamic updates"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    for i, progress in enumerate([0.2, 0.4, 0.6, 0.8]):
        cell = scene.grid[0, i]

        # Create moving dot and static dot
        moving_dot = cell.add_dot(at=(progress, 0.5), radius=5, color="#ef4444")
        static_dot = cell.add_dot(at=(0.5, 0.2), radius=5, color="#3b82f6")

        # Connection follows
        conn = Connection(moving_dot, static_dot, "center", "center", style={"width": 2, "color": "#94a3b8"})
        scene.add(conn)

        cell.add_text(f"t={progress:.1f}", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "06-auto-updating-demonstration.svg")

# =============================================================================
# SECTION: Connection Styling
# =============================================================================

def styling_colors():
    """Different connection colors"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b"]
    names = ["Red", "Blue", "Green", "Orange"]

    for i, (color, name) in enumerate(zip(colors, names)):
        cell = scene.grid[0, i]

        dot1 = cell.add_dot(at=(0.3, 0.5), radius=5, color="#1f2937")
        dot2 = cell.add_dot(at=(0.7, 0.5), radius=5, color="#1f2937")

        conn = Connection(dot1, dot2, "center", "center", style={"width": 3, "color": color})
        scene.add(conn)

        cell.add_text(name, at=(0.5, 0.8), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "07-styling-colors.svg")

def styling_widths():
    """Different connection widths"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    widths = [1, 2, 4, 6]

    for i, width in enumerate(widths):
        cell = scene.grid[0, i]

        dot1 = cell.add_dot(at=(0.3, 0.5), radius=5, color="#1f2937")
        dot2 = cell.add_dot(at=(0.7, 0.5), radius=5, color="#1f2937")

        conn = Connection(dot1, dot2, "center", "center", style={"width": width, "color": "#3b82f6"})
        scene.add(conn)

        cell.add_text(f"{width}px", at=(0.5, 0.8), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "08-styling-widths.svg")

def styling_opacity():
    """Connection opacity variations"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    opacities = [0.25, 0.5, 0.75, 1.0]

    for i, opacity in enumerate(opacities):
        cell = scene.grid[0, i]

        dot1 = cell.add_dot(at=(0.3, 0.5), radius=5, color="#1f2937")
        dot2 = cell.add_dot(at=(0.7, 0.5), radius=5, color="#1f2937")

        conn = Connection(dot1, dot2, "center", "center", style={"width": 4, "color": "#3b82f6"})
        scene.add(conn)

        cell.add_text(f"{opacity:.2f}", at=(0.5, 0.8), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "09-styling-opacity.svg")

# =============================================================================
# SECTION: Common Patterns
# =============================================================================

def pattern_connect_neighbors():
    """Connect neighboring cells"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=30)
    scene.background = "#f8f9fa"

    # Create dots in all cells
    dots = {}
    for cell in scene.grid:
        dot = cell.add_dot(color="#3b82f6", radius=4, z_index=10)
        dots[cell] = dot

    # Connect right neighbors
    for cell in scene.grid:
        if cell.right:
            conn = Connection(
                dots[cell],
                dots[cell.right],
                "center",
                "center", style={"width": 1, "color": "#94a3b8"})
            scene.add(conn)

    # Connect bottom neighbors
    for cell in scene.grid:
        if cell.below:
            conn = Connection(
                dots[cell],
                dots[cell.below],
                "center",
                "center", style={"width": 1, "color": "#94a3b8"})
            scene.add(conn)

    scene.save(OUTPUT_DIR / "10-pattern-connect-neighbors.svg")

def pattern_highlight_connections():
    """Highlight bright cells with connections"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    bright_dots = []

    for cell in scene.grid.where(lambda c: c.brightness > 0.7):
        dot = cell.add_dot(color="#f59e0b", radius=5, z_index=10)
        bright_dots.append(dot)

    # Connect bright dots sequentially
    for i in range(len(bright_dots) - 1):
        conn = Connection(
            bright_dots[i],
            bright_dots[i + 1],
            "center",
            "center", style={"width": 1.5, "color": "#94a3b8"})
        scene.add(conn)

    scene.save(OUTPUT_DIR / "11-pattern-highlight-connections.svg")

def pattern_radial_connections():
    """Radial connections from center"""
    scene = Scene.with_grid(cols=11, rows=11, cell_size=22)
    scene.background = "#f8f9fa"

    center = scene.grid[5, 5]
    center_dot = center.add_dot(color="#ef4444", radius=6, z_index=10)

    # Connect to border cells
    for cell in scene.grid.border(thickness=1):
        outer_dot = cell.add_dot(color="#3b82f6", radius=4, z_index=10)
        conn = Connection(
            center_dot,
            outer_dot,
            "center",
            "center", style={"width": 1, "color": "#d1d5db"})
        scene.add(conn)

    scene.save(OUTPUT_DIR / "12-pattern-radial-connections.svg")

def pattern_sequential_chain():
    """Sequential chain of connections"""
    scene = Scene.with_grid(cols=15, rows=1, cell_size=30)
    scene.background = "#f8f9fa"

    dots = []
    for cell in scene.grid:
        dot = cell.add_dot(color="#3b82f6", radius=5, z_index=10)
        dots.append(dot)

    # Chain connections
    for i in range(len(dots) - 1):
        conn = Connection(
            dots[i],
            dots[i + 1],
            "center",
            "center", style={"width": 2, "color": "#94a3b8"})
        scene.add(conn)

    scene.save(OUTPUT_DIR / "13-pattern-sequential-chain.svg")

def pattern_cross_connections():
    """Cross connections in grid"""
    scene = Scene.with_grid(cols=5, rows=5, cell_size=48)
    scene.background = "#f8f9fa"

    # Create dots in checkerboard pattern
    dots = {}
    for cell in scene.grid.checkerboard("black"):
        dot = cell.add_dot(color="#3b82f6", radius=6, z_index=10)
        dots[cell] = dot

    # Connect diagonal neighbors
    for cell in scene.grid.checkerboard("black"):
        if cell in dots:
            # Connect to diagonal neighbors
            if cell.above_right and cell.above_right in dots:
                conn = Connection(
                    dots[cell],
                    dots[cell.above_right],
                    "center",
                    "center", style={"width": 1, "color": "#94a3b8"})
                scene.add(conn)

            if cell.below_right and cell.below_right in dots:
                conn = Connection(
                    dots[cell],
                    dots[cell.below_right],
                    "center",
                    "center", style={"width": 1, "color": "#94a3b8"})
                scene.add(conn)

    scene.save(OUTPUT_DIR / "14-pattern-cross-connections.svg")

def pattern_different_anchors():
    """Connections between different anchors"""
    scene = Scene.with_grid(cols=3, rows=3, cell_size=80)
    scene.background = "#f8f9fa"

    # Center cell
    center = scene.grid[1, 1]
    from pyfreeform import Rect
    center_rect = Rect(center.center.x - 20.0, center.center.y - 20.0, 40, 40, fill="#ef4444")
    center_rect.cell = center
    center._entities.append(center_rect)

    # Corner cells with different anchor connections
    anchors = [
        (scene.grid[0, 0], "bottom_right", "top_left"),
        (scene.grid[0, 2], "bottom_left", "top_right"),
        (scene.grid[2, 0], "top_right", "bottom_left"),
        (scene.grid[2, 2], "top_left", "bottom_right"),
    ]

    for cell, start_anch, end_anch in anchors:
        from pyfreeform import Rect
        rect = Rect(cell.center.x - 15.0, cell.center.y - 15.0, 30, 30, fill="#3b82f6")
        rect.cell = cell
        cell._entities.append(rect)
        conn = Connection(
            rect,
            center_rect,
            start_anch,
            end_anch, style={"width": 2, "color": "#94a3b8"})
        scene.add(conn)

        # Show anchor points
        cell.add_dot(at=rect.anchor(start_anch), radius=2, color="#10b981", z_index=5)

    # Show center anchors
    for anchor in ["top_left", "top_right", "bottom_left", "bottom_right"]:
        center.add_dot(at=center_rect.anchor(anchor), radius=2, color="#10b981", z_index=5)

    scene.save(OUTPUT_DIR / "15-pattern-different-anchors.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # What is a connection?
    "01-what-is-connection-basic": what_is_connection_basic,
    "02-what-is-connection-labeled": what_is_connection_labeled,

    # Creating connections
    "03-creating-connection-simple": creating_connection_simple,
    "04-creating-connection-styled": creating_connection_styled,

    # Auto-updating
    "05-auto-updating-positions": auto_updating_positions,
    "06-auto-updating-demonstration": auto_updating_demonstration,

    # Styling
    "07-styling-colors": styling_colors,
    "08-styling-widths": styling_widths,
    "09-styling-opacity": styling_opacity,

    # Common patterns
    "10-pattern-connect-neighbors": pattern_connect_neighbors,
    "11-pattern-highlight-connections": pattern_highlight_connections,
    "12-pattern-radial-connections": pattern_radial_connections,
    "13-pattern-sequential-chain": pattern_sequential_chain,
    "14-pattern-cross-connections": pattern_cross_connections,
    "15-pattern-different-anchors": pattern_different_anchors,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-connections.md...")

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
