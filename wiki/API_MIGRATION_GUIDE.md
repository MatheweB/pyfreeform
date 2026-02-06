# PyFreeform API Migration Guide

This guide documents the API changes needed to fix the wiki generator scripts.

## Connection API Changes

### ❌ Old (Incorrect)
```python
Connection(entity1=dot1, entity2=dot2, color="red")
Connection(entity1=dot1, entity2=dot2, width=2, opacity=0.5)
```

### ✅ New (Correct)
```python
# Use start/end instead of entity1/entity2
# Use start_anchor/end_anchor instead of anchor1/anchor2
# Use style dict for color, width, z_index
Connection(start=dot1, end=dot2, style={"color": "red"})
Connection(start=dot1, end=dot2, style={"width": 2, "color": "red", "z_index": 0})

# Or set properties after creation
conn = Connection(start=dot1, end=dot2)
conn.color = "red"
conn.width = 2
```

## Cell Method Changes

### Cell.add_rect — Removed

`cell.add_rect()` does not exist. Use `cell.add_fill()` for full-cell fills, `cell.add_border()` for stroke-only borders, or construct a `Rect()` directly for custom-sized rectangles.

#### ❌ Old (Removed)
```python
cell.add_rect(fill="red", opacity=0.5)
```

#### ✅ New (Correct)
```python
# Full-cell fill
cell.add_fill(color="red", style=FillStyle(color="red", opacity=0.5))

# Stroke-only border
cell.add_border(color="red", width=1)

# Custom-sized rectangle (direct construction)
from pyfreeform import Rect
rect = Rect(x=10, y=10, width=50, height=30, fill="red")
scene.add(rect)
```

### Opacity in Cell Methods

#### ❌ Old (Incorrect)
```python
cell.add_dot(radius=5, color="red", opacity=0.5)
cell.add_line(start="top", end="bottom", color="blue", opacity=0.3)
cell.add_ellipse(rx=10, ry=10, color="green", opacity=0.7)
```

#### ✅ New (Correct)
```python
# Use style objects for opacity
from pyfreeform.config import DotStyle, LineStyle, FillStyle

cell.add_dot(radius=5, style=DotStyle(color="red"))  # No opacity in DotStyle
cell.add_line(start="top", end="bottom", style=LineStyle(color="blue"))  # No opacity in LineStyle

# For fills (ellipse, polygon), use FillStyle or direct params
cell.add_ellipse(rx=10, ry=10, fill="green", stroke=None)

# Note: Most entities don't support opacity directly
# Consider using z_index for layering instead
```

### Cell.add_ellipse Parameters

#### ❌ Old (Incorrect)
```python
cell.add_ellipse(rx=10, ry=10, color="red")
cell.add_ellipse(rx=10, ry=10, fill_opacity=0.5)
```

#### ✅ New (Correct)
```python
# Use fill= instead of color=
cell.add_ellipse(rx=10, ry=10, fill="red")
cell.add_ellipse(rx=10, ry=10, fill="red", stroke=None)
# fill_opacity is not supported - use separate fill and stroke params
```

### Cell.add_polygon Size Parameter

#### ❌ Old (Incorrect)
```python
cell.add_polygon(triangle(), size=0.8)
```

#### ✅ New (Correct)
```python
# The shape utilities already accept size parameter
# Pass sized vertices directly
cell.add_polygon(triangle(size=0.8))
```

### Cell.add_diagonal Direction Parameter

#### ❌ Old (Incorrect)
```python
cell.add_diagonal(direction="down")
cell.add_diagonal(direction="up")
cell.add_diagonal(direction="down_right")
cell.add_diagonal(direction="up_right")
```

#### ✅ New (Correct)
```python
# Use start/end parameters instead of direction
cell.add_diagonal(start="top_left", end="bottom_right")  # down diagonal (was direction="down")
cell.add_diagonal(start="bottom_left", end="top_right")  # up diagonal (was direction="up")
```

### Cell.add_cross and Cell.add_x

#### ❌ Old (Incorrect)
```python
cell.add_cross(color="red")
cell.add_x(color="blue")
```

#### ✅ New (Correct)
```python
# These methods don't exist - create manually
# Cross (horizontal + vertical)
cell.add_line(start="top", end="bottom", color="red")
cell.add_line(start="left", end="right", color="red")

# X (diagonals)
cell.add_diagonal(start="top_left", end="bottom_right", color="blue")
cell.add_diagonal(start="bottom_left", end="top_right", color="blue")
```

## Scene Method Changes

### Scene.add_entity → Scene.add

#### ❌ Old (Incorrect)
```python
scene.add(dot)
scene.add(line)
```

#### ✅ New (Correct)
```python
scene.add(dot)
scene.add(line)
# Can also add multiple at once
scene.add(dot, line, ellipse)
```

## Entity Method Changes

### Entity.add_to → scene.add or cell.place

#### ❌ Old (Incorrect)
```python
dot = Dot(x=100, y=100, radius=5)
dot.add_to(scene)

line = Line(x1=0, y1=0, x2=100, y2=100)
line.add_to(cell)
```

#### ✅ New (Correct)
```python
# Use scene.add() instead of entity.add_to()
dot = Dot(x=100, y=100, radius=5)
scene.add(dot)

line = Line(x1=0, y1=0, x2=100, y2=100, width=1, color="black")
scene.add(line)
```

## Utility Function Changes

### star() Function

#### ❌ Old (Incorrect)
```python
star(points=5, size=0.8, inner_radius=0.4)
```

#### ✅ New (Correct)
```python
star(points=5, size=0.8, inner_ratio=0.4)
```

### hexagon() Function

