
# Grid Selections

Powerful pattern-based iteration over grid cells.

## Selection Methods

### Rows and Columns
```python
grid.row(0)           # Top row
grid.column(5)        # 6th column
```

![Selecting a single row highlighted in blue](./_images/06-grid-selections/01-selection-single-row.svg)

![Selecting multiple rows highlighted in blue](./_images/06-grid-selections/02-selection-multiple-rows.svg)

![Selecting a single column highlighted in blue](./_images/06-grid-selections/03-selection-single-column.svg)

![Selecting multiple columns highlighted in blue](./_images/06-grid-selections/04-selection-multiple-columns.svg)

### Patterns
```python
grid.checkerboard("black")  # Alternating pattern
grid.border(thickness=2)    # Outer border
grid.every(n=3)            # Every 3rd cell
```

![Checkerboard pattern with alternating black squares](./_images/06-grid-selections/05-selection-checkerboard-black.svg)

![Checkerboard pattern with alternating white squares](./_images/06-grid-selections/06-selection-checkerboard-white.svg)

![Border selection with thin thickness](./_images/06-grid-selections/07-selection-border-thin.svg)

![Border selection with thick thickness](./_images/06-grid-selections/08-selection-border-thick.svg)

![Every nth cell selection pattern](./_images/06-grid-selections/09-selection-every-nth.svg)

![Comparison of different every-nth values](./_images/06-grid-selections/10-selection-every-nth-comparison.svg)

### Regions
```python
grid.region(
    row_start=5, row_end=15,
    col_start=5, col_end=15
)
```

![Region selection highlighting a rectangular area](./_images/06-grid-selections/11-selection-region-basic.svg)

![Multiple region selections on the same grid](./_images/06-grid-selections/12-selection-region-multiple.svg)

### Conditional (where)
```python
grid.where(lambda c: c.brightness > 0.7)
grid.where(lambda c: c.row < 10 and c.col > 10)
```

![Conditional selection based on brightness threshold](./_images/06-grid-selections/13-selection-where-brightness.svg)

![Conditional selection based on row and column position](./_images/06-grid-selections/14-selection-where-position.svg)

![Conditional selection based on distance from center forming a circle](./_images/06-grid-selections/15-selection-where-distance.svg)

## Examples

### Pattern 1: Checkerboard
```python
for cell in scene.grid.checkerboard("black"):
    cell.add_fill(color="black")

for cell in scene.grid.checkerboard("white"):
    cell.add_fill(color="white")
```

![Full checkerboard pattern with black and white cells](./_images/06-grid-selections/16-example-checkerboard-full.svg)

### Pattern 2: Border Highlight
```python
for cell in scene.grid.border(thickness=2):
    cell.add_border(color="gold", width=3)
```

![Border highlight with gold-colored outer cells](./_images/06-grid-selections/17-example-border-highlight.svg)

### Pattern 3: Conditional
```python
# Bright areas only
for cell in scene.grid.where(lambda c: c.brightness > 0.6):
    cell.add_dot(radius=8, color="yellow")
```

![Conditional brightness pattern with yellow dots on bright cells](./_images/06-grid-selections/18-example-conditional-brightness.svg)

### Pattern 4: Center Cross
```python
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid.row(center_row):
    cell.add_fill(color="blue")

for cell in scene.grid.column(center_col):
    cell.add_fill(color="blue")
```

![Center cross pattern with horizontal and vertical blue lines](./_images/06-grid-selections/19-example-center-cross.svg)

### Pattern 5: Diagonal Lines
![Diagonal line pattern across the grid](./_images/06-grid-selections/20-example-diagonal-lines.svg)

## Chaining Patterns

```python
# Bright cells in border only
bright_border = [
    cell for cell in scene.grid.border()
    if cell.brightness > 0.5
]

for cell in bright_border:
    cell.add_dot(color="gold", radius=8)
```

![Bright cells in the border highlighted with gold dots](./_images/06-grid-selections/21-chaining-bright-border.svg)

![Chaining checkerboard with conditional selection](./_images/06-grid-selections/22-chaining-checkerboard-conditional.svg)

![Chaining border and cross selections](./_images/06-grid-selections/23-chaining-border-and-cross.svg)

![Complex pattern combining border, checkerboard, and region selections](./_images/06-grid-selections/24-chaining-complex-pattern.svg)

![Chaining conditional selections with region filters](./_images/06-grid-selections/25-chaining-conditional-regions.svg)

## See Also
- [Grid Patterns Example](../examples/beginner/grid-patterns.md)
- [Grids and Cells](../fundamentals/02-grids-and-cells.md)
