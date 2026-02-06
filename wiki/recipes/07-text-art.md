
# Recipe: Text Art

Create typographic artwork using text labels, data overlays, and decorative typography.

---

## Visual Result

![Text art with title, data labels, and rotating text](./_images/07-text-art/01_data_labels.svg)

Text adds context, data, and artistic expression to your compositions.

---

## Why This Works

Text bridges the gap between pure abstraction and concrete meaning. While geometric shapes and colors create emotional responses, text provides explicit information, creates narrative, or serves as a design element itself. Typography can be both functional (labels, data) and decorative (patterns, art).

The power of text in generative art comes from:

- **Dual nature**: Text is both visual (shape, rhythm) and semantic (meaning)
- **Instant recognition**: Our brains process text automatically
- **Data visualization**: Numbers and labels make abstract values concrete
- **Cultural resonance**: Letterforms carry typographic history and associations
- **Contrast**: Text provides hard edges against organic shapes

!!! tip "When to Use This Technique"
    Choose text art when you want:

    - Data visualization (showing values, coordinates, statistics)
    - Conceptual work (adding meaning or narrative to abstract compositions)
    - Hybrid designs (mixing generative art with infographic elements)
    - Typography experiments (exploring letterforms as visual elements)
    - Accessibility (adding labels makes artwork more interpretable)

---

## The Pattern

**Key Idea**: Use text to label, annotate, or create typographic compositions.

```python
for cell in scene.grid:
    # Display brightness value
    value = f"{cell.brightness:.2f}"

    cell.add_text(
        content=value,
        font_size=10,
        color="white",
        font_family="monospace"
    )
```

---

## Complete Examples

### Data Visualization

```python
from pyfreeform import Scene, Palette

scene = Scene.from_image("photo.jpg", grid_size=20)
colors = Palette.paper()
scene.background = colors.background

for cell in scene.grid:
    # Background color based on brightness
    cell.add_fill(color=cell.color, z_index=0)

    # Display brightness value
    value = f"{cell.brightness:.2f}"

    # Choose text color for contrast
    text_color = "white" if cell.brightness < 0.5 else "black"

    cell.add_text(
        content=value,
        font_size=8,
        color=text_color,
        font_family="monospace",
        text_anchor="middle",
        baseline="middle",
        z_index=10
    )

scene.save("data_text_art.svg")
```

### Typographic Grid

```python
from pyfreeform import Scene, Palette

scene = Scene.with_grid(cols=8, rows=8, cell_size=40)
colors = Palette.midnight()
scene.background = colors.background

# Chess-style labels
letters = "ABCDEFGH"

for cell in scene.grid:
    # Checkerboard background
    if (cell.row + cell.col) % 2 == 0:
        cell.add_fill(color=colors.grid, z_index=0)

    # Column letter on top row
    if cell.row == 0:
        cell.add_text(
            content=letters[cell.col],
            font_size=16,
            color=colors.primary,
            font_family="serif",
            z_index=10
        )

    # Row number on left column
    if cell.col == 0:
        cell.add_text(
            content=str(8 - cell.row),
            font_size=16,
            color=colors.primary,
            font_family="serif",
            z_index=10
        )

scene.save("chess_labels.svg")
```

![Chess-style grid with column letters and row numbers](./_images/07-text-art/02_chess_labels.svg)

---

## Text Variations

### Rotating Text

```python
for cell in scene.grid:
    # Rotation based on position
    angle = (cell.row + cell.col) * 15

    cell.add_text(
        content="ART",
        font_size=12,
        rotation=angle,
        color=cell.color
    )
```

![Text "ART" rotating at different angles](./_images/07-text-art/03_rotating_text.svg)

### Size Variations

```python
for cell in scene.grid:
    # Font size based on brightness
    size = 8 + cell.brightness * 16  # 8 to 24

    cell.add_text(
        content="•",  # Bullet point
        font_size=size,
        color=cell.color
    )
```

![Bullet points with size varying based on brightness](./_images/07-text-art/04_size_variations.svg)

### Position-Based Characters

```python
# Create patterns with characters
characters = ["●", "◐", "◑", "◒", "◓", "○"]

for cell in scene.grid:
    # Choose character based on brightness
    char_idx = int(cell.brightness * (len(characters) - 1))
    char = characters[char_idx]

    cell.add_text(
        content=char,
        font_size=14,
        color="white"
    )
```

![Unicode circle symbols representing brightness levels](./_images/07-text-art/09_unicode_symbols.svg)

---

