
# Entity Groups

EntityGroups let you define reusable composite shapes — a flower, a crosshair, a logo — and place them like any other entity.

---

## What is an EntityGroup?

An **EntityGroup** bundles multiple entities into one:

- **Children** are positioned relative to `(0, 0)` — the group's local origin
- **Placement** works like any entity — `cell.place()`, `scene.add()`, `fit_to_cell()`
- **SVG output** uses `<g transform="translate(x,y) scale(s)">` — children are never mutated

![What is an EntityGroup](./_images/08-entity-groups/01_what_is.svg)

---

## Creating Entity Groups

Build groups by adding entities relative to the local origin:

```python
from pyfreeform import EntityGroup, Dot
import math

flower = EntityGroup()

# Center dot at the origin
flower.add(Dot(0, 0, radius=10, color="coral"))

# Petals around the center
for i in range(8):
    angle = i * (2 * math.pi / 8)
    x = 15 * math.cos(angle)
    y = 15 * math.sin(angle)
    flower.add(Dot(x, y, radius=6, color="gold"))
```

![Creating an EntityGroup](./_images/08-entity-groups/02_creating.svg)

### Direct Construction

```python
from pyfreeform import EntityGroup, Dot, Line

# Crosshair marker
marker = EntityGroup()
marker.add(Line(-10, 0, 10, 0, width=1, color="white"))
marker.add(Line(0, -10, 0, 10, width=1, color="white"))
marker.add(Dot(0, 0, radius=3, color="white"))

scene.add(marker.move_to(200, 150))
```

### Via Factory Functions (Recommended)

Wrap creation in a function for reuse — each call returns a fresh instance:

```python
def make_flower(color="coral", petal_color="gold", petal_count=8):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=10, color=color))
    for i in range(petal_count):
        angle = i * (2 * math.pi / petal_count)
        g.add(Dot(15 * math.cos(angle), 15 * math.sin(angle),
                   radius=6, color=petal_color))
    return g

cell1.place(make_flower(color="red"))
cell2.place(make_flower(color="blue"))
```

---

## Placement

EntityGroup supports all standard placement methods:

```python
# Place at absolute position
scene.add(flower.move_to(100, 100))

# Center in a cell
cell.place(flower)

# Same thing, add_* naming convention
cell.add_entity(flower)

# Specific position within a cell
cell.add_entity(flower, at="top_left")
cell.add_entity(flower, at=(0.3, 0.7))
```

![Placement](./_images/08-entity-groups/03_placement.svg)

---

## Properties

```python
group.children      # list of child entities (copy)
group.x, group.y    # Position
group.z_index       # Layer order
```

---

## Anchors

```python
group.anchor_names  # ["center"]
group.anchor("center")  # Center of bounding box
```

---

## Common Patterns

### Pattern 1: Stamp Across a Grid

```python
for cell in scene.grid:
    flower = make_flower(color=colors.primary, petal_color=colors.accent)
    cell.place(flower)
    flower.fit_to_cell(0.75)
```

### Pattern 2: Data-Driven Variation

```python
for cell in scene.grid:
    count = 4 + int(cell.brightness * 8)
    flower = make_flower(petal_count=count, color=cell.color)
    cell.place(flower)
    flower.fit_to_cell(0.8)
```

### Pattern 3: Nested Groups

```python
def make_bouquet(center_color, petal_colors):
    bouquet = EntityGroup()
    bouquet.add(make_flower(color=center_color))
    for i in range(5):
        angle = i * (2 * math.pi / 5)
        outer = make_flower(color=petal_colors[i % len(petal_colors)], petal_count=6)
        outer.scale(0.6)
        outer.move_to(45 * math.cos(angle), 45 * math.sin(angle))
        bouquet.add(outer)
    return bouquet
```

---

## Auto-Sizing with fit_to_cell

Scale the group to fit within its cell bounds:

```python
cell.place(flower)
flower.fit_to_cell(0.75)  # 75% of cell size
```

![fit_to_cell](./_images/08-entity-groups/04_fit_to_cell.svg)

---

## Complete Example

```python
from pyfreeform import Scene, Palette, EntityGroup, Dot
import math

def make_flower(color="coral", petal_color="gold", petal_count=8):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=10, color=color))
    for i in range(petal_count):
        angle = i * (2 * math.pi / petal_count)
        g.add(Dot(15 * math.cos(angle), 15 * math.sin(angle),
                   radius=6, color=petal_color))
    return g

colors = Palette.ocean()
scene = Scene.with_grid(cols=8, rows=5, cell_size=45)
scene.background = colors.background

for cell in scene.grid:
    petal_count = 4 + (cell.col % 4) * 2
    flower = make_flower(
        color=colors.primary,
        petal_color=colors.accent,
        petal_count=petal_count,
    )
    cell.place(flower)
    flower.fit_to_cell(0.75)

scene.save("entity_groups.svg")
```

![Complete Example](./_images/08-entity-groups/05_complete.svg)

---

## EntityGroup vs CellGroup

PyFreeform has two kinds of "groups" — they solve different problems:

| | EntityGroup | CellGroup |
|-|------------|-----------|
| **Purpose** | Reusable composite shapes | Multi-cell surface regions |
| **Inherits from** | `Entity` | `Surface` |
| **Has** | Child entities | Builder methods (add_dot, add_text, ...) |
| **Placement** | `cell.place()`, `scene.add()` | Already positioned by its cells |
| **Use for** | Custom shapes, stamps, patterns | Headers, sidebars, multi-cell labels |

---

## Tips

!!! tip "Use Factory Functions"
    Each call returns a new independent instance — no shared state between placements.

!!! tip "fit_to_cell() for Consistent Sizing"
    Automatically scales groups to fit within cells, regardless of the group's internal dimensions.

---

## See Also

- [EntityGroup Examples](../examples/intermediate/groups.md) — Full walkthrough with 4 examples
- [Fit to Cell](../advanced-concepts/05-fit-to-cell.md) — Auto-scaling details
- [Transforms](../advanced-concepts/04-transforms.md) — Scale, rotate, move
- [Entities API Reference](../api-reference/entities.md) — Full EntityGroup API
