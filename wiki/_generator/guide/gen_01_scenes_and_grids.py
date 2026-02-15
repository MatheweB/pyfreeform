"""Generate SVGs for Guide: Scenes and Grids."""

from pyfreeform import Scene, Palette, Polygon

from wiki._generator import save, sample_image


def generate():
    colors = Palette.midnight()

    # --- 1. Grid size comparison (20, 40, 60) ---
    for grid_size in [20, 40, 60]:
        scene = Scene.from_image(
            sample_image("MonaLisa.jpg"),
            grid_size=grid_size,
            cell_size=10,
        )
        for cell in scene.grid:
            r = cell.brightness * 0.45
            if r > 0.03:
                cell.add_dot(radius=r, color=cell.color)
        save(scene, f"guide/scenes-grid-size-{grid_size}.svg")

    # --- 2. Cell ratio comparison ---
    for ratio, label in [(1.0, "square"), (2.0, "wide"), (0.5, "tall")]:
        scene = Scene.from_image(
            sample_image("MonaLisa.jpg"),
            grid_size=30,
            cell_ratio=ratio,
            cell_size=10,
        )
        for cell in scene.grid:
            cell.add_fill(color=cell.color)
        save(scene, f"guide/scenes-ratio-{label}.svg")

    # --- 3. with_grid basic pattern ---
    scene = Scene.with_grid(cols=15, rows=15, cell_size=22, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        radius = 0.10 + (nx * ny) * 0.35
        cell.add_dot(radius=radius, color=colors.primary, opacity=0.5 + nx * 0.5)
    save(scene, "guide/scenes-with-grid-basic.svg")

    # --- 4. Border selection ---
    scene = Scene.with_grid(cols=12, rows=12, cell_size=24, background=colors.background)
    for cell in scene.grid:
        cell.add_fill(color=colors.background)
    for cell in scene.grid.border(thickness=2):
        cell.add_fill(color=colors.accent, opacity=0.7)
        cell.add_dot(radius=0.15, color=colors.primary)
    save(scene, "guide/scenes-border-selection.svg")

    # --- 5. Checkerboard selection ---
    colors_ocean = Palette.ocean()
    scene = Scene.with_grid(cols=10, rows=10, cell_size=28, background=colors_ocean.background)
    for cell in scene.grid.checkerboard("black"):
        cell.add_polygon(
            Polygon.diamond(size=0.7),
            fill=colors_ocean.primary,
            opacity=0.7,
        )
    for cell in scene.grid.checkerboard("white"):
        cell.add_dot(radius=0.15, color=colors_ocean.accent, opacity=0.5)
    save(scene, "guide/scenes-checkerboard.svg")

    # --- 6. Diagonal selection ---
    scene = Scene.with_grid(cols=12, rows=12, cell_size=22, background=colors.background)
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
    for offset in range(0, 24, 3):
        for cell in scene.grid.diagonal(direction="down", offset=offset):
            cell.add_fill(color=colors.accent, opacity=0.5)
    save(scene, "guide/scenes-diagonal.svg")

    # --- 7. Row and column highlighting ---
    scene = Scene.with_grid(cols=10, rows=10, cell_size=26, background=colors.background)
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
    # Highlight row 3
    for cell in scene.grid.row(3):
        cell.add_fill(color=colors.primary, opacity=0.4)
    # Highlight column 6
    for cell in scene.grid.column(6):
        cell.add_fill(color=colors.accent, opacity=0.4)
    # Intersection gets both — brighter
    scene.grid[3][6].add_fill(color="#ffffff", opacity=0.3)
    scene.grid[3][6].add_dot(radius=0.25, color=colors.accent)
    save(scene, "guide/scenes-row-column.svg")

    # --- 8. Region selection ---
    scene = Scene.with_grid(cols=12, rows=10, cell_size=24, background=colors.background)
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.3, opacity=0.2)
    for cell in scene.grid.region(2, 6, 3, 9):
        nx, ny = cell.normalized_position
        cell.add_fill(color=colors.secondary, opacity=0.3)
        cell.add_polygon(
            Polygon.hexagon(size=0.6),
            fill=colors.primary,
            opacity=0.6,
        )
    save(scene, "guide/scenes-region.svg")

    # --- 9. Merged CellGroup ---
    scene = Scene.with_grid(cols=10, rows=8, cell_size=28, background=colors.background)
    for cell in scene.grid:
        cell.add_border(color=colors.grid, width=0.3, opacity=0.2)
        nx, ny = cell.normalized_position
        cell.add_dot(
            radius=0.05 + nx * 0.15,
            color=colors.secondary,
            opacity=0.3,
        )
    # Merge top row for a title bar
    title_bar = scene.grid.merge_row(0)
    title_bar.add_fill(color=colors.primary, opacity=0.2)
    title_bar.add_text(
        "TITLE BAR",
        at="center",
        font_size=0.50,
        color=colors.accent,
        bold=True,
    )
    save(scene, "guide/scenes-merged-title.svg")
