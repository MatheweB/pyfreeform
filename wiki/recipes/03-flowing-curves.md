
# Recipe: Flowing Curves

Create organic, flowing compositions using Bézier curves with variable curvature across your grid. Master the art of visual flow, movement, and rhythm through parametric curve control.

---

## What Are Flowing Curves?

Flowing curves are Bézier curves whose curvature varies systematically across a grid, creating patterns that suggest movement, waves, energy, or organic growth. Unlike static geometric patterns, flowing curves have directionality and rhythm.

!!! info "Why Curves Flow"
    When curvature changes gradually across space, our visual system perceives:

    - **Movement**: Increasing curvature suggests acceleration
    - **Rhythm**: Regular curvature patterns create visual beats
    - **Organicity**: Variable curves feel natural, not mechanical
    - **Depth**: Curves can suggest 3D forms on flat surfaces

The key is the **curvature parameter** (`-1` to `1`), which controls how much a curve bends between two points.

## Visual Result

Here's what we're creating:

![Horizontal flowing curves with varying curvature](./_images/03-flowing-curves/01_horizontal_flow.svg)

Flowing curves create a sense of movement and organic energy across the composition.

---

## The Pattern

**Key Idea**: Vary curvature across the grid to create wave-like or flowing patterns.

```python
for cell in scene.grid:
    # Curvature varies based on position
    curvature = (cell.col / scene.grid.cols - 0.5) * 2  # Range: -1 to 1

    cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        color=cell.color
    )
```

!!! note "Understanding the Curvature Formula"
    The formula `curvature = (cell.col / scene.grid.cols - 0.5) * 2` creates a linear gradient:

    - `cell.col / scene.grid.cols` ranges from 0.0 (leftmost) to 1.0 (rightmost)
    - Subtracting 0.5 centers it: -0.5 to 0.5
    - Multiplying by 2 scales to full range: -1.0 to 1.0

    Result:
    - **Left side (col=0)**: curvature = -1.0 (curves downward)
    - **Center**: curvature = 0.0 (straight line)
    - **Right side (col=max)**: curvature = 1.0 (curves upward)

### Curvature Values Explained

The `curvature` parameter controls the Bézier curve's control point displacement:

- **curvature = 0**: Straight line (no curve)
- **curvature = 0.5**: Gentle curve
- **curvature = 1.0**: Strong curve (90° arc)
- **curvature = -0.5**: Gentle curve in opposite direction
- **curvature = -1.0**: Strong curve in opposite direction

!!! tip "Curvature Ranges"
    While curvature technically accepts any value, practical ranges are:

    - **-1.0 to 1.0**: Normal curves (recommended)
    - **-2.0 to 2.0**: Extreme curves (loops possible)
    - **Beyond ±2**: Chaos (avoid unless intentional)

---

## Complete Example

```python
from pyfreeform import Scene, Palette

# Create scene from image
scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Only draw in certain brightness range
    if 0.3 < cell.brightness < 0.7:
        # Horizontal flow pattern
        curvature_h = (cell.col / scene.grid.cols - 0.5) * 2

        curve_h = cell.add_curve(
            start="left",
            end="right",
            curvature=curvature_h,
            color=colors.line,
            width=1
        )

        # Add dot that flows along curve
        cell.add_dot(
            along=curve_h,
            t=cell.brightness,
            radius=2,
            color=colors.accent
        )

scene.save("flowing_curves.svg")
```

![Curves with dots flowing along them](./_images/03-flowing-curves/09_curves_with_dots.svg)

---

## Variations

### Vertical Flow

Create vertical movement by varying curvature along the rows.

```python
for cell in scene.grid:
    # Curvature varies vertically
    curvature = (cell.row / scene.grid.rows - 0.5) * 2

    cell.add_curve(
        start="top",
        end="bottom",
        curvature=curvature,
        color=cell.color
    )
```

![Vertical flowing curves with varying curvature](./_images/03-flowing-curves/02_vertical_flow.svg)

