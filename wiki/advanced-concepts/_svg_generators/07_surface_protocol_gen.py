#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/07-surface-protocol.md

Generates visual examples showcasing the Surface Protocol:
- Scene as "big cell" (named positions, along=/t=)
- CellGroup via grid.merge() (title bars, sidebars, averaged data)
- Combined showcase
"""

import math
from pyfreeform import Scene, Palette
from pathlib import Path


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "07-surface-protocol"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 01: Scene as Surface — named positions
# =============================================================================

def example_01_scene_as_surface():
    """Scene named positions — dots at corners, center, with connecting lines"""
    scene = Scene(width=400, height=300, background="#0f172a")

    # Diagonal line first (behind dots)
    scene.add_line(start="top_left", end="bottom_right", color="#334155", width=1.5)
    scene.add_line(start="top_right", end="bottom_left", color="#334155", width=1.5)
    scene.add_line(start="left", end="right", color="#1e293b", width=1)
    scene.add_line(start="top", end="bottom", color="#1e293b", width=1)

    # Named positions — labeled dots
    positions = {
        "top_left": "#3b82f6",
        "top_right": "#22c55e",
        "bottom_left": "#f97316",
        "bottom_right": "#8b5cf6",
        "center": "#f43f5e",
        "top": "#64748b",
        "bottom": "#64748b",
        "left": "#64748b",
        "right": "#64748b",
    }

    for name, color in positions.items():
        radius = 10 if name == "center" else 7
        scene.add_dot(at=name, radius=radius, color=color, z_index=2)

    # Labels for key positions
    scene.add_text("center", at=(0.5, 0.58), font_size=10, color="#94a3b8")
    scene.add_text("top_left", at=(0.15, 0.08), font_size=9, color="#94a3b8")
    scene.add_text("bottom_right", at=(0.82, 0.95), font_size=9, color="#94a3b8")
    scene.add_text("Scene is a Surface", at=(0.5, 0.15), font_size=14,
                   color="#f8fafc", z_index=3)

    scene.save(OUTPUT_DIR / "01-scene-as-surface.svg")


# =============================================================================
# 02: Scene along= and t= — the killer feature
# =============================================================================

def example_02_scene_along_t():
    """Cross-cell curve with dots placed using along=/t="""
    scene = Scene.with_grid(cols=25, rows=14, cell_size=14, background="#0f172a")

    # Subtle cell dots for texture
    for cell in scene.grid:
        cell.add_dot(radius=1.5, color="#1e293b")

    # Scene-level sine wave using a curve
    curve = scene.add_curve(
        start="left", end="right",
        curvature=0.35, color="#334155", width=2, z_index=1
    )

    # Place colored dots along it — the magic of along=/t=!
    n = 12
    for i in range(n):
        t = (i + 0.5) / n
        # Rainbow-ish gradient
        hue = t * 300
        r = max(0, min(255, int(255 * abs(math.sin(math.radians(hue))))))
        g = max(0, min(255, int(255 * abs(math.sin(math.radians(hue + 120))))))
        b = max(0, min(255, int(255 * abs(math.sin(math.radians(hue + 240))))))
        color = f"#{r:02x}{g:02x}{b:02x}"
        scene.add_dot(along=curve, t=t, radius=7, color=color, z_index=2)

    # Label
    scene.add_text("scene.add_dot(along=curve, t=...)",
                   at=(0.5, 0.12), font_size=11, color="#94a3b8", z_index=3)

    scene.save(OUTPUT_DIR / "02-scene-along-t.svg")


# =============================================================================
# 03: Basic merge — rectangular region
# =============================================================================

def example_03_basic_merge():
    """grid.merge() — merge a rectangular region"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#0f172a")

    # Show all cells with subtle borders
    for cell in scene.grid:
        cell.add_border(color="#1e293b", width=0.5)
        cell.add_dot(radius=2, color="#334155")

    # Merge a region
    group = scene.grid.merge(row_start=2, row_end=5, col_start=3, col_end=7)
    group.add_fill(color="#3b82f6", opacity=0.15, z_index=1)
    group.add_border(color="#60a5fa", width=2.5, z_index=2)
    group.add_dot(at="center", radius=8, color="#f43f5e", z_index=3)
    group.add_text("CellGroup", at=(0.5, 0.35), font_size=13, color="#f8fafc", z_index=3)
    group.add_text("(3 rows x 4 cols)", at=(0.5, 0.65), font_size=10, color="#94a3b8", z_index=3)

    scene.save(OUTPUT_DIR / "03-basic-merge.svg")