## Advanced Techniques

### Overlay Title

Add a title over the entire scene:

```python
from pyfreeform import Text

# Create artwork
for cell in scene.grid:
    cell.add_dot(radius=5, color=cell.color)

# Add title overlay
title = Text(
    x=scene.width // 2,
    y=30,
    content="GENERATIVE ART",
    font_size=32,
    color="white",
    font_family="serif",
    text_anchor="middle",
    z_index=1000  # On top of everything
)
scene.add(title)
```

![Title overlay text on top of dot artwork](./_images/07-text-art/08_title_overlay.svg)

### Color-Coded Labels

```python
for cell in scene.grid:
    if cell.brightness > 0.7:
        label = "HIGH"
        color = "gold"
    elif cell.brightness > 0.4:
        label = "MED"
        color = "silver"
    else:
        label = "LOW"
        color = "bronze"

    cell.add_text(
        content=label,
        font_size=8,
        color=color,
        font_family="sans-serif"
    )
```

![Color-coded HIGH, MED, LOW labels based on brightness](./_images/07-text-art/06_color_coded.svg)

### Coordinates Display

```python
for cell in scene.grid:
    # Display (row, col) coordinates
    coords = f"({cell.row},{cell.col})"

    cell.add_text(
        content=coords,
        font_size=6,
        color="gray",
        font_family="monospace"
    )
```

![Grid coordinates displayed in each cell](./_images/07-text-art/07_coordinates.svg)

### ASCII Art Style

```python
# Use ASCII characters for shading
ascii_chars = " .:-=+*#%@"

for cell in scene.grid:
    # Choose character based on brightness
    char_idx = int(cell.brightness * (len(ascii_chars) - 1))
    char = ascii_chars[char_idx]

    cell.add_text(
        content=char,
        font_size=16,
        color="white",
        font_family="monospace"
    )
```

![ASCII art style with various characters representing brightness levels](./_images/07-text-art/05_ascii_art.svg)

---

## Font Families

### Web-Safe Fonts

```python
# Sans-serif (clean, modern)
cell.add_text("Modern", font_family="sans-serif")

# Serif (traditional, elegant)
cell.add_text("Classic", font_family="serif")

# Monospace (code, data)
cell.add_text("0.85", font_family="monospace")
```

![Different font families: sans-serif, serif, and monospace](./_images/07-text-art/10_mixed_fonts.svg)

**Tip**: Stick with generic families for maximum compatibility across systems.

---

## Text Alignment

### Horizontal Alignment

```python
# Left-aligned
cell.add_text("Left", text_anchor="start")

# Centered (default)
cell.add_text("Center", text_anchor="middle")

# Right-aligned
cell.add_text("Right", text_anchor="end")
```

### Vertical Alignment

```python
# Top
cell.add_text("Top", baseline="hanging")

# Middle (recommended)
cell.add_text("Middle", baseline="middle")

# Bottom
cell.add_text("Bottom", baseline="alphabetic")
```

### Perfect Centering

```python
# Both horizontally and vertically centered
cell.add_text(
    "CENTERED",
    text_anchor="middle",  # Horizontal
    baseline="middle"      # Vertical
)
```

---

## Tips

### Contrast for Readability

Always ensure text is visible:

```python
# Choose text color based on background
text_color = "white" if cell.brightness < 0.5 else "black"

cell.add_text(content="Text", color=text_color)
```

### Size Relative to Cell

```python
# Font size proportional to cell height
font_size = cell.height * 0.6

cell.add_text("A", font_size=font_size)
```

### Monospace for Data

Use monospace for numbers and tabular data:

```python
cell.add_text(
    f"{cell.brightness:.3f}",
    font_family="monospace",
    font_size=8
)
```

### Layer Text on Top

Always use high z-index for text:

```python
# Background
cell.add_fill(color=colors.background, z_index=0)

# Text on top
cell.add_text("LABEL", z_index=100)
```

![Text numbers layered on top of dot shapes](./_images/07-text-art/11_text_with_shapes.svg)

### Wave Text

```python
import math

for cell in scene.grid:
    # Vertical offset based on sine wave
    phase = cell.col / scene.grid.cols * math.pi * 2
    dy = math.sin(phase) * 5

    cell.add_text(
        content="~",
        font_size=14,
        color=cell.color,
        dy=dy
    )
```

![Wave text with sinusoidal vertical displacement](./_images/07-text-art/12_wave_text.svg)

---

## Parameter Tuning Guide

### Font Size Selection

Font size determines readability and visual density:

