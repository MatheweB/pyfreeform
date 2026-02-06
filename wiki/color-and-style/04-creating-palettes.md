
# Creating Custom Palettes

Create your own color schemes.

## Custom Palette

```python
from pyfreeform.config import Palette

# Create custom palette
my_palette = Palette(
    background="#1a1a2e",
    primary="#16213e",
    secondary="#0f3460",
    accent="#e94560",
    line="#533483",
    grid="#2d2d44"
)

# Use it
scene.background = my_palette.background
cell.add_dot(color=my_palette.primary)
```

![Custom Palette Definition](_images/04-creating-palettes/01-custom-palette-definition.svg)

![Custom Palette Usage](_images/04-creating-palettes/02-custom-palette-usage.svg)

![Custom Palette Artistic](_images/04-creating-palettes/03-custom-palette-artistic.svg)

## From Existing Palette

```python
# Start with existing
colors = Palette.ocean()

# Modify
custom = Palette(
    background=colors.background,
    primary="#ff0000",  # Custom red
    secondary=colors.secondary,
    accent=colors.accent,
    line=colors.line,
    grid=colors.grid
)
```

### Original Ocean Palette
![Existing Palette Base](_images/04-creating-palettes/04-existing-palette-base.svg)

### Modified with Custom Red
![Modified Palette](_images/04-creating-palettes/05-modified-palette.svg)

### Side-by-Side Comparison
![Palette Comparison](_images/04-creating-palettes/06-palette-comparison.svg)

## Color Theory Tips

- **Complementary**: Opposite on color wheel (blue/orange)
- **Analogous**: Adjacent colors (blue/cyan/teal)
- **Triadic**: Evenly spaced (red/yellow/blue)
- **Monochromatic**: Shades of one color

### Complementary Colors
![Complementary Colors](_images/04-creating-palettes/07-complementary-colors.svg)

### Analogous Colors
![Analogous Colors](_images/04-creating-palettes/08-analogous-colors.svg)

### Triadic Colors
![Triadic Colors](_images/04-creating-palettes/09-triadic-colors.svg)

### Monochromatic Colors
![Monochromatic Colors](_images/04-creating-palettes/10-monochromatic-colors.svg)

### Color Harmony in Practice
![Color Harmony Palette](_images/04-creating-palettes/11-color-harmony-palette.svg)

### Warm vs Cool Palettes
![Warm vs Cool](_images/04-creating-palettes/12-warm-vs-cool-palettes.svg)

## See Also
- [Palettes](02-palettes.md)
- [Color System](01-color-system.md)