!!! tip "Direction Matching"
    Match the curvature variation direction to the curve direction:

    - **Horizontal curves** (`start="left"`, `end="right"`): vary by `cell.col`
    - **Vertical curves** (`start="top"`, `end="bottom"`): vary by `cell.row`
    - **Diagonal curves** (`start="bottom_left"`, `end="top_right"`): vary by `cell.row + cell.col` or `cell.row - cell.col`

### Radial Flow

```python
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    # Distance from center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = (dr*dr + dc*dc) ** 0.5

    # Curvature based on distance
    curvature = (distance / 10) * 0.5

    cell.add_curve(
        start="center",
        end="top_right",
        curvature=curvature,
        color=cell.color
    )
```

![Radial flowing curves from center](./_images/03-flowing-curves/05_radial_flow.svg)

### Brightness-Driven Curvature

Let image data control curvature for organic, responsive patterns.

```python
for cell in scene.grid:
    # Bright = curved, dark = straight
    curvature = cell.brightness  # 0 to 1

    cell.add_curve(
        start="bottom_left",
        end="top_right",
        curvature=curvature,
        color="white" if cell.brightness > 0.5 else "gray"
    )
```

![Curves with brightness-driven curvature](./_images/03-flowing-curves/03_brightness_driven.svg)

!!! info "Brightness as Control Parameter"
    Using `cell.brightness` to control curvature creates a direct relationship between image content and curve shape:

    - **Dark areas (brightness ≈ 0)**: Nearly straight curves
    - **Bright areas (brightness ≈ 1)**: Strongly curved lines

    This technique makes the pattern "respond" to the image, creating organic integration between data and form.

### Advanced Brightness Mapping

```python
# Centered brightness (curves both ways)
curvature = (cell.brightness - 0.5) * 2  # Range: -1 to 1

# Inverted (dark = curved, bright = straight)
curvature = (1 - cell.brightness)  # Range: 0 to 1

# Threshold-based (binary curvature)
curvature = 0.8 if cell.brightness > 0.5 else -0.8

# Exponential scaling (emphasize extremes)
import math
curvature = math.pow(cell.brightness, 2) * 2 - 1

# Sine-based smooth oscillation
curvature = math.sin(cell.brightness * math.pi)
```

---

## Tips

### Create Wave Patterns

Use sine waves for smooth oscillation and natural rhythm.

```python
import math

for cell in scene.grid:
    # Sine wave curvature
    phase = cell.col / scene.grid.cols * math.pi * 2
    curvature = math.sin(phase)

    cell.add_curve(
        start="top",
        end="bottom",
        curvature=curvature,
        color=colors.primary
    )
```

![Sine wave curvature pattern](./_images/03-flowing-curves/04_wave_pattern.svg)

!!! tip "Sine Wave Parameters"
    The formula `curvature = math.sin(phase)` where `phase = (position / total) * math.pi * N` creates waves:

    - **N = 1**: Half wave (smooth gradient from -1 to 1 to -1)
    - **N = 2**: Full wave (one complete oscillation)
    - **N = 4**: Two full waves (two peaks and valleys)
    - **N = 8**: Four full waves (rapid oscillation)

    Experiment with different frequencies:

    ```python
    # Single smooth wave
    phase = cell.col / scene.grid.cols * math.pi

    # Multiple waves
    phase = cell.col / scene.grid.cols * math.pi * 6

    # Add phase shift
    phase = (cell.col / scene.grid.cols * math.pi * 2) + (math.pi / 4)
    ```

### Combining Wave Patterns

```python
import math

for cell in scene.grid:
    # Horizontal wave
    h_phase = cell.col / scene.grid.cols * math.pi * 2
    h_wave = math.sin(h_phase) * 0.5

    # Vertical wave
    v_phase = cell.row / scene.grid.rows * math.pi * 3
    v_wave = math.sin(v_phase) * 0.5

    # Combine
    curvature = h_wave + v_wave

    cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        color=cell.color
    )
```

