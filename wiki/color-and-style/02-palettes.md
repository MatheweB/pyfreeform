
# Palettes

Pre-built color schemes for cohesive artwork.

## Available Palettes

```python
from pyfreeform import Palette

Palette.midnight()    # Dark blue theme
Palette.sunset()      # Warm oranges
Palette.ocean()       # Cool blues
Palette.forest()      # Natural greens
Palette.monochrome()  # Black and white
Palette.paper()       # Beige tones
Palette.neon()        # Vibrant colors
Palette.pastel()      # Soft colors
```

### Midnight
![Midnight Palette](_images/02-palettes/01-palette-midnight.svg)

### Sunset
![Sunset Palette](_images/02-palettes/02-palette-sunset.svg)

### Ocean
![Ocean Palette](_images/02-palettes/03-palette-ocean.svg)

### Forest
![Forest Palette](_images/02-palettes/04-palette-forest.svg)

### Monochrome
![Monochrome Palette](_images/02-palettes/05-palette-monochrome.svg)

### Paper
![Paper Palette](_images/02-palettes/06-palette-paper.svg)

### Neon
![Neon Palette](_images/02-palettes/07-palette-neon.svg)

### Pastel
![Pastel Palette](_images/02-palettes/08-palette-pastel.svg)

### All Palettes Comparison
![All Palettes](_images/02-palettes/14-all-palettes-comparison.svg)

## Palette Properties

```python
colors = Palette.ocean()

colors.background  # Background color
colors.primary     # Main color
colors.secondary   # Secondary color
colors.accent      # Highlight color
colors.line        # Line/stroke color
colors.grid        # Grid/border color
```

![Palette Properties](_images/02-palettes/09-palette-properties.svg)

## Usage

```python
scene = Scene.from_image("photo.jpg", grid_size=40)
colors = Palette.midnight()

scene.background = colors.background

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(color=colors.primary)
    elif cell.brightness > 0.4:
        cell.add_dot(color=colors.secondary)
    else:
        cell.add_dot(color=colors.accent)
```

### Before Applying Palette
![Before Palette](_images/02-palettes/10-usage-before-palette.svg)

### With Midnight Palette
![With Midnight](_images/02-palettes/11-usage-with-midnight.svg)

### With Ocean Palette
![With Ocean](_images/02-palettes/12-usage-with-ocean.svg)

### With Sunset Palette
![With Sunset](_images/02-palettes/13-usage-with-sunset.svg)

## See Also
- [Color System](01-color-system.md)
- [Style Objects](03-style-objects.md)
