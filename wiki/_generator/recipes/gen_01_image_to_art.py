"""Generate SVGs for Recipe: Image-to-Art Portraits."""

from pyfreeform import Scene, Polygon

from wiki._generator import save, sample_image


def generate():
    # --- 1. Classic dot art (white dots on dark) ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=45,
        cell_size=9,
    )
    for cell in scene.grid:
        r = cell.brightness * 0.48
        if r > 0.033:
            cell.add_dot(radius=r, color="#ffffff")
    save(scene, "recipes/image-classic-dots.svg")

    # --- 2. Color dot art (preserve original colors) ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=35,
        cell_size=12,
    )
    for cell in scene.grid:
        r = cell.brightness * 0.45
        if r > 0.025:
            cell.add_dot(
                radius=r,
                color=cell.color,
                opacity=0.7 + cell.brightness * 0.3,
            )
    save(scene, "recipes/image-color-dots.svg")

    # --- 3. Halftone effect (brightness→size, dark bg) ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=50,
        cell_size=8,
    )
    scene.background = "#0a0a0a"
    for cell in scene.grid:
        # Invert: dark areas get large dots (halftone convention)
        r = (1 - cell.brightness) * 0.5
        if r > 0.0375:
            cell.add_dot(radius=r, color="#e0e0e0")
    save(scene, "recipes/image-halftone.svg")

    # --- 4. Line art (diagonal lines, brightness→width) ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=40,
        cell_size=10,
    )
    for cell in scene.grid:
        width = cell.brightness * 3
        if width > 0.2:
            cell.add_diagonal(
                width=width,
                color=cell.color,
                opacity=0.5 + cell.brightness * 0.5,
            )
    save(scene, "recipes/image-line-art.svg")

    # --- 5. Mosaic (color fills with borders) ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=30,
        cell_size=14,
    )
    for cell in scene.grid:
        cell.add_fill(color=cell.color)
        cell.add_border(color="#000000", width=0.5, opacity=0.3)
    save(scene, "recipes/image-mosaic.svg")

    # --- 6. Shape art (shapes chosen by brightness) ---
    scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=30,
        cell_size=14,
    )
    for cell in scene.grid:
        b = cell.brightness
        size = 0.4 + b * 0.4
        if b < 0.3:
            verts = Polygon.square(size=size)
        elif b < 0.6:
            verts = Polygon.hexagon(size=size)
        else:
            verts = Polygon.star(points=6, size=size, inner_ratio=0.5)
        cell.add_polygon(verts, fill=cell.color, opacity=0.6 + b * 0.4)
    save(scene, "recipes/image-shape-art.svg")