```python
# Small (data labels, subtle annotations)
font_size = 6  # Hard to read but creates texture

# Medium (readable labels)
font_size = 10  # Clear at typical viewing distances

# Large (titles, emphasis)
font_size = 20  # Dominant visual element

# Responsive to cell size
font_size = cell.height * 0.6  # Scales with grid
```

!!! tip "Font Size Guidelines"
    - Data visualization: 8-12pt ensures readability
    - Decorative patterns: 6-10pt for texture
    - Titles/headers: 20-32pt for hierarchy
    - Single characters: 12-24pt for shape clarity

### Text Color for Contrast

Always ensure text is visible against backgrounds:

```python
# Simple threshold
text_color = "white" if cell.brightness < 0.5 else "black"

# More sophisticated (considers color, not just brightness)
if cell.brightness < 0.4:
    text_color = "white"
elif cell.brightness > 0.6:
    text_color = "black"
else:
    text_color = "gray"  # Medium backgrounds: use gray
```

!!! warning "Contrast Ratio Matters"
    For accessibility, maintain at least 4.5:1 contrast ratio between text and background. White on dark (or black on light) always works; colored text requires testing.

### Alignment Strategies

```python
# Centered (default, works for most cases)
cell.add_text(
    content="X",
    text_anchor="middle",
    baseline="middle"
)

# Top-left aligned (like coordinates)
cell.add_text(
    content=f"({cell.row},{cell.col})",
    text_anchor="start",  # Left edge
    baseline="hanging"     # Top edge
)

# Bottom-right aligned (like signatures)
cell.add_text(
    content="©",
    text_anchor="end",     # Right edge
    baseline="alphabetic"  # Bottom edge
)
```

### Font Family Choice

```python
# Monospace (data, code, technical)
cell.add_text(
    content=f"{cell.brightness:.3f}",
    font_family="monospace"
)

# Sans-serif (modern, clean, minimal)
cell.add_text(
    content="MODERN",
    font_family="sans-serif"
)

# Serif (traditional, elegant, formal)
cell.add_text(
    content="Classic",
    font_family="serif"
)
```

!!! info "Web-Safe Font Families"
    Stick with generic families (`monospace`, `sans-serif`, `serif`) for maximum compatibility. SVGs render on different systems; specific fonts (like "Arial" or "Helvetica") may not be available.

---

## Common Pitfalls

### Pitfall 1: Using `fill=` Instead of `color=`

```python
# ❌ WRONG - Text uses color=, not fill=
cell.add_text(content="Hello", fill="red")  # Won't work!

# ✅ CORRECT - Use color= for text
cell.add_text(content="Hello", color="red")
```

!!! warning "Text Uses color="
    Text, dots, lines, and curves use `color=`. Only polygons, ellipses, and rectangles use `fill=`. Remember: text is drawn with stroke/fill in SVG, but PyFreeform simplifies this to `color=`.

### Pitfall 2: Text Appearing Behind Other Elements

```python
# ❌ WRONG - Text might be hidden
cell.add_fill(color=colors.background, z_index=5)
cell.add_text(content="LABEL", z_index=1)  # Behind the fill!

# ✅ CORRECT - Text on top
cell.add_fill(color=colors.background, z_index=0)
cell.add_text(content="LABEL", z_index=10)  # In front
```

### Pitfall 3: Not Formatting Numbers

```python
# ❌ WRONG - Too many decimal places
cell.add_text(content=str(cell.brightness))  # "0.7834756287346"

# ✅ CORRECT - Format to 2 decimal places
cell.add_text(content=f"{cell.brightness:.2f}")  # "0.78"
```

### Pitfall 4: Forgetting to Center Text

```python
# ❌ WRONG - Text left-aligned by default (may appear off-center)
cell.add_text(content="X")

# ✅ CORRECT - Explicitly center
cell.add_text(
    content="X",
    text_anchor="middle",
    baseline="middle"
)
```

### Pitfall 5: Using Non-ASCII Characters Without Checking

```python
# ⚠️ CAUTION - Unicode symbols may not render on all systems
cell.add_text(content="◉")  # Works on most modern systems
cell.add_text(content="☃")  # Snowman might not appear everywhere

# ✅ SAFER - Stick to common symbols
cell.add_text(content="•")  # Bullet: very common
cell.add_text(content="*")  # Asterisk: universally supported
```

!!! info "Unicode Support"
    Most modern systems support Unicode symbols, but exotic characters may fail. Test your output on multiple platforms if using symbols beyond basic Latin/numbers.

