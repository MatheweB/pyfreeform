
# Dots

Dots are the simplest entity in PyFreeform - filled circles that serve as the foundation for many artistic styles. Perfect for point-based art, pixels, particles, and dot compositions.

---

## What is a Dot?

A **Dot** is a filled circle entity with:
- **Position** - Center point (x, y)
- **Radius** - Size in pixels
- **Color** - Fill color
- **Z-index** - Layer ordering

Dots are the most common entity, ideal for creating dot art, halftones, scatter plots, and particle systems.

![Dots of varying sizes](./_images/01-dots/01_varying_sizes.svg)

---

## Creating Dots

### Via Cell Method (Recommended)

```python
# Simple dot at cell center
cell.add_dot(radius=5, color="coral")

# Dot at named position
cell.add_dot(at="top_left", radius=3, color="blue")

# Dot at relative coordinates
cell.add_dot(at=(0.75, 0.25), radius=4, color="red")

# Dot along a path
line = cell.add_line(start="left", end="right")
cell.add_dot(along=line, t=0.5, radius=3)
```

![Dot Positioning](./_images/01-dots/02_positioning.svg)

### Direct Construction

```python
from pyfreeform import Dot

# Create dot manually
dot = Dot(x=100, y=200, radius=10, color="coral")
scene.add(dot)
```

---

## Properties

```python
dot.position     # Point(x, y) - center
dot.x            # X coordinate
dot.y            # Y coordinate
dot.radius       # Radius in pixels
dot.color        # Fill color (hex string)
dot.z_index      # Layer order
```

### Modifying Properties

```python
dot = cell.add_dot(radius=5, color="red")

# Change size
dot.radius = 10

# Change color
dot.color = "blue"
dot.color = "#ff5733"
dot.color = (255, 87, 51)

# Change layer
dot.z_index = 5
```

---

## Anchors

Dots have a single anchor - their center:

```python
dot.anchor_names  # ["center"]
center = dot.anchor("center")  # Returns dot's position
```

---

## Common Patterns

### Pattern 1: Basic Dot Art

```python
scene = Scene.from_image("photo.jpg", grid_size=40)

for cell in scene.grid:
    cell.add_dot(color=cell.color, radius=4)

scene.save("dot_art.svg")
```

![Grid Pattern](./_images/01-dots/02_grid_pattern.svg)

### Pattern 2: Size Based on Brightness

!!! tip "Brightness-Based Sizing Creates Natural Compositions"
    ```python
    for cell in scene.grid:
        # Larger dots in brighter areas
        size = 2 + cell.brightness * 8  # Range: 2-10
        cell.add_dot(radius=size, color=cell.color)
    ```

![Brightness Sizing](./_images/01-dots/03_brightness_sized.svg)

### Pattern 3: Conditional Rendering

```python
for cell in scene.grid:
    # Only draw in bright areas
    if cell.brightness > 0.6:
        cell.add_dot(radius=6, color="yellow")
```

### Pattern 4: Halftone Effect

```python
scene = Scene.from_image("photo.jpg", grid_size=50)
scene.background = "white"

for cell in scene.grid:
    # Invert brightness for halftone
    size = (1 - cell.brightness) * 8
    cell.add_dot(radius=size, color="black")

scene.save("halftone.svg")
```

### Pattern 5: Parametric Positioning

```python
for cell in scene.grid:
    # Create diagonal line
    line = cell.add_diagonal(start="bottom_left", end="top_right")

    # Position dot along line based on brightness
    cell.add_dot(
        along=line,
        t=cell.brightness,  # 0.0 to 1.0
        radius=4,
        color="red"
    )
```

---

## Styling with DotStyle

For reusable configurations:

```python
from pyfreeform.config import DotStyle

# Define styles
large_style = DotStyle(radius=8, color="coral")
small_style = DotStyle(radius=3, color="navy")

# Use styles
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(style=large_style)
    else:
        cell.add_dot(style=small_style)

# Create variations
blue_large = large_style.with_color("blue")
huge_coral = large_style.with_radius(15)
```