# =============================================================================
# 04: Layout — title bar + sidebar + content
# =============================================================================

def example_04_layout_merge():
    """Layout with merged header, sidebar, and cell content"""
    scene = Scene.with_grid(cols=16, rows=12, cell_size=22, background="#0f172a")
    colors = Palette.ocean()

    # Header (top 2 rows)
    header = scene.grid.merge(row_start=0, row_end=2)
    header.add_fill(color="#1e293b", z_index=0)
    header.add_text("Surface Protocol Demo", at="center",
                    font_size=14, color="#f8fafc", z_index=1)

    # Sidebar (left 3 cols, below header)
    sidebar = scene.grid.merge(row_start=2, row_end=12, col_start=0, col_end=3)
    sidebar.add_fill(color="#1e293b", opacity=0.5, z_index=0)

    # Sidebar decorative dots
    sidebar_curve = sidebar.add_curve(
        start=(0.5, 0.1), end=(0.5, 0.9),
        curvature=0.6, color="#334155", width=1, z_index=1
    )
    for i in range(5):
        t = (i + 0.5) / 5
        sidebar.add_dot(along=sidebar_curve, t=t, radius=4,
                        color=colors.accent, z_index=2)

    # Content area cells
    for cell in scene.grid:
        if cell.row >= 2 and cell.col >= 3:
            # Distance from center of content area
            cr = (2 + 12) / 2
            cc = (3 + 16) / 2
            dist = ((cell.row - cr)**2 + (cell.col - cc)**2) ** 0.5
            if dist < 5:
                radius = 2 + (5 - dist) * 0.8
                cell.add_dot(radius=radius, color=colors.primary, opacity=0.6)

    # Footer (bottom row, right of sidebar)
    footer = scene.grid.merge(row_start=11, row_end=12, col_start=3, col_end=16)
    footer.add_fill(color="#1e293b", opacity=0.3, z_index=0)
    footer.add_text("footer", at="center", font_size=9, color="#64748b", z_index=1)

    scene.save(OUTPUT_DIR / "04-layout-merge.svg")


# =============================================================================
# 05: Averaged data — super-pixels from merged blocks
# =============================================================================

def example_05_averaged_data():
    """Super-pixel effect using 2x2 merged blocks"""
    scene = Scene.with_grid(cols=20, rows=14, cell_size=16, background="#0f172a")

    # Assign synthetic brightness data (radial gradient)
    center_r, center_c = 7, 10
    for cell in scene.grid:
        dr = cell.row - center_r
        dc = cell.col - center_c
        dist = (dr * dr + dc * dc) ** 0.5
        brightness = max(0.0, 1.0 - dist / 10)
        cell._data["brightness"] = brightness
        # Synthetic color based on position
        r_val = int(59 + brightness * 185)
        g_val = int(130 - brightness * 80)
        b_val = int(246 - brightness * 100)
        cell._data["color"] = f"#{r_val:02x}{g_val:02x}{b_val:02x}"

    # Merge 2x2 blocks — "super pixels" with averaged data
    for row in range(0, scene.grid.rows - 1, 2):
        for col in range(0, scene.grid.cols - 1, 2):
            block = scene.grid.merge(row, row + 2, col, col + 2)
            # block.brightness and block.color are automatically averaged!
            if block.brightness > 0.1:
                radius = 2 + block.brightness * 10
                block.add_dot(at="center", color=block.color, radius=radius,
                              z_index=1)
            else:
                block.add_dot(at="center", radius=1.5, color="#1e293b")

    scene.save(OUTPUT_DIR / "05-averaged-data.svg")


# =============================================================================
# 06: CellGroup along= — curves on merged regions
# =============================================================================