#### ❌ Old (Incorrect)
```python
hexagon(radius=0.8)
```

#### ✅ New (Correct)
```python
hexagon(size=0.8, center=(0.5, 0.5))
```

### square() Function

#### ❌ Old (Incorrect)
```python
square(side=0.8)
```

#### ✅ New (Correct)
```python
square(size=0.8, center=(0.5, 0.5))
```

### triangle() Function

#### ❌ Old (Incorrect)
```python
triangle(side=0.8)
```

#### ✅ New (Correct)
```python
triangle(size=0.8, center=(0.5, 0.5))
```

### pentagon() Function

#### ❌ Old (Incorrect)
```python
from pyfreeform.entities.polygon import pentagon
pentagon(size=0.8)
```

#### ✅ New (Correct)
```python
from pyfreeform.entities.polygon import regular_polygon
regular_polygon(sides=5, size=0.8, center=(0.5, 0.5))
```

## Grid Method Changes

### Grid.corners Property

#### ❌ Old (Incorrect)
```python
for cell in grid.corners:
    cell.add_dot()
```

#### ✅ New (Correct)
```python
# Access corners manually
corners = [
    grid[0, 0],                    # top-left
    grid[0, grid.cols - 1],        # top-right
    grid[grid.rows - 1, 0],        # bottom-left
    grid[grid.rows - 1, grid.cols - 1]  # bottom-right
]
for cell in corners:
    cell.add_dot()
```

### Grid.checkerboard Offset Parameter

#### ❌ Old (Incorrect)
```python
grid.checkerboard(offset=1)
```

#### ✅ New (Correct)
```python
# checkerboard only accepts color parameter
# For offset checkerboard, use where() instead
grid.where(lambda cell: (cell.row + cell.col + 1) % 2 == 0)
```

## Line Constructor Changes

### Line stroke_dasharray Parameter

#### ❌ Old (Incorrect)
```python
Line(x1=0, y1=0, x2=100, y2=100, stroke_dasharray="5,5")
```

#### ✅ New (Correct)
```python
# stroke_dasharray is not supported
# Use solid lines only, or consider custom SVG rendering
Line(x1=0, y1=0, x2=100, y2=100, color="black", width=1)
```

## Style Object Changes

### DotStyle Opacity

#### ❌ Old (Incorrect)
```python
DotStyle(radius=5, color="red", opacity=0.5)
```

#### ✅ New (Correct)
```python
# DotStyle doesn't support opacity
DotStyle(radius=5, color="red", z_index=0)
# Use z_index for layering instead
```

### FillStyle Usage

#### ✅ Correct
```python
from pyfreeform.config import FillStyle

# FillStyle DOES support opacity
style = FillStyle(color="red", opacity=0.5, z_index=0)
cell.add_fill(style=style)
```

## Common Patterns

### Adding Fills with Opacity
```python
from pyfreeform.config import FillStyle

# Old way (doesn't work)
cell.add_fill(color="red", opacity=0.5)

# New way
cell.add_fill(style=FillStyle(color="red", opacity=0.5))
```

### Creating Connections
```python
# Old way (doesn't work)
Connection(entity1=dot1, entity2=dot2, color="red", opacity=0.5)

# New way
Connection(start=dot1, end=dot2, style={"color": "red", "width": 1})
# Or set properties after creation:
conn = Connection(start=dot1, end=dot2)
conn.color = "red"
# Note: Connections don't support opacity
```

### Accessing Cell Neighbors
```python
# Works
if cell.above:
    cell.above.add_dot()

# Also works
neighbors = cell.neighbors  # Returns dict with "above", "below", "left", "right"
if "above" in neighbors:
    neighbors["above"].add_dot()
```

## Summary of Most Common Fixes

1. **Connection**: `entity1` → `start`, `entity2` → `end`, `anchor1` → `start_anchor`, `anchor2` → `end_anchor`, use `style` dict for color/width/z_index or set properties after creation
2. **Cell.add_rect**: Use `Cell.add_fill()` instead
3. **Cell.add_ellipse**: Use `fill=` instead of `color=`
4. **Cell.add_diagonal**: Use `start=` and `end=` instead of `direction=`
5. **Opacity**: Use `FillStyle` for fills, avoid opacity on other entities
6. **Scene.add_entity**: Use `Scene.add()` instead
7. **Entity.add_to**: Use `scene.add()` instead
8. **Utility functions**: Use `size` instead of `radius`/`side`, use `inner_ratio` instead of `inner_radius`
9. **Grid.corners**: Access manually using grid indices
10. **Polygon shapes**: Use `regular_polygon(sides=N)` for pentagons, etc.

## Quick Reference: Cell Methods

```python
# All supported Cell.add_* methods with correct signatures:
cell.add_dot(at="center", along=None, t=None, radius=4, color="black", z_index=0, style=None)
cell.add_line(start="center", end="center", width=1, color="black", z_index=0, style=None)
cell.add_diagonal(start="bottom_left", end="top_right", width=1, color="black", z_index=0, style=None)
cell.add_curve(start="bottom_left", end="top_right", curvature=0.5, width=1, color="black", z_index=0, style=None)
cell.add_ellipse(at="center", rx=None, ry=None, rotation=0, fill="black", stroke=None, stroke_width=1, z_index=0)
cell.add_polygon(vertices, fill="black", stroke=None, stroke_width=1, z_index=0, rotation=0)
cell.add_text(content, at="center", font_size=None, color="black", font_family="sans-serif", text_anchor="middle", baseline="middle", rotation=0, z_index=0)
cell.add_fill(color="black", z_index=0, style=None)
cell.add_border(color="#cccccc", width=0.5, z_index=0, style=None)
```
