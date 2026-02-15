"""Generate SVGs for Guide: Layout & Alignment."""

from pyfreeform import (
    Scene,
    Palette,
    Rect,
    Dot,
    Text,
    RelCoord,
)
from pyfreeform.layout import between, align, distribute, stack

from wiki._generator import save


def generate():
    colors = Palette.midnight()

    # --- 1. between: label placed between a shape and cell bottom ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200, background=colors.background)
    cell = scene.grid[0][0]
    cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    shape = cell.add_rect(at=(0.5, 0.3), width=0.5, height=0.3, fill=colors.primary)
    mid = between(shape, cell, anchor="bottom")
    cell.add_dot(at=mid, radius=0.02, color=colors.accent)
    cell.add_text("between()", at=RelCoord(mid.rx, mid.ry + 0.06), font_size=0.09, color="#aaaacc")
    save(scene, "guide/layout-between.svg")

    # --- 2. align: center_y alignment ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200, background=colors.background)
    cell = scene.grid[0][0]
    cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    d1 = cell.add_dot(at=(0.2, 0.3), radius=0.06, color=colors.primary)
    d2 = cell.add_dot(at=(0.5, 0.6), radius=0.06, color=colors.accent)
    d3 = cell.add_dot(at=(0.8, 0.15), radius=0.06, color=colors.secondary)
    # Show "before" guides with faint lines
    for d in [d2, d3]:
        cell.add_line(start=(0.0, d.at.ry), end=(1.0, d.at.ry), width=0.003, color="#555577", opacity=0.4)
    align(d1, d2, d3, anchor="center_y")
    # Show alignment line
    cell.add_line(start=(0.0, 0.3), end=(1.0, 0.3), width=0.005, color=colors.accent, opacity=0.6)
    cell.add_text("align(anchor='center_y')", at=(0.5, 0.92), font_size=0.07, color="#aaaacc")
    save(scene, "guide/layout-align.svg")

    # --- 3. distribute: even spacing ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200, background=colors.background)
    cell = scene.grid[0][0]
    cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    dots = [cell.add_dot(at=(0.5, 0.5), radius=0.06, color=colors.primary) for _ in range(5)]
    distribute(*dots, axis="x", start=0.1, end=0.9)
    align(*dots, anchor="center_y")
    # Annotate spacing
    cell.add_line(start=(0.1, 0.35), end=(0.9, 0.35), width=0.003, color=colors.accent, opacity=0.5)
    for d in dots:
        dc = d.relative_anchor("center")
        cell.add_line(start=(dc.rx, 0.33), end=(dc.rx, 0.37), width=0.005, color=colors.accent, opacity=0.5)
    cell.add_text("distribute(axis='x', start=0.1, end=0.9)", at=(0.5, 0.92), font_size=0.06, color="#aaaacc")
    save(scene, "guide/layout-distribute.svg")

    # --- 4. stack: vertical stacking ---
    scene = Scene.with_grid(cols=1, rows=1, cell_size=240, background=colors.background)
    cell = scene.grid[0][0]
    cell.add_border(color=colors.grid, width=0.5, opacity=0.3)
    title = cell.add_text("Title", at=(0.5, 0.15), font_size=0.1, color=colors.accent, bold=True)
    box = cell.add_rect(at=(0.5, 0.5), width=0.5, height=0.3, fill=colors.primary)
    caption = cell.add_text("caption", at=(0.5, 0.8), font_size=0.07, color="#aaaacc", italic=True)
    stack(title, box, caption, direction="below", gap=0.04)
    cell.add_text("stack(direction='below', gap=0.04)", at=(0.5, 0.95), font_size=0.055, color="#777799")
    save(scene, "guide/layout-stack.svg")