---

## Best Practices

### 1. Always Ensure Sufficient Contrast

```python
# Calculate contrast automatically
def get_text_color(brightness):
    """Return high-contrast text color for given background brightness."""
    return "white" if brightness < 0.5 else "black"

for cell in scene.grid:
    cell.add_fill(color=cell.color, z_index=0)
    text_color = get_text_color(cell.brightness)
    cell.add_text(
        content=f"{cell.brightness:.2f}",
        color=text_color,
        z_index=10
    )
```

### 2. Use Monospace for Tabular Data

```python
# Monospace keeps digits aligned (important for comparing values)
cell.add_text(
    content=f"{cell.brightness:.3f}",
    font_family="monospace",
    font_size=8
)
```

### 3. Layer Text Above All Other Elements

```python
# Standard z-index convention
cell.add_fill(color=colors.background, z_index=0)     # Background
cell.add_polygon(shapes.hexagon(), fill=colors.primary, z_index=5)  # Shapes
cell.add_text(content="LABEL", z_index=100)           # Text on top
```

### 4. Format Data Consistently

```python
# All brightness values: 2 decimal places
value = f"{cell.brightness:.2f}"

# All coordinates: zero-padded
coords = f"({cell.row:02d},{cell.col:02d})"  # "(03,07)" not "(3,7)"

# All percentages: no decimal places
percent = f"{cell.brightness * 100:.0f}%"  # "78%" not "78.3%"
```

### 5. Test Readability at Target Size

```python
# Preview at actual output size
scene = Scene.with_grid(cols=20, rows=20, cell_size=30)

# If text too small, increase cell_size or font_size
# If text too large, decrease accordingly
```

!!! tip "Readability Test"
    Save a preview SVG and view it at 100% zoom in a web browser. Can you comfortably read all text? If not, adjust font sizes.

---

## Advanced Techniques

### Dynamic Font Size Based on Content Length

```python
# Shorter strings = larger font
for cell in scene.grid:
    content = cell.color  # Hex code like "#FF5733"
    base_size = 12

    # Adjust size based on length
    font_size = base_size * (5 / len(content))  # Longer strings = smaller

    cell.add_text(
        content=content,
        font_size=font_size,
        color=get_contrast_color(cell.brightness)
    )
```

### Rotating Text for Diagonal Labels

```python
# Rotate text 45° for diagonal emphasis
for cell in scene.grid:
    angle = 45

    cell.add_text(
        content="ART",
        rotation=angle,
        color=cell.color,
        font_size=12
    )
```

!!! info "Text Rotation"
    Text rotation works just like shape rotation. Use sparingly - rotated text is harder to read but creates dynamic compositions.

### Creating Text-Based Gradients

```python
# Use varying brightness symbols to create gradients
brightness_chars = " .:-=+*#%@"

for cell in scene.grid:
    char_index = int(cell.brightness * (len(brightness_chars) - 1))
    char = brightness_chars[char_index]

    cell.add_text(
        content=char,
        font_size=14,
        color="white",
        font_family="monospace"
    )
```

### Overlay Title with Semi-Transparent Background

```python
from pyfreeform import Text, Rect

# Create main artwork
for cell in scene.grid:
    cell.add_dot(radius=5, color=cell.color)

# Add semi-transparent background for title
title_bg = Rect(
    x=scene.width // 2 - 150,
    y=10,
    width=300,
    height=50,
    fill="black",
    opacity=0.7,
    z_index=900
)
scene.add(title_bg)

# Add title text on top
title = Text(
    x=scene.width // 2,
    y=35,
    content="GENERATIVE ART",
    font_size=24,
    color="white",
    font_family="sans-serif",
    text_anchor="middle",
    baseline="middle",
    z_index=1000
)
scene.add(title)
```

### Conditional Text Display

```python
# Only show text for interesting cells
for cell in scene.grid:
    # Show value only for bright cells
    if cell.brightness > 0.7:
        cell.add_text(
            content=f"{cell.brightness:.2f}",
            color="gold",
            font_size=10,
            font_family="monospace"
        )
    # Show nothing for dim cells (reduces clutter)
```

### Creating Text Patterns with Symbols

```python
# Use symbols as decorative elements
symbols = ["●", "▲", "■", "◆", "★"]

for cell in scene.grid:
    symbol_idx = (cell.row + cell.col) % len(symbols)
    symbol = symbols[symbol_idx]

    cell.add_text(
        content=symbol,
        font_size=16,
        color=cell.color,
        text_anchor="middle",
        baseline="middle"
    )
```

