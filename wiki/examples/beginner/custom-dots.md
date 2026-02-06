
# Example: Custom Dots

**Difficulty**: ⭐ Beginner

Use palettes and styling to create beautiful dot art with consistent color schemes.

---

## What You'll Learn

- Using Palette objects for color schemes
- DotStyle for reusable configurations
- Sizing dots based on brightness
- Conditional rendering

---

## Final Result

![Brightness Tiers](../_images/custom-dots/01_brightness_tiers.svg)

### More Examples

| Brightness Tiers | Palette Variation | Size Scaling |
|------------------|-------------------|--------------|
| ![Example 1](../_images/custom-dots/01_brightness_tiers.svg) | ![Example 2](../_images/custom-dots/02_palette_variation.svg) | ![Example 3](../_images/custom-dots/03_size_scaling.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette
from pyfreeform.config import DotStyle

scene = Scene.from_image("photo.jpg", grid_size=40)
colors = Palette.midnight()
scene.background = colors.background

# Create reusable styles
large_style = DotStyle(radius=8, color=colors.primary)
small_style = DotStyle(radius=3, color=colors.secondary)

for cell in scene.grid:
    # Size based on brightness
    if cell.brightness > 0.6:
        size = 5 + cell.brightness * 5  # 5-10px
        cell.add_dot(radius=size, color=colors.primary)
    elif cell.brightness > 0.3:
        size = 3 + cell.brightness * 4  # 3-7px
        cell.add_dot(radius=size, color=colors.secondary)
    else:
        cell.add_dot(radius=2, color=colors.accent)

scene.save("custom_dots.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Setup with Palette

```python
from pyfreeform import Scene, Palette

scene = Scene.from_image("photo.jpg", grid_size=40)
colors = Palette.midnight()
scene.background = colors.background
```

**What's happening:**
- `Palette.midnight()` provides a coordinated color scheme
- `scene.background` sets the canvas background color
- Palettes ensure colors work well together

### Step 2: Conditional Rendering

```python
for cell in scene.grid:
    if cell.brightness > 0.6:
        # Bright areas: large primary color dots
        size = 5 + cell.brightness * 5
        cell.add_dot(radius=size, color=colors.primary)
    elif cell.brightness > 0.3:
        # Medium areas: medium secondary color dots
        size = 3 + cell.brightness * 4
        cell.add_dot(radius=size, color=colors.secondary)
    else:
        # Dark areas: small accent dots
        cell.add_dot(radius=2, color=colors.accent)
```

**What's happening:**
- Three brightness thresholds create visual tiers
- Size scales with brightness within each tier
- Different colors for each tier create depth

### Step 3: Using DotStyle (Alternative)

```python
from pyfreeform.config import DotStyle

# Define reusable styles
bright_style = DotStyle(radius=8, color=colors.primary)
medium_style = DotStyle(radius=5, color=colors.secondary)
dark_style = DotStyle(radius=2, color=colors.accent)

for cell in scene.grid:
    if cell.brightness > 0.6:
        cell.add_dot(style=bright_style)
    elif cell.brightness > 0.3:
        cell.add_dot(style=medium_style)
    else:
        cell.add_dot(style=dark_style)
```

**What's happening:**
- `DotStyle` objects are reusable configurations
- Cleaner code when using the same style repeatedly
- Easy to modify all dots of one style at once

---

## Try It Yourself

### Experiment 1: Different Palettes

```python
# Try different color schemes
colors = Palette.ocean()
colors = Palette.sunset()
colors = Palette.forest()
colors = Palette.pastel()
```

### Experiment 2: More Brightness Levels

```python
# Five levels instead of three
if cell.brightness > 0.8:
    cell.add_dot(radius=10, color=colors.primary)
elif cell.brightness > 0.6:
    cell.add_dot(radius=7, color=colors.secondary)
elif cell.brightness > 0.4:
    cell.add_dot(radius=5, color=colors.accent)
elif cell.brightness > 0.2:
    cell.add_dot(radius=3, color=colors.line)
else:
    cell.add_dot(radius=1, color=colors.grid)
```

### Experiment 3: Inverted Brightness

```python
# Larger dots in dark areas (halftone effect)
for cell in scene.grid:
    size = 2 + (1 - cell.brightness) * 8  # Invert: 2-10px
    cell.add_dot(radius=size, color="black")
```

---

## Related

- 📖 [Dots Entity](../../entities/01-dots.md) - Full documentation
- 📖 [Palettes Guide](../../color-and-style/02-palettes.md) - Color schemes
- 📖 [Style Objects](../../color-and-style/03-style-objects.md) - Reusable styles
- 🎯 [Quick Start](quick-start.md) - Simpler example
- 🎨 [Dot Art Recipe](../../recipes/01-dot-art-from-images.md) - More patterns