### Layer Multiple Flows

Create complex compositions by layering curves in different directions.

```python
# Background flow
cell.add_curve(
    start="left",
    end="right",
    curvature=0.5,
    color=colors.line,
    width=1,
    z_index=0
)

# Foreground accent
if cell.brightness > 0.6:
    cell.add_curve(
        start="top",
        end="bottom",
        curvature=-0.5,
        color=colors.accent,
        width=2,
        z_index=10
    )
```

![Horizontal and vertical curves layered](./_images/03-flowing-curves/06_dual_direction.svg)

!!! note "Layering Strategy"
    When layering multiple curve directions:

    1. **Base layer** (z_index=0): Subtle, muted colors, thinner lines
    2. **Middle layer** (z_index=5): Main visual rhythm
    3. **Accent layer** (z_index=10): Conditional, bright colors, selective

    Use different curvature formulas for each layer to avoid repetition:

    ```python
    # Layer 1: Linear gradient
    curvature1 = (cell.col / scene.grid.cols - 0.5) * 2

    # Layer 2: Sine wave
    import math
    curvature2 = math.sin(cell.row / scene.grid.rows * math.pi * 4)

    # Layer 3: Brightness-driven
    curvature3 = cell.brightness
    ```

### Vary Line Width

Add depth and emphasis by varying stroke width across the composition.

```python
# Thicker curves in brighter areas
width = 0.5 + cell.brightness * 2  # 0.5 to 2.5

cell.add_curve(
    curvature=0.5,
    width=width,
    color=cell.color
)
```

![Curves with varying line width based on brightness](./_images/03-flowing-curves/07_varying_width.svg)

!!! tip "Width Variation Strategies"
    Different width formulas create different effects:

    ```python
    # Subtle variation (0.8 to 1.2)
    width = 0.8 + cell.brightness * 0.4

    # Dramatic variation (0.1 to 5)
    width = 0.1 + cell.brightness * 4.9

    # Position-based (thicker on right)
    width = 0.5 + (cell.col / scene.grid.cols) * 3

    # Threshold-based (binary widths)
    width = 2.0 if cell.brightness > 0.5 else 0.5

    # Inverted (thick in dark areas)
    width = 0.5 + (1 - cell.brightness) * 2.5
    ```

### Combining Width and Curvature

```python
# Thicker curves are more curved
width = 0.5 + cell.brightness * 2
curvature = cell.brightness * 0.8

cell.add_curve(
    start="left",
    end="right",
    curvature=curvature,
    width=width,
    color=cell.color
)
```

### Diagonal Curves

```python
for cell in scene.grid:
    curvature = (cell.row + cell.col) / (scene.grid.rows + scene.grid.cols)
    cell.add_curve(
        start="bottom_left",
        end="top_right",
        curvature=curvature,
        color=cell.color
    )
```

![Diagonal flowing curves across the grid](./_images/03-flowing-curves/08_diagonal_curves.svg)

### Alternating Curves

Create weaving, textile-like patterns with alternating curve directions.

```python
for cell in scene.grid:
    direction = 1 if cell.row % 2 == 0 else -1
    curvature = direction * cell.brightness

    cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        color=cell.color
    )
```

![Alternating curve directions creating a weaving pattern](./_images/03-flowing-curves/10_alternating_curves.svg)

### Advanced Alternation Patterns

```python
# Checkerboard alternation
direction = 1 if (cell.row + cell.col) % 2 == 0 else -1
curvature = direction * 0.7

# Every third row alternates
direction = 1 if cell.row % 3 == 0 else -1
curvature = direction * cell.brightness

# Gradient alternation (gradual flip)
t = cell.col / scene.grid.cols
curvature = cell.brightness * (1 - t * 2)  # Flips from +1 to -1
```

---

## Parameter Tuning Guide

### Curvature Range Selection

