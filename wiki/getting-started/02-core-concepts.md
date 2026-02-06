
# Core Concepts

Understanding PyFreeform's core concepts will unlock its full creative potential. Let's explore the fundamental building blocks: Scene, Grid, Cell, and Entity.

---

## The Mental Model

!!! info "The Hierarchy"
    Think of creating art with PyFreeform like painting on an organized canvas:

    ```
    Scene                    (The canvas)
      └─ Grid                (Spatial organization)
           └─ Cell           (Individual units)
                └─ Entity    (Things you draw)
    ```

    Each level provides structure and convenience for the next.

---

## 1. Scene: Your Canvas

The **Scene** is the top-level container for your artwork. It defines:
- Canvas dimensions (width × height)
- Background color
- The primary grid (if using one)
- All entities that will be rendered

### Creating Scenes

There are three ways to create a scene:

#### From an Image (Most Common)
```python
scene = Scene.from_image("photo.jpg", grid_size=40)
```

![Scene from image](./_images/02-core-concepts/01-scene-from-image.svg)

- Loads image data into grid cells
- Scene dimensions match the image
- Cells contain color and brightness information

#### With an Empty Grid
```python
scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
```

![Scene with grid](./_images/02-core-concepts/02-scene-with-grid.svg)

- Creates an empty organized grid
- Perfect for algorithmic/generative art
- Scene size = cols × cell_width, rows × cell_height

#### Manually
```python
scene = Scene(width=800, height=600, background="white")

# Scene is a Surface — use builder methods directly!
scene.add_dot(at=(0.5, 0.5), radius=50, color="#f59e0b")
scene.add_ellipse(at=(0.75, 0.33), rx=80, ry=40, fill="#10b981")
scene.add_line(start=(0.125, 0.17), end=(0.875, 0.83), color="#ef4444", width=3)
```

![Scene manual](./_images/02-core-concepts/03-scene-manual.svg)

- Complete control — same builder API as cells
- Named positions and relative coordinates work at scene level
- Good for freeform compositions

---

## 2. Grid: Spatial Organization

A **Grid** divides your canvas into organized cells. Think of it like graph paper - each cell is a coordinate unit you can work with.

### Why Use Grids?

!!! tip "Benefits of Grids"
    Grids provide:

    - **Organization**: Structured layout for systematic artwork
    - **Image Mapping**: Each cell can hold image data
    - **Iteration**: Easy loops over cells
    - **Neighbors**: Built-in access to adjacent cells

### Accessing Cells

```python
# By index (row, column)
cell = scene.grid[10, 5]

# Iterate all cells
for cell in scene.grid:
    # Do something with each cell
    pass

# Get dimensions
cols = scene.grid.cols
rows = scene.grid.rows
total = len(scene.grid)  # cols × rows
```

![Cell access](./_images/02-core-concepts/04-cell-access.svg)

---

## 3. Cell: The Building Block

A **Cell** is an individual unit in the grid. It's both a container and a workspace:

### Cell Properties

Each cell knows about:

```python
# Position in grid
cell.row                 # 0 to rows-1
cell.col                 # 0 to cols-1

# Physical dimensions
cell.x, cell.y          # Top-left corner (pixels)
cell.width, cell.height  # Size (pixels)
cell.center             # Center point

# Position helpers
cell.top_left           # Point at top-left
cell.top_right          # Point at top-right
cell.bottom_left        # Point at bottom-left
cell.bottom_right       # Point at bottom-right

# Image data (when loaded from image)
cell.brightness         # 0.0 to 1.0
cell.color             # Hex color "#rrggbb"
cell.rgb               # Tuple (r, g, b)

# Neighbors
cell.above             # Cell above
cell.below             # Cell below
cell.left              # Cell to the left
cell.right             # Cell to the right
```

### Builder Methods

Cells provide convenient methods to add entities:

```python
cell.add_dot(radius=5, color="red")
cell.add_line(start="top_left", end="bottom_right")
cell.add_curve(curvature=0.5, color="blue")
cell.add_ellipse(rx=10, ry=8, fill="coral")
cell.add_polygon(vertices, fill="purple")
cell.add_text("Hello", font_size=14)
cell.add_fill(color="lightgray")
cell.add_border(color="black", width=1)
```

![Cell properties](./_images/02-core-concepts/05-cell-properties.svg)

These methods:
- Create entities positioned relative to the cell
- Accept named positions like "center", "top_left"
- Return the created entity for further manipulation

---

## 4. Entity: What You Draw

An **Entity** is anything you can draw: dots, lines, curves, ellipses, polygons, text, etc.

### Common to All Entities

Every entity has:

```python
# Position
entity.position         # Point(x, y)
entity.x, entity.y      # Coordinate access

# Layering
entity.z_index         # Controls render order

# Movement
entity.move_to(x, y)   # Absolute positioning
entity.move_by(dx, dy) # Relative offset
entity.translate(dx, dy)  # Same as move_by

# Transforms
entity.rotate(angle)   # Degrees, counterclockwise
entity.scale(factor)   # Resize

# Anchors
entity.anchor("center")  # Get named reference point
entity.anchor_names      # List available anchors

# Data
entity.data            # Custom dictionary for your data
```

### Entity Types

PyFreeform provides these built-in entities:

- **Dot**: Simple filled circle
- **Line**: Straight path between points
- **Curve**: Smooth Bézier curve
- **Ellipse**: Oval or circle
- **Polygon**: Custom or built-in shapes
- **Text**: Labels and typography
- **Rect**: Rectangles with fill and stroke

Each type has specific properties and methods. See [Entities](../entities/) for details on each.

---

## How They Work Together

Here's a complete example showing all concepts:

```python
from pyfreeform import Scene, Palette

# 1. Create Scene with Grid
scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background

# 2. Work with Cells and Entities
for cell in scene.grid:
    # Cell knows its brightness from the image
    if cell.brightness > 0.7:
        # Add a large dot entity in bright areas
        dot = cell.add_dot(radius=8, color=colors.primary)

    elif cell.brightness > 0.4:
        # Add a curve entity in medium areas
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.5,
            color=colors.secondary
        )
        # Add smaller dot along the curve
        cell.add_dot(
            along=curve,
            t=cell.brightness,
            radius=3,
            color=colors.accent
        )

    else:
        # Add border in dark areas
        cell.add_border(color=colors.line, width=0.5)

# 3. Scene renders all entities
scene.save("artwork.svg")
```

![Complete workflow](./_images/02-core-concepts/06-complete-workflow.svg)

This example:
- Creates a scene from an image
- Iterates cells in the grid
- Uses cell properties (brightness) to make decisions
- Creates entities with different configurations
- Entities are automatically added to the scene
- Scene renders everything to SVG

---

## The Flow of Creation

1. **Create Scene** - Define your canvas
2. **Access Grid** - Work with organized cells (or create entities directly)
3. **Use Cell Data** - Let image data or position drive your art
4. **Add Entities** - Create visual elements
5. **Transform & Style** - Adjust properties, move, rotate, scale
6. **Save** - Export to SVG

---

## Coordinate Systems

PyFreeform uses several coordinate systems:

### Absolute (Pixels)
Used by Entity positions:
- Origin (0, 0) is top-left
- Positive x goes right
- Positive y goes down
- Example: `entity.move_to(100, 200)`

### Relative (0-1)
Used within any Surface (cells, scene, merged groups):
- (0, 0) is surface's top-left
- (1, 1) is surface's bottom-right
- (0.5, 0.5) is surface's center
- Example: `cell.add_dot(at=(0.75, 0.25))`
- Example: `scene.add_dot(at="center")`

### Parametric (0-1)
Used for positioning along paths — works on any Surface:
- 0 = start of path
- 1 = end of path
- 0.5 = midpoint
- Example: `cell.add_dot(along=curve, t=0.5)`
- Example: `scene.add_dot(along=curve, t=0.5)` — works at scene level too!

![Coordinate systems](./_images/02-core-concepts/07-coordinate-systems.svg)

---

## Key Takeaways

!!! note "Remember These Concepts"
    1. **Scene** is your canvas — it contains everything
    2. **Grid** provides organization — optional but powerful
    3. **Cell** is a workspace — position, data, and builders
    4. **Entity** is what you draw — dots, lines, curves, etc.
    5. **Surface** is the unifying idea — Scene, Cell, and CellGroup all share the same builder API (`add_dot`, `add_line`, `add_curve`, etc.)

    Understanding these concepts makes everything else in PyFreeform intuitive!

---

## Next Steps

Now that you understand the core concepts:

- **Apply them**: Try the [Image to Art Guide](03-image-to-art.md)
- **Go deeper**: Read about [Scenes](../fundamentals/01-scenes.md)
- **See examples**: Browse [Examples](../examples/index.md)
- **Learn entities**: Explore [Entities](../entities/01-dots.md)

---

## See Also

- 📖 [Scenes](../fundamentals/01-scenes.md) - Deep dive into Scene API
- 📖 [Grids and Cells](../fundamentals/02-grids-and-cells.md) - Grid system details
- 📖 [Entities](../fundamentals/03-entities.md) - Entity system overview
- 🎯 [Grid Patterns Example](../examples/beginner/grid-patterns.md) - Using grids

