# Your First Artwork

PyFreeform gives you two ways to create art: from an image or from scratch. Both use the same powerful grid system.

=== "From an Image"

    ## Load an Image

    `Scene.from_image()` divides a photo into a grid of cells. Each cell knows the **color** and **brightness** of the pixels beneath it.

    ```python
    from pyfreeform import Scene

    scene = Scene.from_image("MonaLisa.jpg", grid_size=35, cell_size=12)

    for cell in scene.grid:
        cell.add_dot(radius=3, color=cell.color)  # (1)!

    scene.save("artwork.svg")
    ```

    1. `cell.color` is the hex color sampled from the image at this cell's position.

    <figure markdown>
    ![Step 1: uniform dots with image colors](../_images/getting-started/first-image-step1.svg){ width="420" }
    <figcaption>Every cell gets a dot colored by the image — already recognizable!</figcaption>
    </figure>

    ## Size by Brightness

    Make bright areas pop and dark areas recede by tying dot radius to brightness:

    ```python
    for cell in scene.grid:
        radius = cell.brightness * 5  # (1)!
        if radius > 0.3:
            cell.add_dot(radius=radius, color=cell.color)
    ```

    1. `cell.brightness` is a float from 0.0 (black) to 1.0 (white).

    <figure markdown>
    ![Step 2: brightness-driven dot sizes](../_images/getting-started/first-image-step2.svg){ width="420" }
    <figcaption>Larger dots in bright areas create depth and dimension.</figcaption>
    </figure>

    ## Polish It

    Add a subtle border and vary opacity for a finished look:

    ```python
    scene = Scene.from_image("MonaLisa.jpg", grid_size=40, cell_size=11)

    for cell in scene.grid:
        radius = cell.brightness * 5
        if radius > 0.3:
            cell.add_dot(
                radius=radius,
                color=cell.color,
                opacity=0.6 + cell.brightness * 0.4,
            )

    for cell in scene.grid.border():  # (1)!
        cell.add_border(color="#333344", width=0.3)

    scene.save("artwork.svg")
    ```

    1. `grid.border()` selects only the cells on the grid's outer edge.

    <figure markdown>
    ![Step 3: polished with border and opacity](../_images/getting-started/first-image-step3.svg){ width="420" }
    <figcaption>Opacity variation and a border frame give it a gallery-ready feel.</figcaption>
    </figure>

=== "From Scratch"

    ## Start with a Grid

    `Scene.with_grid()` creates an empty grid — no image needed. Use position and math to drive the visuals.

    ```python
    from pyfreeform import Scene, Palette

    colors = Palette.sunset()
    scene = Scene.with_grid(cols=12, rows=12, cell_size=25, background=colors.background)

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.7)
        else:
            cell.add_fill(color=colors.secondary, opacity=0.3)

    scene.save("pattern.svg")
    ```

    <figure markdown>
    ![Step 1: checkerboard fills](../_images/getting-started/first-scratch-step1.svg){ width="320" }
    <figcaption>A warm checkerboard using the Sunset palette.</figcaption>
    </figure>

    ## Add Shapes

    Use `cell.normalized_position` to drive size, rotation, and opacity based on where each cell sits in the grid:

    ```python
    from pyfreeform import Polygon

    for cell in scene.grid:
        nx, ny = cell.normalized_position  # (1)!
        t = (nx + ny) / 2
        cell.add_polygon(
            Polygon.diamond(size=0.3 + t * 0.5),
            fill=colors.accent,
            opacity=0.4 + t * 0.6,
            rotation=t * 45,
        )
    ```

    1. `normalized_position` returns (nx, ny) where both values range from 0.0 (top-left) to 1.0 (bottom-right).

    <figure markdown>
    ![Step 2: diamonds growing across the grid](../_images/getting-started/first-scratch-step2.svg){ width="320" }
    <figcaption>Diamonds that grow and rotate from corner to corner.</figcaption>
    </figure>

    ## Layer Curves for Flow

    Stack curves on top for an organic finish:

    ```python
    import math

    for cell in scene.grid:
        nx, ny = cell.normalized_position
        curvature = math.sin(nx * math.pi * 2) * 0.6
        cell.add_curve(
            start="left", end="right",
            curvature=curvature,
            width=0.8,
            color=colors.line,
            opacity=0.3 + ny * 0.4,
        )
    ```

    <figure markdown>
    ![Step 3: curves layered on diamonds](../_images/getting-started/first-scratch-step3.svg){ width="320" }
    <figcaption>Curves add rhythm and movement to the geometric base.</figcaption>
    </figure>

---

## What's Next?

You've seen how PyFreeform turns a few lines of code into visual art. Now learn the concepts behind it:

[How PyFreeform Works &rarr;](03-how-it-works.md){ .md-button }