---

## Movement and Transforms

Dots support all standard entity operations:

```python
dot = cell.add_dot(radius=5, color="red")

# Move
dot.move_to(100, 200)
dot.move_by(dx=10, dy=-5)

# Scale (changes radius)
dot.scale(2.0)  # Double the radius
dot.scale(0.5)  # Half the radius

# Rotate (no visual effect for circles, but updates internal rotation)
dot.rotate(45)
```

---

## Layering

Control render order with z-index:

```python
# Background dots
cell.add_dot(radius=8, color="lightgray", z_index=0)

# Middle layer
cell.add_dot(radius=5, color="gray", z_index=1)

# Foreground dots
cell.add_dot(radius=3, color="black", z_index=2)
```

![Layered dots](./_images/01-dots/03_layering.svg)

![Advanced Layering](./_images/01-dots/04_layering.svg)

Higher z-index renders on top.

---

## Complete Examples

### Example 1: Grid with Variable Sizing

```python
from pyfreeform import Scene, Palette

scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Distance from center
    dx = cell.col - 10
    dy = cell.row - 10
    distance = (dx*dx + dy*dy) ** 0.5

    # Size decreases with distance
    max_distance = (10*10 + 10*10) ** 0.5
    size = 2 + (1 - distance / max_distance) * 8

    cell.add_dot(radius=size, color=colors.primary)

scene.save("radial_dots.svg")
```

![Grid Pattern](./_images/01-dots/05_grid_pattern.svg)

### Example 2: Multi-Color Composition

```python
from pyfreeform import Scene, Palette

scene = Scene.from_image("photo.jpg", grid_size=40)
colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(radius=6, color=colors.primary)
    elif cell.brightness > 0.4:
        cell.add_dot(radius=4, color=colors.secondary)
    elif cell.brightness > 0.2:
        cell.add_dot(radius=2, color=colors.accent)

scene.save("threshold_dots.svg")
```

![Multi-Color Composition](./_images/01-dots/06_multicolor.svg)

---

## Tips and Best Practices

!!! tip "Start with Dots"
    Dots are the easiest entity to work with - great for prototyping:

```python
# Quick prototype
for cell in scene.grid:
    cell.add_dot(color=cell.color)
```

### Use Brightness for Size

Creates natural-looking compositions:

```python
size = min_size + cell.brightness * (max_size - min_size)
```

### Layer Large Before Small

For depth:

```python
cell.add_dot(radius=10, color="lightgray", z_index=0)  # Background
cell.add_dot(radius=5, color="gray", z_index=1)        # Middle
cell.add_dot(radius=2, color="black", z_index=2)       # Foreground
```

### Consider Overlap

!!! note "Overlapping Can Be Artistic"
    Large dots may overlap neighbors - this can create interesting effects:

```python
# Intentional overlap for organic feel
cell.add_dot(radius=cell.width * 0.7, color=cell.color)
```

---

## Next Steps

- **Explore lines**: [Lines](02-lines.md)
- **Try curves**: [Curves](03-curves.md)
- **See examples**: [Quick Start](../examples/beginner/quick-start.md), [Custom Dots](../examples/beginner/custom-dots.md)
- **Learn styling**: [Styling](../fundamentals/04-styling.md)

---

## See Also

- 📖 [Lines](02-lines.md) - Straight paths
- 📖 [Curves](03-curves.md) - Bézier curves
- 📖 [Styling](../fundamentals/04-styling.md) - Colors and properties
- 🎯 [Quick Start Example](../examples/beginner/quick-start.md)
- 🎯 [Custom Dots Example](../examples/beginner/custom-dots.md)
- 🎨 [Dot Art Recipe](../recipes/01-dot-art-from-images.md)
- 🔍 [Dot API Reference](../api-reference/entities.md#dot)