| Range | Effect | Use Case |
|-------|--------|----------|
| 0 to 0.3 | Subtle curves, mostly straight | Technical, architectural |
| 0 to 0.7 | Gentle flowing curves | Natural, organic patterns |
| -1 to 1 | Full range, dramatic flow | Artistic, expressive work |
| -2 to 2 | Extreme curves, possible loops | Abstract, chaotic art |

!!! warning "Avoiding Loops"
    Curvature values beyond ±1.5 can create self-intersecting curves (loops). This may be intentional for abstract art, but usually indicates the curvature is too extreme. If you see unexpected loops, reduce your curvature multiplier.

### Grid Size Considerations

- **Grid 20-30**: Large cells, bold curves, graphic style
- **Grid 40-50**: Balanced detail, visible flow patterns
- **Grid 60-80**: Fine detail, subtle flow (recommended for images)
- **Grid 90+**: Very fine, may lose flow visibility

### Line Width Selection

| Width | Effect | Best Use |
|-------|--------|----------|
| 0.5-1 | Fine, delicate lines | Detailed, intricate patterns |
| 1-2 | Standard weight | Most general purposes |
| 2-4 | Bold, prominent lines | Graphic, poster-like art |
| 4+ | Very heavy strokes | Abstract, painterly effects |

!!! tip "Width vs Grid Size Balance"
    Keep `width < (canvas_width / grid_size) / 2` to avoid excessive overlap:

    - Grid 40, width < 12
    - Grid 60, width < 8
    - Grid 80, width < 6

---

## Choosing Curve Directions

### Start and End Anchor Points

PyFreeform supports these anchor positions for curves:

- **Cardinal**: `"left"`, `"right"`, `"top"`, `"bottom"`
- **Corners**: `"top_left"`, `"top_right"`, `"bottom_left"`, `"bottom_right"`
- **Center**: `"center"`

### Common Direction Patterns

```python
# Horizontal flow (most common)
start="left", end="right"

# Vertical flow
start="top", end="bottom"

# Diagonal ascending
start="bottom_left", end="top_right"

# Diagonal descending
start="top_left", end="bottom_right"

# Radial from center
start="center", end="top_right"  # or any corner

# Circular/spiral (combine with rotation)
start="left", end="right"  # with varying curvature per angle
```

### Direction-Curvature Relationships

!!! info "Curvature Direction Convention"
    For horizontal curves (`start="left"`, `end="right"`):

    - **Positive curvature**: Curves upward (toward top)
    - **Negative curvature**: Curves downward (toward bottom)

    For vertical curves (`start="top"`, `end="bottom"`):

    - **Positive curvature**: Curves rightward
    - **Negative curvature**: Curves leftward

    This is based on the "right-hand rule" in 2D graphics.

---

## Complete Example: Wave Field

```python
from pyfreeform import Scene, Palette
import math

# Create scene from image
scene = Scene.from_image("landscape.jpg", grid_size=50)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Horizontal wave curvature
    h_phase = cell.col / scene.grid.cols * math.pi * 3
    h_wave = math.sin(h_phase + cell.row * 0.1)

    # Modulate by brightness
    curvature = h_wave * cell.brightness

    # Width varies with position
    width = 0.5 + (cell.row / scene.grid.rows) * 2

    # Color varies with brightness
    if cell.brightness > 0.7:
        color = colors.light
    elif cell.brightness > 0.4:
        color = colors.primary
    else:
        color = colors.dark

    cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        width=width,
        color=color
    )

    # Add accent dots on curve peaks
    if abs(curvature) > 0.7:
        curve = cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            width=1,
            color=colors.accent
        )
        cell.add_dot(
            along=curve,
            t=0.5,
            radius=2,
            color=colors.accent
        )

scene.save("wave_field.svg")
```

---

## Tips and Best Practices

### Creating Natural Flow

1. **Use gradual changes**: Smooth transitions feel organic
   ```python
   # Good: gradual
   curvature = (cell.col / scene.grid.cols - 0.5) * 2

   # Avoid: too abrupt
   curvature = 1 if cell.col > 20 else -1
   ```