def example_06_group_along():
    """Curves and along= on a merged CellGroup"""
    scene = Scene.with_grid(cols=20, rows=10, cell_size=20, background="#0f172a")

    # Cell texture
    for cell in scene.grid:
        cell.add_dot(radius=1, color="#1e293b")

    # Top banner — merged top 2 rows
    banner = scene.grid.merge(row_start=0, row_end=2)
    banner.add_fill(color="#1e293b", z_index=0)
    wave = banner.add_curve(
        start="left", end="right",
        curvature=0.5, color="#334155", width=1.5, z_index=1
    )
    for i in range(8):
        t = (i + 0.5) / 8
        banner.add_dot(along=wave, t=t, radius=5, color="#f43f5e", z_index=2)
    banner.add_text("along= on CellGroup", at=(0.5, 0.35),
                    font_size=11, color="#f8fafc", z_index=3)

    # Bottom banner — merged bottom 2 rows
    bottom = scene.grid.merge(row_start=8, row_end=10)
    bottom.add_fill(color="#1e293b", z_index=0)
    arc = bottom.add_curve(
        start="left", end="right",
        curvature=-0.4, color="#334155", width=1.5, z_index=1
    )
    for i in range(8):
        t = (i + 0.5) / 8
        bottom.add_dot(along=arc, t=t, radius=5, color="#3b82f6", z_index=2)

    # Middle content — a vertical merged strip
    strip = scene.grid.merge(row_start=2, row_end=8, col_start=9, col_end=11)
    strip.add_fill(color="#1e293b", opacity=0.4, z_index=0)
    vline = strip.add_line(start="top", end="bottom", color="#334155", width=1, z_index=1)
    for i in range(4):
        t = (i + 0.5) / 4
        strip.add_dot(along=vline, t=t, radius=4, color="#22c55e", z_index=2)

    scene.save(OUTPUT_DIR / "06-group-along.svg")


# =============================================================================
# 07: Showcase — everything together
# =============================================================================

def example_07_showcase():
    """Complete showcase: cells + merged regions + scene-level overlays"""
    scene = Scene.with_grid(cols=24, rows=16, cell_size=18, background="#0f172a")

    # --- Header ---
    header = scene.grid.merge(row_start=0, row_end=2)
    header.add_fill(color="#1e293b", z_index=0)
    header.add_text("The Surface Protocol", at="center",
                    font_size=15, color="#f8fafc", z_index=2)

    # --- Cell-level art in the body ---
    center_r, center_c = 9, 12
    for cell in scene.grid:
        if cell.row >= 2:
            dr = cell.row - center_r
            dc = cell.col - center_c
            dist = (dr * dr + dc * dc) ** 0.5
            if dist < 8:
                t = 1.0 - dist / 8
                radius = 1.5 + t * 4
                opacity = 0.2 + t * 0.8
                cell.add_dot(radius=radius, color="#3b82f6", opacity=opacity)

    # --- Scene-level decorative arc at the bottom ---
    arc = scene.add_curve(
        start=(0.05, 0.88), end=(0.95, 0.88),
        curvature=-0.2, color="#f43f5e", width=1.5, z_index=3
    )
    for i in range(14):
        t = (i + 0.5) / 14
        size = 2 + abs(math.sin(t * math.pi)) * 4
        scene.add_dot(along=arc, t=t, radius=size, color="#f43f5e",
                      opacity=0.3 + abs(math.sin(t * math.pi)) * 0.7, z_index=4)

    # --- Merged accent blocks ---
    left_block = scene.grid.merge(row_start=5, row_end=9, col_start=1, col_end=4)
    left_block.add_fill(color="#22c55e", opacity=0.1, z_index=1)
    left_block.add_border(color="#22c55e", opacity=0.5, width=1.5, z_index=2)
    left_block.add_text("merge()", at="center", font_size=10,
                        color="#22c55e", z_index=3)

    right_block = scene.grid.merge(row_start=5, row_end=9, col_start=20, col_end=23)
    right_block.add_fill(color="#f97316", opacity=0.1, z_index=1)
    right_block.add_border(color="#f97316", opacity=0.5, width=1.5, z_index=2)
    right_block.add_text("merge()", at="center", font_size=10,
                         color="#f97316", z_index=3)

    # --- Connecting scene-level line between blocks ---
    scene.add_line(
        start=(left_block.center.x / scene.width,
               left_block.center.y / scene.height),
        end=(right_block.center.x / scene.width,
             right_block.center.y / scene.height),
        color="#64748b", width=1, z_index=1
    )
    scene.add_dot(
        at=(0.5, left_block.center.y / scene.height),
        radius=5, color="#ffd23f", z_index=5
    )

    scene.save(OUTPUT_DIR / "07-showcase.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-scene-as-surface": example_01_scene_as_surface,
    "02-scene-along-t": example_02_scene_along_t,
    "03-basic-merge": example_03_basic_merge,
    "04-layout-merge": example_04_layout_merge,
    "05-averaged-data": example_05_averaged_data,
    "06-group-along": example_06_group_along,
    "07-showcase": example_07_showcase,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 07-surface-protocol.md...")

    for name, func in GENERATORS.items():
        try:
            func()
            print(f"  ✓ {name}.svg")
        except Exception as e:
            print(f"  ✗ {name}.svg - ERROR: {e}")
            import traceback
            traceback.print_exc()

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
