
# EntityGroup — Reusable Shapes

**Difficulty**: ⭐⭐ Intermediate

Define composite shapes once and place them like any entity — `cell.place()`, `scene.add()`, `fit_to_cell()` all work.

---

## What You'll Learn

- Creating reusable shapes with `EntityGroup`
- Placing groups with `cell.place()`, `cell.add_entity()`, and `scene.add()`
- Auto-sizing with `fit_to_cell()`
- Writing factory functions for parameterized shapes
- Nesting groups inside groups

---

## Final Result

![Grid Stamps](../_images/groups/03_grid_stamps.svg)

### More Examples

| Flower Pattern | Shape Library | Grid Stamps | Nested Groups |
|---------------|---------------|-------------|---------------|
| ![1](../_images/groups/01_flower_pattern.svg) | ![2](../_images/groups/02_shape_library.svg) | ![3](../_images/groups/03_grid_stamps.svg) | ![4](../_images/groups/04_nested_groups.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette, EntityGroup, Dot
import math

def make_flower(color="coral", petal_color="gold", petal_count=8):
    """Create a flower EntityGroup."""
    g = EntityGroup()
    g.add(Dot(0, 0, radius=10, color=color))
    for i in range(petal_count):
        angle = i * (2 * math.pi / petal_count)
        g.add(Dot(15 * math.cos(angle), 15 * math.sin(angle), radius=6, color=petal_color))
    return g

colors = Palette.midnight()
scene = Scene.with_grid(cols=8, rows=6, cell_size=40)
scene.background = colors.background

for cell in scene.grid:
    flower = make_flower(
        color=colors.primary,
        petal_color=colors.accent,
        petal_count=6 + (cell.col % 3) * 2,
    )
    cell.place(flower)
    flower.fit_to_cell(0.75)

scene.save("groups.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Define an EntityGroup

Add entities positioned relative to `(0, 0)` — the group's local origin:

```python
from pyfreeform import EntityGroup, Dot
import math

flower = EntityGroup()

# Center dot at the origin
flower.add(Dot(0, 0, radius=10, color="coral"))

# Petals around the center
for i in range(8):
    angle = i * (2 * math.pi / 8)
    x = 15 * math.cos(angle)
    y = 15 * math.sin(angle)
    flower.add(Dot(x, y, radius=6, color="gold"))
```

**What's happening:**

- `EntityGroup()` creates an empty group at position `(0, 0)`
- `group.add(entity)` adds a child — its position is relative to the group's origin
- The group is not rendered yet — it's just a definition

---

### Step 2: Place It

EntityGroup behaves like any entity. All standard placement methods work:

![Flower Pattern](../_images/groups/01_flower_pattern.svg)

```python
# Place at an absolute position
scene.add(flower.move_to(100, 100))

# Place centered in a cell
cell.place(flower)

# Same thing, add_* naming convention
cell.add_entity(flower)

# Place at a specific position within a cell
cell.add_entity(flower, at="top_left")
cell.add_entity(flower, at=(0.3, 0.7))
```

**What's happening:**

- `scene.add(group)` adds the group to the scene at its current position
- `cell.place(group)` sets the group's position to the cell center and registers it
- `cell.add_entity(group)` is an alias for `place()` that matches the `add_*` naming convention
- The SVG output wraps children in `<g transform="translate(x, y)">` — children are never mutated

---

### Step 3: Auto-Size with fit_to_cell

`fit_to_cell()` scales the group to fit within its cell bounds, just like any entity:

![Grid Stamps](../_images/groups/03_grid_stamps.svg)

```python
scene = Scene.with_grid(cols=8, rows=6, cell_size=40)
scene.background = colors.background

for cell in scene.grid:
    flower = make_flower(color=colors.primary, petal_color=colors.accent)
    cell.place(flower)
    flower.fit_to_cell(0.75)  # Scale to 75% of cell size
```

**What's happening:**

- `fit_to_cell(0.75)` computes the group's bounding box, calculates the scale needed to fit within 75% of the cell, and applies it
- The group's internal scale factor adjusts the SVG `<g>` transform — children are not modified
- This works identically to calling `fit_to_cell()` on a Dot, Ellipse, or any other entity

---

### Step 4: Factory Functions for Reuse

Wrap `EntityGroup` creation in a function for parameterized reuse. Each call returns a new independent instance:

![Shape Library](../_images/groups/02_shape_library.svg)

```python
def make_flower(color="coral", petal_color="gold", petal_count=8):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=10, color=color))
    for i in range(petal_count):
        angle = i * (2 * math.pi / petal_count)
        g.add(Dot(15 * math.cos(angle), 15 * math.sin(angle), radius=6, color=petal_color))
    return g

def make_ring(radius=20, count=8, dot_radius=3, color="teal"):
    g = EntityGroup()
    for i in range(count):
        angle = i * (2 * math.pi / count)
        g.add(Dot(radius * math.cos(angle), radius * math.sin(angle),
                   radius=dot_radius, color=color))
    return g

def make_star_burst(count=12, radius=20, color="white"):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=3, color=color))
    for i in range(count):
        angle = i * (2 * math.pi / count)
        g.add(Dot(radius * math.cos(angle), radius * math.sin(angle),
                   radius=2, color=color, opacity=0.6))
    return g

# Use them
scene.add(make_flower(color="coral").move_to(100, 100))
scene.add(make_ring(color="teal").move_to(250, 100))
scene.add(make_star_burst(color="gold").move_to(100, 200))
```

**What's happening:**

- Each factory function creates a fresh `EntityGroup` — no shared state between placements
- Parameters control colors, counts, sizes — full customization per instance
- Build a library of shapes and mix them freely

---

### Step 5: Nesting Groups

EntityGroup can contain other EntityGroups. Build complex shapes from simpler ones:

![Nested Groups](../_images/groups/04_nested_groups.svg)

```python
def make_bouquet(center_color, petal_colors):
    bouquet = EntityGroup()

    # Center flower
    center = make_flower(color=center_color, petal_color=petal_colors[0])
    bouquet.add(center)

    # Surrounding flowers (smaller, offset)
    for i in range(5):
        angle = i * (2 * math.pi / 5)
        outer = make_flower(
            color=petal_colors[i % len(petal_colors)],
            petal_color=center_color,
            petal_count=6,
        )
        outer.scale(0.6)
        outer.move_to(45 * math.cos(angle), 45 * math.sin(angle))
        bouquet.add(outer)

    return bouquet

scene.add(make_bouquet(colors.primary, [colors.accent, colors.secondary]).move_to(200, 150))
```

**What's happening:**

- `bouquet.add(center)` adds a flower EntityGroup as a child of the bouquet EntityGroup
- `outer.scale(0.6)` scales the outer flowers before adding them — this adjusts the SVG scale transform
- `outer.move_to(x, y)` offsets each outer flower from the bouquet center
- The resulting SVG nests `<g>` elements: the bouquet `<g>` contains each flower's `<g>`

---

## EntityGroup vs CellGroup

PyFreeform has two kinds of "groups" — they solve different problems:

| | EntityGroup | CellGroup |
|-|------------|-----------|
| **Purpose** | Reusable composite shapes | Multi-cell surface regions |
| **Inherits from** | `Entity` | `Surface` |
| **Created by** | Direct construction | `grid.merge()` |
| **Has** | Child entities | Builder methods (add_dot, add_text, ...) |
| **Placement** | `cell.place()`, `scene.add()` | Already positioned by its cells |
| **Use for** | Custom shapes, stamps, patterns | Headers, sidebars, multi-cell labels |

```python
# EntityGroup — reusable shape
flower = EntityGroup()
flower.add(Dot(0, 0, radius=10, color="coral"))
cell.place(flower)

# CellGroup — multi-cell region
header = grid.merge_row(0)
header.add_text("Title", font_size=20, color="white")
header.add_border(color="gray", width=2)
```

---

## Try It Yourself

### Experiment 1: Crosshair Markers

```python
from pyfreeform import EntityGroup, Dot, Line

def make_crosshair(size=15, color="white"):
    g = EntityGroup()
    g.add(Line(-size, 0, size, 0, width=1, color=color, opacity=0.5))
    g.add(Line(0, -size, 0, size, width=1, color=color, opacity=0.5))
    g.add(Dot(0, 0, radius=3, color=color))
    return g

for cell in scene.grid:
    if cell.brightness > 0.6:
        cell.place(make_crosshair(color=cell.color))
```

### Experiment 2: Scaled Grid Pattern

```python
for cell in scene.grid:
    shape = make_flower(color=colors.primary, petal_color=colors.accent)
    cell.place(shape)
    shape.fit_to_cell(0.3 + cell.brightness * 0.5)
```

### Experiment 3: Random Composition

```python
import random

shape_factories = [make_flower, make_ring, make_star_burst]

for cell in scene.grid:
    factory = random.choice(shape_factories)
    shape = factory(color=colors.primary)
    cell.place(shape)
    shape.fit_to_cell(0.7)
```

---

## API Reference

### EntityGroup

```python
from pyfreeform import EntityGroup

# Create
g = EntityGroup(x=0, y=0, z_index=0)

# Add children (positioned relative to 0, 0)
g.add(entity)

# Properties
g.children      # list of child entities (copy)
g.bounds()      # (min_x, min_y, max_x, max_y) in absolute coords
g.anchor_names  # ["center"]

# Placement (inherited from Entity)
scene.add(g)                    # add to scene
cell.place(g)                   # center in cell
cell.add_entity(g, at="center") # same as place, add_* naming
g.move_to(x, y)                 # move to absolute position
g.move_by(dx, dy)               # move by offset

# Transforms
g.scale(factor)                 # scale group
g.scale(factor, origin=point)   # scale around a point
g.fit_to_cell(0.85)             # auto-scale to fit cell

# Connections (inherited from Entity)
conn = g.connect(other_entity, style={"color": "white", "width": 1})
scene.add(conn)
```

### Surface.add_entity()

```python
# Works on Cell, CellGroup, and Scene — accepts any Entity type
cell.add_entity(dot, at="center")
cell.add_entity(group, at=(0.3, 0.7))
scene.add_entity(rect, at="top_left")
```

---

## Best Practices

### 1. Use Factory Functions for Reusable Shapes

```python
def make_shape(color="coral", size=10):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=size, color=color))
    return g

# Each call returns a new independent instance
cell1.place(make_shape(color="red"))
cell2.place(make_shape(color="blue"))
```

### 2. Use fit_to_cell() for Auto-Sizing

```python
for cell in scene.grid:
    shape = make_shape()
    cell.place(shape)
    shape.fit_to_cell(0.75)  # Consistent sizing across all cells
```

### 3. Compose Complex Shapes from Simple Ones

```python
def make_complex():
    g = EntityGroup()
    g.add(make_simple_a())                    # center
    g.add(make_simple_b().move_to(30, 0))     # right
    g.add(make_simple_b().move_to(-30, 0))    # left
    return g
```

### 4. Z-Index Works at the Group Level

```python
background = make_ring(color="gray")
background.z_index = 0

foreground = make_flower(color="coral")
foreground.z_index = 10

cell.place(background)
cell.place(foreground)
```

---

## Related

- [Entities](../../fundamentals/03-entities.md) — Entity types and properties
- [Grids and Cells](../../fundamentals/02-grids-and-cells.md) — Cell placement and grid access
- [Fit to Cell](../../advanced-concepts/05-fit-to-cell.md) — Auto-scaling entities
- [Multi-Layer Example](../advanced/multi-layer.md) — Complex layered compositions
