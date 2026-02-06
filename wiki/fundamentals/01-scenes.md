
# Scenes

The Scene is your canvas - the top-level container that holds everything in your PyFreeform artwork. Understanding scenes is fundamental to creating any artwork.

---

## What is a Scene?

A Scene represents a complete artwork with:
- **Dimensions** - Width and height in pixels
- **Background** - Optional background color
- **Grid** - Optional primary grid for organization
- **Entities** - All drawable elements (dots, lines, curves, etc.)
- **Connections** - Links between entities

Think of it as your digital canvas - everything you create lives in a scene.

---

## Creating Scenes

!!! info "Three Ways to Create Scenes"
    PyFreeform provides three ways to create scenes, each optimized for different workflows:

### 1. From an Image (Recommended for Photo Art)

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=40)
```

**What it does:**
- Loads your image
- Creates a scene matching image dimensions
- Divides into a grid (40×40 by default)
- Loads color and brightness data into cells
- Ready to iterate and create art

**Parameters:**
```python
Scene.from_image(
    source="path/to/image.jpg",  # Image file path
    grid_size=40,                # Grid columns (rows auto-calculated)
    cell_size=10,                # Cell size in pixels
    background=None              # Background color (optional)
)
```

**Example:**
```python
scene = Scene.from_image("photo.jpg", grid_size=50, cell_size=12)

for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(color=cell.color, radius=5)

scene.save("art.svg")
```

**Visual Progression:**

| Step | Description | Output |
|------|-------------|--------|
| 0 | Original image | ![Original Image](./_images/01-scenes/method1-step0-original-image.svg) |
| 1 | Load into scene with grid | ![Empty Grid](./_images/01-scenes/method1-step1-with-grid.svg) |
| 2 | Analyze brightness per cell | ![Brightness Analysis](./_images/01-scenes/method1-step2-grid-and-dots.svg) |
| 3 | Add dots where brightness > 0.5 | ![Complete Dots](./_images/01-scenes/method1-step3-complete-dots.svg) |

**Variations:**

| Variation | Output |
|-----------|--------|
| grid_size=50 (more detail) | ![Grid Size 50 Variation](./_images/01-scenes/method1-variation-grid-size-50.svg) |
| Adjusted cell_size | ![Cell Size Variation](./_images/01-scenes/method1-variation-cell-size.svg) |

### 2. With a Grid (For Generative/Algorithmic Art)

```python
scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
```

!!! note "Perfect for Generative Art"
    **What it does:**

    - Creates an empty scene
    - Sets up a grid with your dimensions
    - Scene size = cols × cell_size, rows × cell_size
    - No image data, perfect for generative patterns

**Parameters:**
```python
Scene.with_grid(
    cols=30,                     # Number of columns
    rows=30,                     # Number of rows
    cell_size=12,                # Size of each cell
    background=None              # Background color
)
```

**Example:**
```python
from pyfreeform import Palette

scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    # Algorithmic pattern based on position
    if (cell.row + cell.col) % 2 == 0:
        cell.add_dot(color=colors.primary, radius=6)

scene.save("pattern.svg")
```

**Visual Progression:**

| Step | Description | Output |
|------|-------------|--------|
| 1 | Empty grid setup | ![Empty Grid](./_images/01-scenes/method2-step1-empty-grid.svg) |
| 2 | Apply checkerboard logic | ![Checkerboard Pattern](./_images/01-scenes/method2-step2-checkerboard.svg) |
| 3 | Complete pattern with colors | ![Full Pattern](./_images/01-scenes/method2-step3-full-pattern.svg) |

**Variations:**

| Variation | Output |
|-----------|--------|
| Different dimensions (cols/rows) | ![Dimensions Variation](./_images/01-scenes/method2-variation-dimensions.svg) |

### 3. Manual (For Freeform Compositions)

```python
scene = Scene(width=800, height=600)
```

**What it does:**
- Creates an empty scene with exact dimensions
- No grid, complete freedom
- Add entities anywhere
- Perfect for non-grid artwork

**Example:**
```python
from pyfreeform import Scene

scene = Scene(width=800, height=600, background="white")

# Scene is a Surface — same builder API as cells!
scene.add_line(start=(0.125, 0.17), end=(0.375, 0.33), color="gray", width=2)
scene.add_dot(at=(0.125, 0.17), radius=20, color="red", z_index=1)
scene.add_dot(at=(0.375, 0.33), radius=20, color="blue", z_index=1)

