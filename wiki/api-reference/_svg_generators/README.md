# API Reference SVG Generators

This directory contains SVG generators for all API reference documentation pages.

## Generated Files

### Successfully Created Generators

1. **scene_gen.py** - Scene API examples (6/7 generated)
2. **cell_gen.py** - Cell API examples (10/12 generated)
3. **grid_gen.py** - Grid API examples (6/12 generated)
4. **entities_gen.py** - Entity types examples (1/12 generated)
5. **pathable_gen.py** - Pathable protocol examples (6/9 generated)
6. **transforms_gen.py** - Transform methods examples (10/11 generated)
7. **connections_gen.py** - Connection class examples (0/10 generated)
8. **utilities_gen.py** - Utilities and helpers examples (8/12 generated)

**Total: 47 SVG files successfully generated**

## Known API Differences (To Fix)

The generators revealed several API differences that need correction:

### Method Names
- `scene.add_entity()` → `scene.add()`  ✓ FIXED
- `entity.add_to(scene)` → `scene.add(entity)` - needs fixing

### Connection API
- `Connection(entity1, entity2, color=...)` → `Connection(entity1, entity2, "center", "center", color=...)`
- Anchors must be provided as positional arguments before kwargs

### Missing/Different Methods
- `cell.add_cross()` - does not exist
- `cell.add_x()` - does not exist
- `cell.add_rect()` - creates a custom-sized rectangle (at= positions center)
- `grid.corners()` - does not exist
- `grid.checkerboard(offset=...)` - different parameter name

### Shape Helper Arguments
- `Polygon.star(points, inner_radius=...)` - `inner_radius` not supported

### Style Objects
- `DotStyle(opacity=...)` - opacity parameter not supported

### Grid Indexing
- Negative indexing `grid[-1, -1]` not supported
- Negative row/column access `grid.row(-1)` not supported

## Usage

Generate all images for a specific file:
```bash
python3 scene_gen.py
python3 cell_gen.py
# etc.
```

Generate a specific image:
```bash
python3 scene_gen.py example1-constructor
```

Generate all images:
```bash
for gen in *.py; do python3 "$gen"; done
```

## Output

All generated SVGs are saved to:
```
../images/{filename}/example{N}-{name}.svg
```

For example:
- `../images/scene/example1-constructor.svg`
- `../images/cell/example1-named-positions.svg`
- etc.

## Next Steps

1. Fix the remaining API differences in the generators
2. Verify all generated SVGs render correctly
3. Embed SVG references in the markdown documentation
4. Add more examples for comprehensive coverage

## File Structure

```
api-reference/
├── _svg_generators/
│   ├── scene_gen.py
│   ├── cell_gen.py
│   ├── grid_gen.py
│   ├── entities_gen.py
│   ├── pathable_gen.py
│   ├── transforms_gen.py
│   ├── connections_gen.py
│   ├── utilities_gen.py
│   └── README.md (this file)
└── _images/
    ├── scene/
    ├── cell/
    ├── grid/
    ├── entities/
    ├── pathable/
    ├── transforms/
    ├── connections/
    └── utilities/
```
