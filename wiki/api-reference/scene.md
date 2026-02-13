# Scene

Everything starts with a `Scene`. It is the canvas -- it holds your artwork and renders it to SVG.

!!! info "See also"
    For a hands-on walkthrough of creating scenes, see [Scenes and Grids](../guide/01-scenes-and-grids.md).

---

## Three Ways to Create a Scene

| Constructor | Use Case | Returns |
|---|---|---|
| `Scene(width, height, background=None)` | Manual canvas, no grid | Scene |
| `Scene.from_image(source, *, grid_size=40, cell_size=10, ...)` | Image-based art | Scene with grid |
| `Scene.with_grid(*, cols=30, rows=None, cell_size=10, ...)` | Grid-based art, no image | Scene with grid |

**`Scene.from_image()`** is the flagship -- load a photo, get a grid where every cell knows the color and brightness of the pixel it overlays.

**`Scene.with_grid()`** gives you the same grid structure but with no image data (cells default to brightness 0.5, color "#808080").

**`Scene(w, h)`** is for freeform art -- you place entities at absolute positions, no grid involved.

## Scene Properties

| Property | Type | Description |
|---|---|---|
| `scene.width` | `int` | Canvas width in pixels |
| `scene.height` | `int` | Canvas height in pixels |
| `scene.background` | `str \| None` | Background color (default: `"#1a1a2e"` midnight blue) |
| `scene.grid` | `Grid` | The primary grid (raises `ValueError` if none) |
| `scene.grids` | `list[Grid]` | All grids in the scene |
| `scene.entities` | `list[Entity]` | All entities (including those inside grid cells) |
| `scene.connections` | `list[Connection]` | All connections |

## Scene Methods

| Method | Description |
|---|---|
| `scene.add(entity, at=)` | Add an entity with relative positioning (inherited from Surface). |
| `scene.place(entity)` | Add an entity at its current pixel position (inherited from Surface). |
| `scene.add_grid(grid)` | Add a grid to the scene. |
| `scene.remove(entity)` | Remove an entity. Returns `True` if found. |
| `scene.remove_grid(grid)` | Remove a grid. Returns `True` if found. |
| `scene.clear()` | Remove everything. |
| `scene.to_svg()` | Render to SVG string. |
| `scene.save(path)` | Save to `.svg` file (adds extension if missing). |
| `scene.crop(padding=0)` | Crop viewBox to fit content bounds. Great for transparent exports. |
| `scene.trim(top=0, right=0, bottom=0, left=0)` | Remove pixels from edges of the scene. Chainable with `crop()`. |

## `from_image()` Full Signature

??? note "Expand full signature"

    ```python
    Scene.from_image(
        source: str | Path | Image,   # File path or Image object
        *,
        grid_size: int | None = 40,   # Columns (rows auto from aspect ratio)
        cell_size: int = 10,          # Base cell size in pixels
        cell_ratio: float = 1.0,      # Width-to-height ratio (2.0 = domino)
        cell_width: float | None,     # Explicit cell width (overrides cell_size)
        cell_height: float | None,    # Explicit cell height (overrides cell_size)
        background: str | None,       # Background color (default "#1a1a2e")
    ) -> Scene
    ```

Two modes:

- **`grid_size=N`** (default): N columns, rows calculated from image aspect ratio. Scene dimensions = grid * cell_size.
- **`grid_size=None`**: Grid fits the image dimensions. Columns/rows derived from `image.width / cell_size`.

## `with_grid()` Full Signature

??? note "Expand full signature"

    ```python
    Scene.with_grid(
        *,
        cols: int = 30,               # Columns
        rows: int | None = None,      # Rows (defaults to cols for square)
        cell_size: int = 10,          # Base cell size in pixels
        cell_width: float | None,     # Explicit cell width
        cell_height: float | None,    # Explicit cell height
        background: str | None,       # Background color (default "#1a1a2e")
    ) -> Scene
    ```