2. **Combine multiple influences**: Position + brightness + waves
   ```python
   import math
   position_influence = (cell.col / scene.grid.cols - 0.5) * 2
   wave_influence = math.sin(cell.row * 0.3)
   data_influence = cell.brightness
   curvature = (position_influence + wave_influence + data_influence) / 3
   ```

3. **Use mathematical functions**: Sine, cosine, exponentials for smooth curves
   ```python
   # Smooth bell curve
   t = cell.col / scene.grid.cols
   curvature = math.exp(-((t - 0.5) ** 2) / 0.1)

   # Smooth S-curve
   curvature = 2 / (1 + math.exp(-10 * (t - 0.5))) - 1
   ```

### Performance Optimization

```python
# Sparse curves (only some cells)
for cell in scene.grid:
    if cell.row % 2 == 0:  # Every other row
        curvature = cell.brightness
        cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            color=cell.color
        )

# Pre-calculate complex formulas
import math
for cell in scene.grid:
    # Calculate once per cell, not per curve
    phase = (cell.col / scene.grid.cols) * math.pi * 2
    curvature = math.sin(phase)

    cell.add_curve(start="left", end="right", curvature=curvature, color=cell.color)
```

### Debugging Curvature

If your curves look wrong:

1. **Print curvature values**: Check the range
   ```python
   curvature = (cell.col / scene.grid.cols - 0.5) * 2
   if cell.row == 0:  # Debug first row only
       print(f"Col {cell.col}: curvature = {curvature:.2f}")
   ```

2. **Visualize with color**: Map curvature to color
   ```python
   # Red = negative, white = zero, blue = positive
   if curvature < 0:
       color = f"rgb({int(abs(curvature) * 255)}, 0, 0)"
   else:
       color = f"rgb(0, 0, {int(curvature * 255)})"
   cell.add_curve(curvature=curvature, color=color)
   ```

3. **Test with extremes**: Try curvature = -1, 0, 1 explicitly
   ```python
   if cell.col == 0:
       curvature = -1
   elif cell.col == scene.grid.cols // 2:
       curvature = 0
   elif cell.col == scene.grid.cols - 1:
       curvature = 1
   ```

### Common Mistakes

!!! warning "Avoid These Pitfalls"
    1. **Division by zero**: Check grid size before dividing
       ```python
       # Bad: crashes if cols = 1
       t = cell.col / (scene.grid.cols - 1)

       # Good: safe division
       t = cell.col / max(scene.grid.cols - 1, 1)
       ```

    2. **Forgetting to center**: Remember to subtract 0.5 for symmetric ranges
       ```python
       # Bad: only positive curvature (0 to 1)
       curvature = cell.col / scene.grid.cols

       # Good: symmetric range (-0.5 to 0.5)
       curvature = (cell.col / scene.grid.cols) - 0.5
       ```

    3. **Wrong direction variable**: Match row/col to curve direction
       ```python
       # Bad: horizontal curve varied by row (creates uniform curves)
       curvature = cell.row / scene.grid.rows
       cell.add_curve(start="left", end="right", curvature=curvature)

       # Good: horizontal curve varied by col
       curvature = cell.col / scene.grid.cols
       cell.add_curve(start="left", end="right", curvature=curvature)
       ```

---

## See Also

- [Curves](../entities/03-curves.md) - Bézier curve mathematics
- [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md) - Positioning along paths
- [Curves Example](../examples/intermediate/curves.md) - Detailed breakdown
- [Bézier Mathematics](../parametric-art/03-bezier-mathematics.md) - Deep dive

## See Also

- 📖 [Curves](../entities/03-curves.md) - Bézier curve mathematics
- 📖 [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md) - Positioning along paths
- 🎯 [Curves Example](../examples/intermediate/curves.md) - Detailed breakdown
- 🎨 [Bézier Mathematics](../parametric-art/03-bezier-mathematics.md) - Deep dive