scene.save("freeform.svg")
```

**Visual Progression:**

| Step | Description | Output |
|------|-------------|--------|
| 1 | Blank canvas (800×600) | ![Blank Canvas](./_images/01-scenes/method3-step1-blank-canvas.svg) |
| 2 | Add first dot | ![Add First Dot](./_images/01-scenes/method3-step2-add-dots.svg) |
| 3 | Add second dot and line | ![Add Second Dot and Line](./_images/01-scenes/method3-step3-add-line.svg) |
| 4 | Complete freeform composition | ![Complete](./_images/01-scenes/method3-step4-complete.svg) |

---

## Scene Properties

### Dimensions

```python
scene.width   # Width in pixels
scene.height  # Height in pixels
```

These are read-only and set during scene creation.

### Background

```python
# Set background color
scene.background = "white"
scene.background = "#f0f0f0"
scene.background = (240, 240, 240)  # RGB tuple

# Remove background (transparent)
scene.background = None
```

The background is rendered first (bottom layer) when saving to SVG.

**Background Examples:**

| Type | Code | Output |
|------|------|--------|
| Named color | `scene.background = "white"` | ![White Background](./_images/01-scenes/properties-background-white.svg) |
| Hex color | `scene.background = "#f0f0f0"` | ![Hex Background](./_images/01-scenes/properties-background-colored.svg) |
| Transparent | `scene.background = None` | ![Transparent Background](./_images/01-scenes/properties-background-none.svg) |

### The Primary Grid

```python
# Access the grid created by from_image() or with_grid()
grid = scene.grid

# Iterate cells
for cell in scene.grid:
    pass

# Access specific cell
cell = scene.grid[row, col]
```

Only available if scene was created with `from_image()` or `with_grid()`.

### Entities and Connections

```python
# All entities in the scene
entities = scene.entities

# All connections between entities
connections = scene.connections
```

These lists are automatically populated when you add entities using cell methods or `scene.add()`.

---

## Adding Content

### Using Cell Methods (Recommended for Grid Art)

When working with grids, use cell builder methods:

```python
for cell in scene.grid:
    cell.add_dot(radius=5, color="red")
    cell.add_line(start="top_left", end="bottom_right")
    cell.add_curve(curvature=0.5)
```

This is the easiest and most intuitive approach for grid-based art.

### Scene Builder Methods

The scene itself has the same builder API as cells — named positions, relative coordinates, and `along=`/`t=` all work:

```python
# Named positions work on the full canvas
scene.add_dot(at="center", radius=20, color="coral")
scene.add_line(start="top_left", end="bottom_right", color="gray")

# along= works at scene level for cross-cell entities
curve = scene.add_curve(start="left", end="right", curvature=0.3, color="blue")
scene.add_dot(along=curve, t=0.5, radius=8, color="red")

# Scene-level text and borders
scene.add_text("My Art", at=(0.5, 0.05), font_size=20, color="white")
scene.add_border(color="white", width=2)
```

### Direct Entity Addition

For precise absolute positioning, you can still construct entities manually:

```python
from pyfreeform import Dot, Line

dot = Dot(x=100, y=200, radius=10, color="coral")
line = Line(x1=0, y1=0, x2=800, y2=600)
scene.add(dot)
scene.add(line)
```

### Adding Connections

Link entities dynamically:

```python
dot1 = cell1.add_dot(color="red")
dot2 = cell2.add_dot(color="blue")

# Create connection
connection = dot1.connect(
    dot2,
    start_anchor="center",
    end_anchor="center",
    style={"width": 2, "color": "gray"}
)

# Add to scene
scene.add(connection)
```

---

## Saving Your Artwork

### Save to SVG

```python
scene.save("artwork.svg")
```

This:
1. Renders all entities sorted by z-index
2. Generates SVG XML
3. Writes to file

### Get SVG String

```python
svg_content = scene.to_svg()
print(svg_content)  # Raw SVG XML
```

Useful for:
- Web applications
- Further processing
- Debugging

---

## Scene Dimensions and Sizing

### From Image

Scene dimensions match the image:

```python
# If photo.jpg is 1200×800 pixels
scene = Scene.from_image("photo.jpg", grid_size=40)

print(scene.width)   # 1200
print(scene.height)  # 800
```

Grid size affects cell count, not scene dimensions.

### With Grid

Scene dimensions calculated from grid:

```python
scene = Scene.with_grid(cols=30, rows=20, cell_size=15)

print(scene.width)   # 30 × 15 = 450
print(scene.height)  # 20 × 15 = 300
```

### Manual

You specify exact dimensions:

```python
scene = Scene(width=1024, height=768)
```

---

## Common Patterns

### Pattern 1: Image-Based Art

```python
scene = Scene.from_image("photo.jpg", grid_size=40)

for cell in scene.grid:
    # Use image data
    if cell.brightness > 0.5:
        cell.add_dot(color=cell.color)

