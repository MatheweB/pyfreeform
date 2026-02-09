"""Generate SVGs for Recipe: Flowing Curves & Waves."""

import math

from pyfreeform import Scene, Palette, Coord, map_range

from wiki_v2._generator import save, sample_image


def generate():
    # --- 1. Curve field (curves connecting neighbors) ---
    colors = Palette.ocean()
    scene = Scene.with_grid(cols=18, rows=14, cell_size=18, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        curvature = math.sin(nx * math.pi * 2 + ny * math.pi) * 0.7
        cell.add_curve(
            start="left", end="right",
            curvature=curvature,
            width=0.5 + ny * 2,
            color=colors.primary,
            opacity=0.3 + nx * 0.6,
        )
    save(scene, "recipes/flow-curve-field.svg")

    # --- 2. Wave visualization ---
    class Wave:
        def __init__(self, x1, y1, x2, y2, amplitude, frequency):
            self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
            self.amp, self.freq = amplitude, frequency

        def point_at(self, t):
            x = self.x1 + t * (self.x2 - self.x1)
            cy = self.y1 + t * (self.y2 - self.y1)
            y = cy + self.amp * math.sin(t * self.freq * 2 * math.pi)
            return Coord(x, y)

    colors = Palette.neon()
    scene = Scene.with_grid(cols=1, rows=1, cell_size=360, background=colors.background)
    cell = scene.grid[0, 0]
    cx, cy = cell.center
    # Multiple overlapping waves
    for i in range(8):
        phase = i * 0.3
        amplitude = 20 + i * 12
        freq = 2 + i * 0.5
        wave = Wave(
            cell.x + 10, cy + math.sin(phase) * 30,
            cell.x + cell.width - 10, cy + math.cos(phase) * 30,
            amplitude=amplitude,
            frequency=freq,
        )
        opacity = 0.8 - i * 0.08
        color = colors.primary if i % 2 == 0 else colors.secondary
        cell.add_path(wave, segments=48, width=1.5, color=color, opacity=opacity)
    save(scene, "recipes/flow-waves.svg")

    # --- 3. Spiral paths with varying density ---
    class Spiral:
        def __init__(self, cx, cy, max_r, turns=3):
            self.cx, self.cy, self.max_r, self.turns = cx, cy, max_r, turns

        def point_at(self, t):
            angle = t * self.turns * 2 * math.pi
            r = t * self.max_r
            return Coord(self.cx + r * math.cos(angle), self.cy + r * math.sin(angle))

    colors = Palette.sunset()
    scene = Scene.with_grid(cols=6, rows=5, cell_size=48, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        cx, cy = cell.center
        turns = 2 + nx * 3
        spiral = Spiral(cx, cy, scene.grid.cell_width * 0.42, turns=turns)
        cell.add_path(
            spiral, segments=48,
            width=0.8 + ny * 1.5,
            color=colors.primary,
            opacity=0.4 + (nx + ny) / 2 * 0.6,
        )
    save(scene, "recipes/flow-spirals.svg")

    # --- 4. Overlapping curves on image ---
    scene = Scene.from_image(
        sample_image("MCEscherBirds.jpg"),
        grid_size=35,
        cell_size=10,
    )
    for cell in scene.grid:
        if cell.brightness > 0.15:
            curvature = (cell.brightness - 0.5) * 1.5
            cell.add_curve(
                start="bottom_left", end="top_right",
                curvature=curvature,
                width=0.5 + cell.brightness * 2,
                color=cell.color,
                opacity=0.4 + cell.brightness * 0.5,
            )
    save(scene, "recipes/flow-escher-curves.svg")

    # --- 5. Cross-hatching with varying angles ---
    colors = Palette.paper()
    scene = Scene.with_grid(cols=16, rows=12, cell_size=20, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        # First set of lines
        cell.add_line(
            start=(0.1, 0.1), end=(0.9, 0.9),
            width=0.5 + t * 1.5,
            color=colors.primary,
            opacity=0.3 + t * 0.4,
        )
        # Second set: perpendicular
        cell.add_line(
            start=(0.9, 0.1), end=(0.1, 0.9),
            width=0.3 + (1 - t) * 1,
            color=colors.secondary,
            opacity=0.2 + (1 - t) * 0.3,
        )
    save(scene, "recipes/flow-crosshatch.svg")
