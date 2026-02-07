
# Example: Text

**Difficulty**: ⭐⭐ Intermediate

Master typography features: alignment, rotation, sizing, and combining text with graphics.

---

## What You'll Learn

- Text positioning and alignment
- Font families and sizing
- Rotating text
- Combining text with entities
- Data-driven labels
- Auto-sizing text inside shapes with `fit_within`

---

## Final Result

![Alignment](../_images/text/01_alignment.svg)

### More Examples

| Alignment | Font Families | Data Labels |
|-----------|---------------|-------------|
| ![Example 1](../_images/text/01_alignment.svg) | ![Example 2](../_images/text/02_font_families.svg) | ![Example 3](../_images/text/03_data_labels.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette, Text

scene = Scene.with_grid(cols=10, rows=10, cell_size=30)
colors = Palette.midnight()
scene.background = colors.background

# Example 1: Title overlay
title = Text(
    x=scene.width // 2,
    y=30,
    content="Generative Art",
    font_size=28,
    color=colors.primary,
    font_family="serif",
    text_anchor="middle",
    z_index=100
)
scene.add(title)

# Example 2: Grid labels
for row in range(scene.grid.rows):
    cell = scene.grid[row, 0]
    cell.add_text(
        content=str(row + 1),
        at="left",
        font_size=12,
        color=colors.line,
        text_anchor="start"
    )

for col in range(scene.grid.cols):
    cell = scene.grid[0, col]
    label = chr(65 + col)  # A, B, C, ...
    cell.add_text(
        content=label,
        at="top",
        font_size=12,
        color=colors.line,
        baseline="hanging"
    )

# Example 3: Data labels inside dots (auto-sized with fit_within)
for cell in scene.grid[2:8, 2:8]:
    # Dot sized by brightness
    dot = cell.add_dot(
        radius=2 + cell.brightness * 8,
        color=colors.secondary,
        z_index=5
    )

    # Label auto-sized to fit inside the dot
    label = cell.add_text(
        content=f"{cell.brightness:.2f}",
        font_size=50,
        color="white" if cell.brightness < 0.5 else "black",
        font_family="monospace",
        z_index=10
    )
    label.fit_within(dot)

scene.save("text_art.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Basic Text Creation

```python
from pyfreeform import Text

text = Text(
    x=100,
    y=100,
    content="Hello World",
    font_size=18,
    color="white"
)
scene.add(text)
```

**What's happening:**
- `(x, y)`: Position of the text anchor point
- `content`: The string to display
- `font_size`: Size in pixels
- Default alignment: center horizontal, alphabetic baseline

### Step 2: Text Alignment

```python
# Horizontal alignment (text_anchor)
left_aligned = Text(
    x=100, y=50,
    content="Left",
    text_anchor="start"  # Left edge at x position
)

centered = Text(
    x=100, y=80,
    content="Center",
    text_anchor="middle"  # Center at x position
)

right_aligned = Text(
    x=100, y=110,
    content="Right",
    text_anchor="end"  # Right edge at x position
)
```

**Text Anchor Visualization:**
```
text_anchor="start":   |Hello
text_anchor="middle":  He|llo
text_anchor="end":     Hello|
                       ^ x position
```

### Step 3: Vertical Alignment

```python
# Vertical alignment (baseline)
text = Text(
    x=100, y=100,
    content="Text",
    baseline="middle"  # Vertically centered
)
```

**Baseline Options:**
- `"auto"`: Browser default
- `"middle"`: Vertically centered (recommended)
- `"hanging"`: Top of text at y position
- `"alphabetic"`: Baseline at y position
- `"ideographic"`: For CJK text

### Step 4: Font Families

```python
# Web-safe fonts
sans = Text(content="Modern", font_family="sans-serif")
serif = Text(content="Classic", font_family="serif")
mono = Text(content="Code", font_family="monospace")

# Specific fonts (may vary by system)
arial = Text(content="Arial", font_family="Arial")
georgia = Text(content="Georgia", font_family="Georgia")
```

**When to use:**
- `sans-serif`: Clean, modern, headings
- `serif`: Traditional, elegant, long text
- `monospace`: Code, data, numbers

### Step 5: Rotation

```python
# Rotate text
text = cell.add_text("Rotated", rotation=45)

# Vertical text
text = cell.add_text("Vertical", rotation=90)

# Upside down
text = cell.add_text("Flipped", rotation=180)
```

**What's happening:**
- Rotation happens around the text's anchor point
- Degrees, not radians
- Positive = clockwise

---

## Try It Yourself

### Experiment 1: Grid Labels

```python
# Column headers (A-Z)
for col in range(scene.grid.cols):
    cell = scene.grid[0, col]
    label = chr(65 + col) if col < 26 else f"A{col-25}"
    cell.add_text(
        label,
        at="top",
        font_size=12,
        color=colors.line
    )

# Row numbers
for row in range(scene.grid.rows):
    cell = scene.grid[row, 0]
    cell.add_text(
        str(row + 1),
        at="left",
        font_size=12,
        color=colors.line
    )
```

### Experiment 2: Brightness Heatmap

```python
scene = Scene.from_image("photo.jpg", grid_size=20)

for cell in scene.grid:
    # Background based on brightness
    cell.add_fill(color=cell.color, z_index=0)

    # Show brightness as number
    cell.add_text(
        content=f"{int(cell.brightness * 100)}",
        font_size=8,
        color="white" if cell.brightness < 0.5 else "black",
        font_family="monospace",
        text_anchor="middle",
        baseline="middle",
        z_index=10
    )
```

### Experiment 3: Rotating Labels

```python
for cell in scene.grid:
    # Rotation based on position
    angle = (cell.row * 20 + cell.col * 20) % 360

    cell.add_text(
        content="TEXT",
        font_size=10,
        rotation=angle,
        color=colors.primary
    )
```

### Experiment 4: Title with Shadow

```python
# Shadow (dark, behind)
shadow = Text(
    x=scene.width // 2 + 2,
    y=32,
    content="TITLE",
    font_size=36,
    color="#000000",
    font_family="sans-serif",
    text_anchor="middle",
    z_index=0
)
scene.add(shadow)

# Main title (bright, in front)
title = Text(
    x=scene.width // 2,
    y=30,
    content="TITLE",
    font_size=36,
    color=colors.primary,
    font_family="sans-serif",
    text_anchor="middle",
    z_index=1
)
scene.add(title)
```

---

## Common Patterns

### Pattern 1: Centered Title

```python
title = Text(
    x=scene.width // 2,
    y=30,
    content="My Artwork",
    font_size=24,
    color=colors.primary,
    font_family="serif",
    text_anchor="middle",  # Horizontally centered
    z_index=100  # On top of everything
)
scene.add(title)
```

### Pattern 2: Data Annotations (with fit_within)

```python
for cell in scene.grid:
    # Dot sized by data
    dot = cell.add_dot(
        radius=2 + cell.brightness * 10,
        color=colors.primary,
        z_index=5
    )

    # Label auto-sized to fit inside the dot
    label = cell.add_text(
        content=f"{cell.brightness:.2f}",
        font_size=50,  # Start large — fit_within scales down
        color="white",
        font_family="monospace",
        z_index=10
    )
    label.fit_within(dot)
```

**What's happening:** `fit_within` uses the dot's inscribed square (the largest rectangle inside the circle) to calculate the maximum font size. No manual `font_size` tuning needed — it always fits.

### Pattern 3: Corner Labels

```python
# Top-left: Title
Text(x=20, y=20, content="Title", font_size=18, text_anchor="start")

# Top-right: Date
Text(x=scene.width-20, y=20, content="2024", font_size=12, text_anchor="end")

# Bottom-left: Author
Text(x=20, y=scene.height-10, content="Artist Name", font_size=10, text_anchor="start")

# Bottom-right: Page number
Text(x=scene.width-20, y=scene.height-10, content="1", font_size=10, text_anchor="end")
```

---

## Font Sizing Guidelines

```python
# Based on typical usage
header = 24-36    # Main titles
subheader = 18-24 # Section headers
body = 12-16      # Labels, descriptions
caption = 8-12    # Small annotations
tiny = 6-8        # Fine print
```

**Relative to cell size:**
```python
# Fill cell height
text_size = cell.height * 0.7

# Consistent across grid
text_size = scene.grid.cell_size * 0.4
```

---

## Related

- 📖 [Text Entity](../../entities/06-text.md) - Full documentation
- 📖 [Layering](../../fundamentals/05-layering.md) - Z-index for text on top
- 🎯 [Groups Example](groups.md) - Previous example
- 🎯 [Multi-Layer Example](../advanced/multi-layer.md) - Complex compositions
- 🎨 [Text Art Recipe](../../recipes/07-text-art.md) - Typography patterns