scene.save("photo_art.svg")
```

**Workflow:**

| Step | Description | Output |
|------|-------------|--------|
| 1 | Load image into scene | ![Load Image](./_images/01-scenes/pattern1-step1-load-image.svg) |
| 2 | Process cells based on brightness | ![Process Cells](./_images/01-scenes/pattern1-step2-add-dots.svg) |
| 3 | Final image-based artwork | ![Final](./_images/01-scenes/pattern1-step3-final.svg) |

### Pattern 2: Generative Patterns

```python
from pyfreeform import Palette

scene = Scene.with_grid(cols=25, rows=25, cell_size=16)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Algorithmic logic
    distance = ((cell.row - 12)**2 + (cell.col - 12)**2) ** 0.5
    if distance < 10:
        cell.add_dot(color=colors.primary, radius=7)

scene.save("circle_pattern.svg")
```

**Workflow:**

| Step | Description | Output |
|------|-------------|--------|
| 1 | Create empty grid | ![Empty Grid](./_images/01-scenes/pattern2-step1-empty-grid.svg) |
| 2 | Apply distance calculation | ![Distance Calculation](./_images/01-scenes/pattern2-step2-center-marker.svg) |
| 3 | Add dots within threshold | ![Add Dots](./_images/01-scenes/pattern2-step3-distance-calc.svg) |
| 4 | Complete circular pattern | ![Complete](./_images/01-scenes/pattern2-step4-complete.svg) |

### Pattern 3: Mixed Approach

```python
# Start with image
scene = Scene.from_image("photo.jpg", grid_size=30)

# Add grid-based elements
for cell in scene.grid:
    cell.add_dot(color=cell.color)

# Scene builder methods — no manual coordinate math!
scene.add_text("My Artwork", at=(0.5, 0.1), font_size=24, color="white")
scene.add_border(color="white", width=3)

scene.save("mixed.svg")
```

**Workflow:**

| Step | Description | Output |
|------|-------------|--------|
| 1 | Start with image base | ![Image Base](./_images/01-scenes/pattern3-step1-image-base.svg) |
| 2 | Add grid-based dots | ![Add Grid Dots](./_images/01-scenes/pattern3-step2-add-title.svg) |
| 3 | Add text overlay and border | ![Add Border](./_images/01-scenes/pattern3-step3-add-border.svg) |

---

## Multiple Grids (Advanced)

A scene can have multiple grids:

```python
scene = Scene(width=800, height=600)

# Create multiple grids
grid1 = Grid(cols=20, rows=20, cell_size=10, origin=(0, 0))
grid2 = Grid(cols=10, rows=10, cell_size=20, origin=(400, 300))

# Add grids to the scene
scene.add(grid1)
scene.add(grid2)

# Add entities to each grid
for cell in grid1:
    cell.add_dot(color="red", radius=2)

for cell in grid2:
    cell.add_dot(color="blue", radius=5)
```

The primary grid (`scene.grid`) is the one created by `from_image()` or `with_grid()`.

**Visual Example:**

| Step | Description | Output |
|------|-------------|--------|
| 1 | Create first grid | ![First Grid](./_images/01-scenes/advanced-multiple-grids-step1.svg) |
| 2 | Add second overlapping grid | ![Two Grids](./_images/01-scenes/advanced-multiple-grids-step2.svg) |

---

## Tips and Best Practices

!!! tip "Choose the Right Creation Method"
    - **Image art?** Use `Scene.from_image()`
    - **Patterns/generative?** Use `Scene.with_grid()`
    - **Freeform/custom?** Use `Scene()` manual

### Set Background Early

```python
scene = Scene.from_image("photo.jpg", grid_size=40)
scene.background = "white"  # Set before creating entities
```

### Consider Output Size

!!! warning "Watch Your Grid Size"
    SVG files scale infinitely, but:

    - Larger scenes = more entities = larger file size
    - Grid size affects entity count exponentially (30×30 = 900, 60×60 = 3,600)
    - Start with smaller grids for prototyping

### Scene is Automatic

You rarely need to manage the scene manually:
- Cell methods automatically add entities to scene
- Connections automatically register
- Just save when done!

---

## Next Steps

Now that you understand scenes:

- **Learn about grids**: [Grids and Cells](02-grids-and-cells.md)
- **Explore entities**: [Entities](03-entities.md)
- **See examples**: [Quick Start Example](../examples/beginner/quick-start.md)

---

## See Also

- 📖 [Grids and Cells](02-grids-and-cells.md) - Organizing your canvas
- 📖 [Entities](03-entities.md) - Things you can draw
- 🎯 [Quick Start](../examples/beginner/quick-start.md) - Complete example
- 🎨 [Image to Art Guide](../getting-started/03-image-to-art.md) - Image workflow
- 🔍 [Scene API Reference](../api-reference/scene.md) - Technical details

