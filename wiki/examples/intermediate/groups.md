
# Example: Groups

**Difficulty**: ⭐⭐ Intermediate

Organize multiple entities into groups for easier management and transformations.

---

## What You'll Learn

- Creating groups of entities
- Transforming entire groups at once
- Layering groups
- Building composite shapes

---

## Final Result

![Flower Groups](../_images/groups/01_flower_groups.svg)

### More Examples

| Flower Groups | Composite Shapes | Radial Groups |
|---------------|------------------|---------------|
| ![Example 1](../_images/groups/01_flower_groups.svg) | ![Example 2](../_images/groups/02_composite_shapes.svg) | ![Example 3](../_images/groups/03_radial_groups.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette, Group
import math

scene = Scene.with_grid(cols=12, rows=10, cell_size=25)
colors = Palette.midnight()
scene.background = colors.background

# Example 1: Flower pattern as a group
def create_flower(center_cell, scale=1.0):
    """Create a flower pattern from dots."""
    group = Group()

    # Center dot
    center = center_cell.add_dot(
        radius=10 * scale,
        color=colors.primary,
        z_index=5
    )
    group.add(center)

    # Petals around center
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        distance = 15 * scale

        x = center_cell.center.x + distance * math.cos(angle)
        y = center_cell.center.y + distance * math.sin(angle)

        from pyfreeform import Dot
        petal = Dot(x=x, y=y, radius=6 * scale, color=colors.accent)
        scene.add(petal)
        group.add(petal)

    return group

# Create flowers
cell1 = scene.grid[2, 2]
flower1 = create_flower(cell1, scale=1.0)
flower1.rotate(15)  # Rotate entire flower

cell2 = scene.grid[2, 8]
flower2 = create_flower(cell2, scale=0.8)
flower2.rotate(-30)

# Example 2: Constellation group
constellation = Group()

# Stars
for cell in scene.grid[6:8, 3:6]:
    dot = cell.add_dot(radius=3, color=colors.secondary, z_index=5)
    constellation.add(dot)

# Connections between stars (simplified)
# ... add connections to group ...

scene.save("groups.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Creating a Group

```python
from pyfreeform import Group

group = Group()
```

**What's happening:**
- `Group()` creates an empty container for entities
- Groups can hold dots, lines, curves, polygons, etc.
- Entities can belong to multiple groups

### Step 2: Adding Entities to Groups

```python
dot1 = cell.add_dot(radius=5, color="red")
dot2 = cell.add_dot(radius=5, color="blue")
line = cell.add_line(start="left", end="right")

group.add(dot1)
group.add(dot2)
group.add(line)
```

**What's happening:**
- `group.add(entity)` adds an entity to the group
- Entities still exist independently in the scene
- Group maintains references for batch operations

### Step 3: Transforming Groups

```python
# Rotate all entities in group
group.rotate(45)

# Scale all entities in group
group.scale(1.5)

# Move all entities in group
group.translate(dx=20, dy=10)
```

**What's happening:**
- Transformations apply to ALL entities in the group
- Rotation happens around the group's centroid
- Can specify custom origin for rotation/scaling

### Step 4: Composite Patterns

```python
def create_arrow(cell, direction=0):
    """Create an arrow pointing in direction (degrees)."""
    group = Group()

    # Arrow shaft (custom rectangle)
    from pyfreeform import Rect
    shaft = Rect(
        x=cell.x,
        y=cell.center.y - cell.height * 0.1,
        width=cell.width * 0.6,
        height=cell.height * 0.2,
        fill=colors.primary
    )
    scene.add(shaft)
    group.add(shaft)

    # Arrowhead (triangle)
    from pyfreeform import shapes
    head = cell.add_polygon(
        shapes.triangle(size=0.4, center=(0.85, 0.5)),
        fill=colors.primary
    )
    head.rotate(90)  # Point right
    group.add(head)

    # Rotate entire arrow
    group.rotate(direction, origin=cell.center)

    return group

# Create arrows pointing different directions
arrow_up = create_arrow(scene.grid[3, 3], direction=270)
arrow_right = create_arrow(scene.grid[3, 6], direction=0)
arrow_down = create_arrow(scene.grid[6, 3], direction=90)
```

**What's happening:**
- Function creates composite shape from multiple entities
- Returns group for further manipulation
- Each arrow can be rotated independently

---

## Try It Yourself

### Experiment 1: Radial Pattern

```python
def create_radial_group(center_cell, count=12):
    """Create radial pattern of lines."""
    group = Group()

    for i in range(count):
        angle = i * (2 * math.pi / count)
        x_end = center_cell.center.x + 30 * math.cos(angle)
        y_end = center_cell.center.y + 30 * math.sin(angle)

        from pyfreeform import Line
        line = Line.from_points(
            start=center_cell.center,
            end=(x_end, y_end),
            color=colors.line,
            width=2
        )
        scene.add(line)
        group.add(line)

    return group

radial = create_radial_group(scene.grid[5, 5])
radial.rotate(15)  # Rotate entire pattern
```

### Experiment 2: Grid of Groups

```python
for cell in scene.grid:
    if (cell.row + cell.col) % 3 == 0:
        # Create mini pattern in cell
        group = Group()

        # Four corner dots
        for at in ["top_left", "top_right", "bottom_left", "bottom_right"]:
            dot = cell.add_dot(at=at, radius=2, color=colors.primary)
            group.add(dot)

        # Rotate based on position
        angle = (cell.row * 15 + cell.col * 15) % 360
        group.rotate(angle, origin=cell.center)
```

### Experiment 3: Hierarchical Groups

```python
# Groups can contain other groups
main_group = Group()

sub_group1 = create_flower(scene.grid[3, 3])
sub_group2 = create_flower(scene.grid[3, 6])

# Add sub-groups to main group
for entity in sub_group1.entities:
    main_group.add(entity)
for entity in sub_group2.entities:
    main_group.add(entity)

# Transform all at once
main_group.scale(1.2)
main_group.rotate(10)
```

---

## Group Properties

```python
group.entities       # List of all entities in group
group.centroid       # Geometric center of group
len(group)           # Number of entities

# Check if entity is in group
if dot in group:
    print("Dot is in group")

# Remove entity from group
group.remove(dot)

# Clear all entities
group.clear()
```

---

## Best Practices

### 1. Use Groups for Composite Shapes

```python
# Create reusable composite shapes
def create_house(cell):
    group = Group()

    # Base (fill cell)
    base = cell.add_fill(color=colors.primary)
    group.add(base)

    # Roof (triangle)
    roof = cell.add_polygon(shapes.triangle(), fill=colors.secondary)
    group.add(roof)

    return group
```

### 2. Transform Groups, Not Individuals

```python
# Good: Transform once
group.rotate(45)

# Bad: Transform each entity
for entity in entities:
    entity.rotate(45)  # Slower, less accurate
```

### 3. Layer Groups

```python
# Background group
background_group = Group()
for entity in backgrounds:
    entity.z_index = 0
    background_group.add(entity)

# Foreground group
foreground_group = Group()
for entity in foregrounds:
    entity.z_index = 10
    foreground_group.add(entity)
```

---

## Related

- 📖 [Transforms](../../advanced-concepts/04-transforms.md) - Rotation, scaling, translation
- 📖 [Layering](../../fundamentals/05-layering.md) - Z-index system
- 🎯 [Transforms Example](transforms.md) - Individual entity transforms
- 🎯 [Multi-Layer Example](../advanced/multi-layer.md) - Complex grouping

