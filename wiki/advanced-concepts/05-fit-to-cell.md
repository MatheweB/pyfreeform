
# Fit to Cell

Automatically constrain entities within cell boundaries.

## What is fit_to_cell()?

```python
entity.fit_to_cell(scale=1.0, recenter=True)
```

![Before and after fit_to_cell: constraining an oversized ellipse](./_images/05-fit-to-cell/01-what-is-fit-concept.svg)

![Step-by-step breakdown of the fit_to_cell process](./_images/05-fit-to-cell/02-what-is-fit-steps.svg)

Automatically:
1. Calculates entity's bounding box
2. Accounts for rotation
3. Scales to fit within cell
4. Optionally centers in cell

## Usage

![Basic fit_to_cell usage with a single entity](./_images/05-fit-to-cell/03-usage-basic.svg)

```python
# Create large ellipse
ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45)

# Auto-fit to 85% of cell
ellipse.fit_to_cell(0.85)
```

![fit_to_cell with different shapes: ellipse, rectangle, polygon, star](./_images/05-fit-to-cell/04-usage-different-shapes.svg)

## Parameters

- `scale` (0-1): Target size relative to cell (1.0 = full cell)
- `recenter` (bool): Whether to center in cell (default: True)

![Scale parameter variations from 0.5 to 1.0](./_images/05-fit-to-cell/05-parameters-scale.svg)

![Recenter parameter: centered vs. non-centered entities](./_images/05-fit-to-cell/06-parameters-recenter.svg)

## Examples

### Dynamic Sizing
```python
for cell in scene.grid:
    # Size based on brightness
    target_scale = 0.3 + cell.brightness * 0.7
    
    ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45)
    ellipse.fit_to_cell(target_scale)
```

![Dynamic sizing based on cell brightness values](./_images/05-fit-to-cell/07-example-brightness-based.svg)

![Position-based sizing varying across the grid](./_images/05-fit-to-cell/08-example-position-based.svg)

![Pattern-based sizing using checkerboard or border selections](./_images/05-fit-to-cell/09-example-pattern-based.svg)

### Rotation-Aware
```python
# Rotated ellipses still fit perfectly!
for cell in scene.grid:
    rotation = (cell.row + cell.col) * 15
    ellipse = cell.add_ellipse(rx=20, ry=10, rotation=rotation)
    ellipse.fit_to_cell(0.8)  # Handles rotation automatically
```

![Rotated ellipses at different angles all fitting perfectly within cells](./_images/05-fit-to-cell/10-example-rotation-awareness.svg)

![Combined rotation and dynamic sizing in a single grid](./_images/05-fit-to-cell/11-example-combined-rotation-sizing.svg)

![Rotation grid showing fit_to_cell across many angles](./_images/05-fit-to-cell/12-example-rotation-grid.svg)

## Works For All Entities

```python
dot.fit_to_cell(0.9)
ellipse.fit_to_cell(0.85)
polygon.fit_to_cell(0.75)
text.fit_to_cell(0.8)
```

![fit_to_cell working across all entity types: Dot, Ellipse, Rectangle, Polygon, Text](./_images/05-fit-to-cell/13-works-for-all-comparison.svg)

![Complex example of fit_to_cell with various entity types and transforms](./_images/05-fit-to-cell/14-works-for-all-complex.svg)

## Position-Aware Fitting

Place entities at specific positions within a cell **and** guarantee they never overflow:

```python
entity.fit_to_cell(scale, at=(rx, ry))
```

The `at` parameter accepts a cell-relative position. Available space is automatically constrained by the nearest cell edge — so a shape at `(0.25, 0.25)` only gets the top-left quadrant, while `(0.5, 0.5)` gets the full cell.

![Position-aware fitting: same entity at different cell positions](./_images/05-fit-to-cell/15-position-aware-concept.svg)

```python
# Place a huge dot in the top-left quadrant — it shrinks to fit
dot = cell.add_dot(radius=9999, color="blue")
dot.fit_to_cell(0.9, at=(0.25, 0.25))

# Same call at center uses the full cell
dot = cell.add_dot(radius=9999, color="blue")
dot.fit_to_cell(0.9, at=(0.5, 0.5))
```

### Orbiting Dots

Combine `at=` with a bit of math for a fun orbital effect:

```python
import math
for cell in scene.grid:
    angle = math.atan2(dy, dx)
    rx = 0.5 + math.cos(angle) * 0.18
    ry = 0.5 + math.sin(angle) * 0.18
    dot = cell.add_dot(radius=100, color=color)
    dot.fit_to_cell(scale, at=(rx, ry))
```

![Orbiting dots: position-aware fitting creates a swirling pattern](./_images/05-fit-to-cell/16-position-aware-orbit.svg)

## See Also
- [Ellipses Example](../examples/advanced/ellipses.md)
- [Transforms](04-transforms.md)