### Multi-Line Text in Cells

```python
# SVG doesn't natively support multi-line text in add_text
# Workaround: add multiple text entities with vertical offset

line1 = cell.add_text(
    content="Line 1",
    font_size=8,
    color="white",
    dy=-6  # Shift up
)

line2 = cell.add_text(
    content="Line 2",
    font_size=8,
    color="white",
    dy=6  # Shift down
)
```

!!! warning "Multi-Line Limitations"
    SVG text doesn't automatically wrap. For multi-line text, manually create multiple `Text` entities with vertical offsets. Keep lines short for best results.

---

## Typography as Art

### Creating Texture with Repeated Characters

```python
# Dense text creates visual texture
for cell in scene.grid:
    cell.add_text(
        content="█",  # Full block character
        font_size=20,
        color=cell.color
    )
```

### Brightness-Responsive Character Sets

```python
# Different characters for different brightness levels
ascii_gradient = " .:-=+*#%@"

for cell in scene.grid:
    char_idx = int(cell.brightness * (len(ascii_gradient) - 1))
    char = ascii_gradient[char_idx]

    cell.add_text(
        content=char,
        font_size=14,
        color="white",
        font_family="monospace"
    )
```

### Typographic Grid with Letter Coordinates

```python
# A-H columns, 1-8 rows (chess board style)
letters = "ABCDEFGH"

for cell in scene.grid:
    if cell.row == 0:  # Top row: show column letters
        cell.add_text(
            content=letters[cell.col],
            font_size=16,
            color=colors.primary,
            font_family="serif"
        )

    if cell.col == 0:  # Left column: show row numbers
        cell.add_text(
            content=str(scene.grid.rows - cell.row),
            font_size=16,
            color=colors.primary,
            font_family="serif"
        )
```

### Rotating Text Wave

```python
import math

for cell in scene.grid:
    # Wave-based rotation
    phase = cell.col / scene.grid.cols * math.pi * 2
    rotation = math.sin(phase) * 45  # -45° to +45°

    cell.add_text(
        content="~",
        font_size=16,
        rotation=rotation,
        color=cell.color
    )
```

---

## Combining Text with Other Techniques

### Text + Geometric Patterns

```python
# Background: geometric shape
poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary, z_index=0)
poly.rotate((cell.row + cell.col) * 15)

# Foreground: text label
cell.add_text(
    content=f"{cell.row}",
    font_size=10,
    color="white",
    z_index=10
)
```

### Text + Connected Networks

```python
# Create network of dots
dot = cell.add_dot(radius=3, color=colors.primary, z_index=5)

# Label each node
cell.add_text(
    content=str(cell.row * scene.grid.cols + cell.col),  # Node ID
    font_size=6,
    color="white",
    z_index=15
)
```

### Text + Rotating Shapes

```python
# Rotating shape
poly = cell.add_polygon(shapes.star(5), fill=colors.primary, z_index=0)
poly.rotate((cell.row + cell.col) * 30)

# Static text label
cell.add_text(
    content="★",
    font_size=12,
    color="gold",
    z_index=10
)
```

---

## Accessibility Considerations

### Adding Alt-Text Context

While SVG text is inherently accessible (screen readers can read it), consider adding context:

```python
# Good: descriptive labels
cell.add_text(content=f"Brightness: {cell.brightness:.2f}")

# Less helpful: raw numbers without context
cell.add_text(content=f"{cell.brightness:.2f}")
```

### Ensuring Readable Font Sizes

```python
# Minimum recommended font sizes for accessibility
MINIMUM_READABLE = 10  # Points

for cell in scene.grid:
    font_size = max(MINIMUM_READABLE, cell.height * 0.5)
    cell.add_text(content="TEXT", font_size=font_size)
```

### High-Contrast Color Choices

```python
# Ensure text meets WCAG contrast guidelines
def get_high_contrast_color(brightness):
    """Returns white or black for maximum contrast."""
    return "white" if brightness < 0.5 else "black"

# Use throughout artwork
text_color = get_high_contrast_color(cell.brightness)
cell.add_text(content="LABEL", color=text_color)
```

---

## See Also

- 📖 [Text](../entities/06-text.md) - Text entity documentation
- 📖 [Layering](../fundamentals/05-layering.md) - Z-index for text
- 🎯 [Text Example](../examples/intermediate/text.md) - Detailed examples
- 🎯 [Text Showcase](../examples/intermediate/text.md) - Typography patterns

