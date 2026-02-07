
# Scene API Reference

Complete API documentation for the Scene class.

## Class: Scene

Main container for all drawable objects. Scene inherits from **Surface**, giving it the same builder methods as Cell and CellGroup.

### Constructor

```python
Scene(width: int, height: int, background: str | None = None)
```

![Constructor Example](./_images/scene/example1-constructor.svg)

### Factory Methods

```python
@classmethod
Scene.from_image(
    source,
    grid_size=40,         # Number of columns (None = fit grid to image)
    cell_size=10,
    cell_ratio=1.0,       # Width:height ratio (2.0 = domino cells)
    cell_width=None,      # Explicit cell width (overrides cell_size/cell_ratio)
    cell_height=None,     # Explicit cell height (overrides cell_size)
    background=None
)

@classmethod
Scene.with_grid(
    cols=30,
    rows=None,            # Defaults to cols (square grid)
    cell_size=10,
    cell_width=None,      # Explicit cell width (overrides cell_size)
    cell_height=None,     # Explicit cell height (overrides cell_size)
    background=None
)
```

**`grid_size` modes**:
- `grid_size=40` (default): 40 columns, rows auto-calculated from aspect ratio. Scene size = cols × cell_size × rows × cell_size.
- `grid_size=None`: Grid fits the image. Cols/rows derived from image dimensions ÷ cell size.

![Scene from Image](./_images/scene/example2-from-image.svg)

![Scene with Grid](./_images/scene/example3-with-grid.svg)

### Properties

- `width: int` - Scene width in pixels
- `height: int` - Scene height in pixels
- `background: str | None` - Background color
- `grid: Grid | None` - Primary grid
- `entities: list[Entity]` - All entities
- `connections: list[Connection]` - All connections

Position properties (inherited from Surface):

- `center: Point` - Center of the canvas
- `top_left: Point` - Top-left corner
- `top_right: Point` - Top-right corner
- `bottom_left: Point` - Bottom-left corner
- `bottom_right: Point` - Bottom-right corner
- `bounds: tuple` - (x, y, width, height)

![Scene Properties](./_images/scene/example4-properties.svg)

---

## Builder Methods (Surface Protocol)

Scene inherits all builder methods from Surface. Named positions, relative coordinates, and `along=`/`t=` work at the scene level — the same API you use inside cells.

```python
scene = Scene(400, 300, background="#0f172a")

# Scene-level curve with along= positioning
curve = scene.add_curve(start="left", end="right", curvature=0.4, color="#334155", width=2)

# Place dots along the curve — works at scene level!
scene.add_dot(along=curve, t=0.25, radius=12, color="#f43f5e")
scene.add_dot(along=curve, t=0.50, radius=12, color="#22c55e")
scene.add_dot(along=curve, t=0.75, radius=12, color="#3b82f6")
```

![Scene Builder Methods](./_images/scene/example5-scene-builders.svg)

| Method | Description |
|---|---|
| `add_dot(at=, along=, t=, align=, radius=, color=)` | Add a dot |
| `add_line(start=, end=, along=, t=, align=, width=, color=)` | Add a line |
| `add_curve(start=, end=, along=, t=, align=, curvature=, width=, color=)` | Add a curve |
| `add_text(content, at=, along=, t=, font_size=, color=)` | Add text (along= without t= warps via textPath) |
| `add_rect(at=, along=, t=, align=, width=, height=, fill=)` | Add a rectangle |
| `add_ellipse(at=, along=, t=, align=, rx=, ry=, fill=)` | Add an ellipse |
| `add_polygon(vertices, along=, t=, align=, fill=)` | Add a polygon |
| `add_fill(color=)` | Fill the entire scene |
| `add_border(color=, width=)` | Border around the scene |
| `add_diagonal(along=, t=, align=, ...)` | Add a diagonal line |

---

## Methods

### add()

```python
def add(self, *objects: Entity | Connection | Grid) -> Entity | Connection | Grid
```

Add pre-constructed entities, connections, or grids to the scene. For convenience, prefer the builder methods above.

**Parameters**:
- `*objects`: One or more Entity, Connection, or Grid objects

**Returns**: The last added object (for method chaining)

![Add Connection Example](./_images/scene/example6-add-connection.svg)

### remove()

```python
def remove(self, obj: Entity | Connection | Grid) -> bool
```

Remove an object from the scene.

**Returns**: True if object was found and removed, False otherwise

### clear()

```python
def clear(self) -> None
```

Remove all objects from the scene (entities, connections, and grids).

### save()

```python
def save(self, path: str) -> None
```

Save the scene as an SVG file.

### to_svg()

```python
def to_svg(self) -> str
```

Generate SVG markup as a string (without saving to file).

### Iteration Support

```python
for entity in scene:
    print(entity)

num_entities = len(scene)
```

---

## Complete Example

Grid-based art with scene-level overlays:

```python
scene = Scene.with_grid(cols=15, rows=10, cell_size=20, background="#1a1a2e")

# Cell-level art
for cell in scene.grid:
    cell.add_dot(color=colors.primary, radius=2)

# Scene-level overlay — same builder API!
scene.add_text("Scene API Demo", at=(0.5, 0.12), font_size=18, color="#ffd23f")

curve = scene.add_curve(start="bottom_left", end="bottom_right",
                        curvature=-0.3, color="#4ecca3", width=2)
for i in range(5):
    scene.add_dot(along=curve, t=(i + 0.5) / 5, radius=4, color="#ffd23f")
```

![Complete Scene](./_images/scene/example7-complete.svg)

---

## See Also
- [Scenes Guide](../fundamentals/01-scenes.md)
- [Surface Protocol](../advanced-concepts/07-surface-protocol.md) - The unifying abstraction
- [Grid API](grid.md)
- [CellGroup](../advanced-concepts/07-surface-protocol.md#cell-merging-with-gridmerge)
