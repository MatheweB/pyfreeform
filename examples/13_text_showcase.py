#!/usr/bin/env python3
"""
Example 13: Text Feature Showcase

Demonstrates all text features in PyFreeform:
- Different font families (serif, sans-serif, monospace)
- Font sizes
- Alignment options (anchor and baseline)
- Text rotation
- Color customization
- Combining text with other elements

Output: examples/13_text_showcase.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Text, map_range

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 4
CELL_SIZE = 80

colors = Palette.sunset()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=GRID_SIZE, rows=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

# Row 0: Different font families
for i, (font, label) in enumerate([
    ("serif", "Serif"),
    ("sans-serif", "Sans"),
    ("monospace", "Mono"),
    ("cursive", "Cursive"),
]):
    cell = scene.grid[0, i]
    cell.add_border(color=colors.grid, z_index=0)
    cell.add_text(
        label,
        font_family=font,
        font_size=14,
        color=colors.accent,
        z_index=1,
    )

# Row 1: Different font sizes
for i in range(GRID_SIZE):
    cell = scene.grid[1, i]
    cell.add_border(color=colors.grid, z_index=0)
    font_size = 10 + (i * 6)
    cell.add_text(
        str(font_size),
        font_size=font_size,
        color=colors.primary,
        z_index=1,
    )

# Row 2: Text alignment
alignments = ["start", "middle", "middle", "end"]
baselines = ["hanging", "middle", "alphabetic", "middle"]
for i in range(GRID_SIZE):
    cell = scene.grid[2, i]
    cell.add_border(color=colors.grid, z_index=0)

    # Add crosshair to show anchor point
    cell.add_line(start=(0.5, 0.2), end=(0.5, 0.8), color=colors.grid, width=0.5, z_index=0)
    cell.add_line(start=(0.2, 0.5), end=(0.8, 0.5), color=colors.grid, width=0.5, z_index=0)

    cell.add_text(
        "Aa",
        font_size=16,
        color=colors.secondary,
        text_anchor=alignments[i],
        baseline=baselines[i],
        z_index=1,
    )

# Row 3: Rotated text
for i in range(GRID_SIZE):
    cell = scene.grid[3, i]
    cell.add_border(color=colors.grid, z_index=0)

    rotation = i * 30
    cell.add_text(
        f"{rotation}°",
        font_size=14,
        color=colors.line,
        rotation=rotation,
        z_index=1,
    )

# Add title using absolute positioning
title = Text(
    scene.width / 2,
    scene.height + 25,
    "Text Feature Showcase",
    font_size=16,
    font_family="sans-serif",
    color=colors.accent,
    text_anchor="middle",
    baseline="hanging",
    z_index=10,
)
scene.place(title)

# Add labels for rows
labels = [
    "Font Families",
    "Font Sizes",
    "Alignment",
    "Rotation",
]

for i, label in enumerate(labels):
    label_text = Text(
        -10,
        i * CELL_SIZE + CELL_SIZE / 2,
        label,
        font_size=10,
        font_family="sans-serif",
        color=colors.grid,
        text_anchor="end",
        baseline="middle",
        z_index=10,
    )
    scene.place(label_text)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "13_text_showcase.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("This example demonstrates:")
print("  • Different font families (serif, sans-serif, monospace, cursive)")
print("  • Multiple font sizes (10-28px)")
print("  • Text alignment options (anchor and baseline)")
print("  • Text rotation (0°, 30°, 60°, 90°)")
print("  • Combining text with other elements")
print("  • Absolute positioning with scene.place()")
