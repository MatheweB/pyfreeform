# wiki_v2 Design-Flow Document

> The blueprint for the new PyFreeform documentation.
> Describes the structure, user experience, visual design, generation system,
> and every page in the new wiki.

---

## Philosophy

**One sentence**: PyFreeform turns images and ideas into beautiful SVG art through an elegant grid-and-cell system.

The wiki should feel like opening a beautifully typeset art book, not reading API documentation. Every page should produce a visual result that makes the reader think *"I want to try that."*

### Core Principles

1. **Show, don't tell.** Every concept immediately demonstrated with a rendered SVG.
2. **Progressive revelation.** Start simple, layer complexity. Never dump everything at once.
3. **No dead SVGs.** Every generated image must look intentional and beautiful. No empty scenes, no entities outside bounds, no "here's a blank grid" steps.
4. **Diverse examples.** Vary shapes, colors, techniques. Never repeat the same pattern (e.g., "dots dots dots") across pages.
5. **The API Surface page is a destination.** Users can jump there at any time for a comprehensive overview of what's possible.
6. **MkDocs Material maximized.** Admonitions, tabbed code blocks, annotated code, grid cards, dark mode — all leveraged thoughtfully.

---

## Target Audience

Three user personas the wiki serves, in order of priority:

1. **The Curious Creative** — Has basic Python skills. Wants to make art. Will follow tutorials.
2. **The Experienced Developer** — Knows Python well. Wants the API surface, patterns, and architecture.
3. **The Contributor** — Wants to extend PyFreeform. Needs entity system internals and protocols.

Each page should serve persona 1 first (clear, visual, step-by-step), with deeper material accessible for personas 2 and 3 via admonitions, expandable sections, and dedicated reference pages.

---

## Information Architecture

### Navigation Structure (6 sections, down from 10)

```
Home
├── Getting Started (3 pages)
│   ├── Installation
│   ├── Your First Artwork
│   └── How PyFreeform Works
├── Guide (8 pages — the learning path)
│   ├── Scenes and Grids
│   ├── Working with Cells
│   ├── Drawing with Entities
│   ├── Colors, Styles & Palettes
│   ├── Paths and Parametric Positioning
│   ├── Shapes and Polygons
│   ├── Text and Typography
│   └── Transforms and Layout
├── Recipes (6 pages — project-based)
│   ├── Image-to-Art Portraits
│   ├── Geometric Patterns
│   ├── Flowing Curves & Waves
│   ├── Connected Networks
│   ├── Typographic Art
│   └── Advanced Compositions
├── API Surface (1 page — comprehensive reference)
│   └── Complete API Reference
├── Developer Guide (3 pages — for contributors)
│   ├── Architecture Overview
│   ├── Creating Custom Entities
│   └── The Pathable Protocol
└── Gallery (1 page)
    └── Showcase
```

**Total: 22 pages** (down from 81+ in the old wiki). Quality over quantity.

### Why This Structure

| Old Wiki Problem | New Wiki Solution |
|---|---|
| 10 sections, 81+ files — overwhelming navigation | 6 sections, 22 pages — focused navigation |
| Separate "Fundamentals" and "Entities" with overlap | Merged into "Guide" with natural flow |
| "Advanced Concepts" dumped many unrelated topics | Split: transforms go in Guide, pathable in Guide, architecture in Developer Guide |
| Repetitive entity pages (same pattern for each entity) | Single "Drawing with Entities" page that covers all entities with diverse examples |
| "Parametric Art" section felt academic | Folded into "Paths and Parametric Positioning" (Guide) and "Flowing Curves" (Recipes) |
| API reference spread across 8 pages | Single comprehensive "API Surface" page — the user's explicit request |
| Examples section disconnected from learning | "Recipes" are self-contained projects; "Gallery" is a showcase |

---

## Page-by-Page Design

### Home (`index.md`)

**Purpose**: Hook the user in 5 seconds. Show what's possible.

**Layout**:
1. **Hero section**: A single stunning SVG artwork (generated, not static) with the tagline: *"Turn images into art with Python."*
2. **3 code snippets**: Each 3-4 lines, each produces a different visual. Side-by-side with their SVG output.
3. **"Choose Your Path" cards**: Getting Started (beginner), Guide (learning), Recipes (building), API Surface (reference).
4. **Installation one-liner**: `pip install pyfreeform`

**No**: Long explanations. Feature lists. Version history.

---

### Getting Started

#### Page 1: Installation (`getting-started/01-installation.md`)

**Content**: `pip install pyfreeform`. Verify with a 3-line "hello world" that produces a visible result. System requirements (Python 3.10+, Pillow).

**SVG**: One small, satisfying artwork from the hello world.

#### Page 2: Your First Artwork (`getting-started/02-your-first-artwork.md`)

**Content**: The flagship tutorial. Two paths:

=== "From an Image"
    Load MonaLisa.jpg → create scene → iterate cells → add dots by brightness → save.
    Build up in 3 steps, each with a rendered SVG showing progress.

=== "From Scratch"
    `Scene.with_grid()` → iterate cells → add shapes based on position → save.
    Build up in 3 steps, each with a rendered SVG.

**Key teaching moments**: Scene, Grid, Cell, `cell.brightness`, `cell.color`, `add_dot()`, `save()`.

**SVG count**: 6 (3 per tab). Each must look good on its own — no empty grids.

#### Page 3: How PyFreeform Works (`getting-started/03-how-it-works.md`)

**Content**: Conceptual overview with a visual diagram.

> **Scene** → contains a **Grid** → divided into **Cells** → each cell holds image data and receives **Entities** (dots, lines, curves, shapes)

**Key concepts introduced** (with visual for each):
- The Surface protocol (cells and scenes share the same `add_*` methods)
- Named positions (`"center"`, `"top_left"`, etc.)
- z_index layering
- The `along`/`t` parametric system (teaser)

**SVG count**: 3-4 conceptual diagrams. Use annotated code blocks.

---

### Guide (The Learning Path)

Each Guide page follows this template:
1. **Opening visual**: A compelling SVG that uses the page's concepts.
2. **Core concept**: Explained in 2-3 paragraphs with annotated code.
3. **Building examples**: 2-3 progressive examples, each with rendered SVG.
4. **Variation showcase**: A comparison table or grid showing parameter variations.
5. **"Try This" callout**: A creative challenge with a hint.

#### Page 1: Scenes and Grids (`guide/01-scenes-and-grids.md`)

**Covers**:
- `Scene.from_image()` — full parameter exploration (grid_size, cell_size, cell_ratio)
- `Scene.with_grid()` — cols, rows, cell dimensions
- Grid properties (cols, rows, pixel dimensions)
- Grid selection methods: `grid.row()`, `grid.column()`, `grid.region()`, `grid.border()`
- Grid pattern selections: `grid.every()`, `grid.checkerboard()`, `grid.where()`, `grid.diagonal()`
- Cell merging: `grid.merge()`, `grid.merge_row()`, `grid.merge_col()`

**Visuals** (use both from_image and with_grid examples):
- Parameter comparison: same image at different grid_size values (20, 40, 60)
- Cell ratio comparison: square vs domino vs tall cells
- Grid selections visualized: border cells colored, checkerboard pattern, diagonal pattern
- Merged CellGroup with a title bar

**SVG count**: ~8-10

#### Page 2: Working with Cells (`guide/02-working-with-cells.md`)

**Covers**:
- Cell data properties: `brightness`, `color`, `rgb`, `alpha`
- Using brightness to drive visuals (radius, opacity, rotation, shape choice)
- Named positions within a cell
- Neighbor access: `cell.above`, `cell.right`, cross-cell comparisons
- Sub-cell sampling: `sample_image()`, `sample_brightness()`, `sample_hex()`
- `cell.normalized_position` for position-based effects
- `cell.distance_to()` for radial effects

**Visuals** (using MonaLisa.jpg and with_grid examples):
- Brightness-to-radius mapping (classic dot art)
- Brightness-to-color mapping (gradient effect)
- Edge detection using neighbor comparison
- Radial effect using distance_to
- Sub-cell sampling for higher-detail effects

**SVG count**: ~6-8

#### Page 3: Drawing with Entities (`guide/03-drawing-with-entities.md`)

**Covers**: All 8 entity types in ONE page, each demonstrated with a different creative use case (not just "here's a dot, here's a line").

**Structure**: Short section per entity, each showing what makes that entity special:

1. **Dots** — The fundamental mark. Example: size and opacity varying by brightness.
2. **Lines** — Structure and direction. Example: diagonal lines showing flow direction based on brightness gradient.
3. **Curves** — Organic flow. Example: curvature driven by brightness, creating a wave-like texture.
4. **Ellipses** — The Pathable shape. Example: rotation driven by brightness, creating a moiré pattern.
5. **Rectangles** — Filled regions. Example: rotation and opacity grid creating a mosaic.
6. **Polygons** — Shape variety. Example: different shapes per brightness band (triangles, hexagons, stars).
7. **Text** — Labels and typography. Example: letters from the image used as dot replacements.
8. **Paths** — Any shape imaginable. Example: spiral path rendered in each cell.

**SVG count**: 8 (one per entity type), all visually distinct and compelling.

#### Page 4: Colors, Styles & Palettes (`guide/04-colors-styles-palettes.md`)

**Covers**:
- Color formats (named, hex, RGB)
- The `fill=` vs `color=` distinction (with clear rule table)
- Opacity system: `opacity`, `fill_opacity`, `stroke_opacity`
- Style classes: DotStyle, LineStyle, ShapeStyle, TextStyle, etc.
- The `.with_*()` builder pattern
- Palettes: all 8 pre-built palettes visualized
- Custom palettes, `with_background()`, `inverted()`

**Visuals**:
- All 8 palettes applied to the same artwork (comparison grid)
- Opacity layering demo
- Style reuse example (define once, apply many)

**SVG count**: ~6-8

#### Page 5: Paths and Parametric Positioning (`guide/05-paths-and-parametric.md`)

**Covers** (this is the "aha" page):
- The `along`/`t` system: position any entity along any path
- Lines as paths: `cell.add_dot(along=line, t=cell.brightness)`
- Curves as paths: dots sliding along curves
- Ellipses as paths: dots orbiting around ellipses
- The Pathable protocol: `point_at(t)` explained visually
- Custom paths: `add_path(pathable)` for Wave, Spiral, etc.
- `align=True`: rotating entities to follow path tangent
- Sub-paths/arcs: `start_t`/`end_t` for partial paths
- TextPath: text warped along curves and ellipses

**Visuals**:
- Dot sliding along a line (brightness-driven position)
- Dots along a curve vs dots along an ellipse (comparison)
- Spiral path rendered with varying colors
- Text warped along a curve
- Multiple t-values visualized on a single path

**SVG count**: ~8-10

#### Page 6: Shapes and Polygons (`guide/06-shapes-and-polygons.md`)

**Covers**:
- Polygon shape classmethods: `triangle()`, `hexagon()`, `star()`, `squircle()`, etc.
- Using shapes in cells: `cell.add_polygon(Polygon.hexagon(), fill=cell.color)`
- Shape comparison gallery
- EntityGroup: composing custom reusable shapes
- Factory function pattern for EntityGroups
- `group.fit_to_cell()` and `entity.fit_within()`

**Visuals**:
- All 8 shape classmethods in a comparison grid
- Hexagonal grid using `add_polygon(Polygon.hexagon())`
- Star pattern with brightness-driven size
- EntityGroup "flower" pattern reused across cells
- fit_to_cell demonstration with rotation

**SVG count**: ~6-8

#### Page 7: Text and Typography (`guide/07-text-and-typography.md`)

**Covers**:
- Basic text placement: `add_text("A", color=cell.color)`
- Font families, bold/italic
- Text alignment: `text_anchor`, `baseline`
- Rotation and positioning
- `fit_within()` for fitting text inside shapes
- TextPath: text along curves, ellipses, custom paths
- Auto-sizing behavior
- `start_offset` / `end_offset` for partial path warping

**Visuals**:
- Character grid from image (each cell shows a letter sized by brightness)
- Text along curve comparison
- Bold vs italic vs monospace showcase
- Title overlaid on artwork using merged CellGroup

**SVG count**: ~5-7

#### Page 8: Transforms and Layout (`guide/08-transforms-and-layout.md`)

**Covers**:
- `entity.rotate()`, `entity.scale()`
- `entity.move_to()`, `entity.move_by()`, `entity.translate()`
- `entity.fit_to_cell(scale, recenter, at)` — the auto-fitting system
- `entity.fit_within(target)` — fit inside another entity
- `entity.place_beside(other, side, gap)` — relative positioning
- `entity.offset_from(anchor, dx, dy)` — anchor-based positioning
- Connections: `entity.connect()` with styles
- The anchor system: named anchors per entity type
- z_index layering: controlling draw order
- `map_range()` utility

**Visuals**:
- Rotation grid (shapes rotated by position)
- Scale comparison (same shape at different scales)
- fit_to_cell with different `at=` positions
- Connected network of entities
- Layered composition using z_index

**SVG count**: ~6-8

---

### Recipes (Project-Based)

Recipes are self-contained "build this" projects. Each produces a complete, impressive artwork.

**Template**: Goal → Setup → Build (3-5 steps) → Variations → Complete code.

#### Recipe 1: Image-to-Art Portraits (`recipes/01-image-to-art.md`)

Using MonaLisa.jpg and FrankMonster.png:
- Classic dot art (brightness → radius)
- Color dot art (preserve original colors)
- Halftone effect (brightness → size, dark background)
- Line art variant (diagonal lines, brightness → width)

**SVG count**: ~6 (technique comparisons using real images)

#### Recipe 2: Geometric Patterns (`recipes/02-geometric-patterns.md`)

Using `Scene.with_grid()`:
- Checkerboard with shape variations
- Rotating hexagonal tiling
- Brightness-wave pattern (sine function driving shape properties)
- Islamic-geometry-inspired pattern using stars and connections

**SVG count**: ~5

#### Recipe 3: Flowing Curves & Waves (`recipes/03-flowing-curves.md`)

- Curve field (curves connecting neighbors)
- Wave visualization using custom Pathable
- Spiral paths with varying density
- MCEscher-inspired flowing pattern using MCEscherBirds.jpg

**SVG count**: ~5

#### Recipe 4: Connected Networks (`recipes/04-connected-networks.md`)

- Connecting bright dots to their neighbors
- Distance-based connection filtering
- Arrow-cap directed graphs
- Network overlay on image

**SVG count**: ~4

#### Recipe 5: Typographic Art (`recipes/05-typographic-art.md`)

- ASCII art: character per cell based on brightness
- Text along paths: curved titles and labels
- TextPath on ellipses
- Combined: image art with text overlay

**SVG count**: ~4

#### Recipe 6: Advanced Compositions (`recipes/06-advanced-compositions.md`)

- Multi-layer artwork (z_index orchestration)
- EntityGroup reusable motifs
- CellGroup merged regions with different treatments
- Combined techniques: image + geometry + text + connections

**SVG count**: ~4

---

### API Surface (`api-surface/index.md`)

**This is the API_SURFACE.md document**, reformatted for the wiki with proper MkDocs Material features:
- Tabbed sections for quick navigation
- Collapsible details for verbose signatures
- Syntax-highlighted code examples
- Cross-links to relevant Guide pages

**Single comprehensive page** covering the entire API. The user explicitly requested this.

---

### Developer Guide

#### Page 1: Architecture Overview (`developer-guide/01-architecture.md`)

- Module structure diagram
- Surface protocol explained
- Entity class hierarchy
- SVG rendering pipeline (Scene.to_svg flow)

#### Page 2: Creating Custom Entities (`developer-guide/02-creating-entities.md`)

- Implementing the Entity abstract class
- Required methods: `anchor()`, `anchor_names`, `to_svg()`, `bounds()`
- Optional: `inner_bounds()`, `get_required_markers()`, `get_required_paths()`
- Example: creating a custom "Arrowhead" entity

#### Page 3: The Pathable Protocol (`developer-guide/03-pathable-protocol.md`)

- The protocol interface: `point_at(t)` + optional `arc_length()`, `angle_at(t)`, `to_svg_path_d()`
- Creating custom pathables (Wave, Spiral, Lissajous examples)
- How `add_path()` converts pathables to smooth SVG
- The cubic Bezier fitting algorithm explained

---

### Gallery (`gallery/index.md`)

A visual showcase grid of the best SVGs generated across all pages. Each links to its source page/recipe.

---

## SVG Generation System

### Design Principles

1. **One generator per page** (not per image). Each generator produces all SVGs for its page.
2. **Pathlib everywhere**. No `os.path`.
3. **Common utilities**: Shared helper module for colors, saving, and image loading.
4. **Explicit output paths**: Every SVG path is clearly derived from the page name.
5. **No internal attribute access**: Never use `cell._brightness` — always use `cell.brightness`.
6. **Validation**: Each generator validates its outputs exist and are non-empty.

### Directory Structure

```
wiki_v2/
├── index.md
├── mkdocs.yml            # (or symlink from project root)
├── sample_images/
│   ├── FrankMonster.png
│   ├── MonaLisa.jpg
│   └── MCEscherBirds.jpg
├── _generator/
│   ├── __init__.py       # Common utilities
│   ├── generate_all.py   # Master runner
│   ├── getting_started/
│   │   ├── gen_02_first_artwork.py
│   │   └── gen_03_how_it_works.py
│   ├── guide/
│   │   ├── gen_01_scenes_and_grids.py
│   │   ├── gen_02_working_with_cells.py
│   │   ├── gen_03_drawing_with_entities.py
│   │   ├── gen_04_colors_styles_palettes.py
│   │   ├── gen_05_paths_and_parametric.py
│   │   ├── gen_06_shapes_and_polygons.py
│   │   ├── gen_07_text_and_typography.py
│   │   └── gen_08_transforms_and_layout.py
│   ├── recipes/
│   │   ├── gen_01_image_to_art.py
│   │   ├── gen_02_geometric_patterns.py
│   │   ├── gen_03_flowing_curves.py
│   │   ├── gen_04_connected_networks.py
│   │   ├── gen_05_typographic_art.py
│   │   └── gen_06_advanced_compositions.py
│   └── home/
│       └── gen_index.py
├── _images/              # All generated SVGs go here
│   ├── home/
│   ├── getting-started/
│   ├── guide/
│   ├── recipes/
│   └── gallery/
├── getting-started/
│   ├── 01-installation.md
│   ├── 02-your-first-artwork.md
│   └── 03-how-it-works.md
├── guide/
│   ├── 01-scenes-and-grids.md
│   ├── 02-working-with-cells.md
│   ├── 03-drawing-with-entities.md
│   ├── 04-colors-styles-palettes.md
│   ├── 05-paths-and-parametric.md
│   ├── 06-shapes-and-polygons.md
│   ├── 07-text-and-typography.md
│   └── 08-transforms-and-layout.md
├── recipes/
│   ├── 01-image-to-art.md
│   ├── 02-geometric-patterns.md
│   ├── 03-flowing-curves.md
│   ├── 04-connected-networks.md
│   ├── 05-typographic-art.md
│   └── 06-advanced-compositions.md
├── api-surface/
│   └── index.md
├── developer-guide/
│   ├── 01-architecture.md
│   ├── 02-creating-entities.md
│   └── 03-pathable-protocol.md
└── gallery/
    └── index.md
```

### Generator Common Utilities (`_generator/__init__.py`)

```python
"""Common utilities for wiki SVG generators."""
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent
IMAGES_DIR = WIKI_ROOT / "_images"
SAMPLE_IMAGES = WIKI_ROOT / "sample_images"

def save(scene, path: str) -> Path:
    """Save scene to _images/ directory. Returns the output path."""
    output = IMAGES_DIR / path
    output.parent.mkdir(parents=True, exist_ok=True)
    scene.save(str(output))
    assert output.exists(), f"Failed to generate: {output}"
    assert output.stat().st_size > 100, f"Suspiciously small file: {output}"
    return output

def sample_image(name: str) -> Path:
    """Get path to a sample image."""
    path = SAMPLE_IMAGES / name
    assert path.exists(), f"Sample image not found: {path}"
    return path
```

### Generator Runner (`_generator/generate_all.py`)

```python
"""Regenerate all SVGs for wiki_v2."""
import importlib
import sys
from pathlib import Path

GENERATORS_DIR = Path(__file__).parent

def discover_generators():
    """Find all gen_*.py files."""
    return sorted(GENERATORS_DIR.rglob("gen_*.py"))

def run_all():
    """Run all generators, report results."""
    generators = discover_generators()
    print(f"Found {len(generators)} generators")

    passed, failed = 0, 0
    for gen_path in generators:
        module_path = gen_path.relative_to(GENERATORS_DIR.parent)
        module_name = str(module_path).replace("/", ".").replace("\\", ".").removesuffix(".py")

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "generate"):
                module.generate()
            passed += 1
            print(f"  OK  {gen_path.name}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {gen_path.name}: {e}")

    print(f"\n{passed} passed, {failed} failed out of {len(generators)}")
    return failed == 0

if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
```

### Example Generator (`_generator/guide/gen_01_scenes_and_grids.py`)

```python
"""Generate SVGs for Guide: Scenes and Grids."""
from pyfreeform import Scene, Palette
from _generator import save, sample_image

def generate():
    # --- Grid size comparison ---
    for grid_size in [20, 40, 60]:
        scene = Scene.from_image(
            sample_image("MonaLisa.jpg"),
            grid_size=grid_size,
        )
        for cell in scene.grid:
            cell.add_dot(
                radius=cell.brightness * scene.grid.cell_width * 0.45,
                color=cell.color,
            )
        save(scene, f"guide/scenes-grid-size-{grid_size}.svg")

    # --- Cell ratio comparison ---
    for ratio, label in [(1.0, "square"), (2.0, "domino"), (0.5, "tall")]:
        scene = Scene.from_image(
            sample_image("MonaLisa.jpg"),
            grid_size=30,
            cell_ratio=ratio,
        )
        for cell in scene.grid:
            cell.add_fill(color=cell.color)
        save(scene, f"guide/scenes-ratio-{label}.svg")

    # --- Border selection ---
    scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
    palette = Palette.midnight()
    for cell in scene.grid:
        cell.add_fill(color=palette.background)
    for cell in scene.grid.border(thickness=2):
        cell.add_fill(color=palette.accent)
    save(scene, "guide/scenes-border-selection.svg")

    # ... more examples
```

---

## MkDocs Material Features Used

### Theme Configuration

```yaml
theme:
  name: material
  palette:
    - scheme: default
      primary: deep purple
      accent: amber
      toggle: { icon: material/brightness-7, name: Switch to dark mode }
    - scheme: slate
      primary: deep purple
      accent: amber
      toggle: { icon: material/brightness-4, name: Switch to light mode }
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs        # Top-level sections as tabs
    - navigation.sections    # Expand sections in sidebar
    - navigation.top         # Back to top button
    - navigation.indexes     # Section index pages
    - search.suggest
    - search.highlight
    - content.code.copy      # Copy buttons on code blocks
    - content.code.annotate  # Code annotations
    - content.tabs.link      # Linked tabs (same tab selection across page)
    - toc.follow
```

### Markdown Features Used Per Page

| Feature | Usage |
|---|---|
| **Admonitions** | `!!! tip`, `!!! info`, `!!! warning` for callouts |
| **Expandable details** | `??? note "Advanced"` for deep dives |
| **Tabbed code** | `=== "From Image"` / `=== "From Scratch"` |
| **Annotated code** | `# (1)!` with annotation below |
| **Image comparison** | Side-by-side SVGs in grid layout |
| **Tables** | Parameter comparisons, style references |
| **Grid cards** | Home page "choose your path" |
| **Glightbox** | Click to zoom on SVGs |

### Image Embedding Pattern

```markdown
<figure markdown>
  ![Dot art from MonaLisa](_images/guide/dot-art-mona-lisa.svg){ width="400" }
  <figcaption>Brightness-driven dot sizes reveal the portrait</figcaption>
</figure>
```

For side-by-side comparison:
```markdown
<div class="grid" markdown>

![Grid size 20](_images/guide/scenes-grid-size-20.svg){ width="280" }

![Grid size 40](_images/guide/scenes-grid-size-40.svg){ width="280" }

![Grid size 60](_images/guide/scenes-grid-size-60.svg){ width="280" }

</div>
```

---

## Sample Image Strategy

### Provided Images

| Image | Use | Why |
|---|---|---|
| **MonaLisa.jpg** | Primary tutorial image | Iconic, high contrast, universally recognized |
| **FrankMonster.png** | Secondary tutorial image | Fun, colorful, different aesthetic from Mona Lisa |
| **MCEscherBirds.jpg** | Advanced examples | Detailed, pattern-rich, good for flowing curves and edge detection |

### Usage Rules

- **MonaLisa**: Getting Started tutorial, Recipes: Image-to-Art, Guide: Working with Cells
- **FrankMonster**: Guide: Drawing with Entities, Recipes: Image-to-Art (alternate)
- **MCEscher**: Recipes: Flowing Curves, Guide: Paths (advanced examples)
- Each image used in **at most 3 pages** to avoid repetition
- Most Guide pages use **`Scene.with_grid()`** (no image) for clarity and focus

### Custom Sample Images (To Create)

We should create 2-3 additional simple images specifically designed to showcase `from_image()` well:

1. **gradient.png** — A smooth color gradient (great for demonstrating brightness-driven effects clearly)
2. **circles.png** — Simple geometric circles on a dark background (demonstrates edge detection, high-contrast effects)

These can be generated programmatically with Pillow and placed in `sample_images/`.

---

## Build Order

The implementation should proceed in this order:

### Phase 1: Foundation
1. Set up directory structure
2. Create `_generator/__init__.py` with utilities
3. Create `_generator/generate_all.py` runner
4. Create custom sample images (gradient.png, circles.png)
5. Create `mkdocs_v2.yml` configuration

### Phase 2: Core Pages
6. Home page (`index.md`) with hero SVG generator
7. Getting Started: Installation
8. Getting Started: Your First Artwork (with generator)
9. Getting Started: How PyFreeform Works (with generator)

### Phase 3: Guide
10. Guide pages 1-8, each with its generator
    - Build in order, as later pages reference earlier concepts

### Phase 4: Recipes
11. Recipes 1-6, each with its generator
    - Can be built in any order

### Phase 5: Reference & Meta
12. API Surface page (adapt API_SURFACE.md)
13. Developer Guide pages
14. Gallery page (collects best SVGs from all generators)

### Phase 6: Polish
15. Cross-link all pages
16. Run full regeneration, verify all SVGs
17. Dark mode testing
18. Final navigation refinement

---

## Quality Checklist (per page)

- [ ] Every SVG renders correctly and looks intentional
- [ ] No empty/blank SVGs (every image shows meaningful content)
- [ ] No entities rendering outside scene bounds
- [ ] Code examples are complete and correct (can be copy-pasted)
- [ ] Examples are diverse (no two examples on the same page produce similar-looking output)
- [ ] MkDocs features used appropriately (not overloaded)
- [ ] Cross-links to related pages where relevant
- [ ] Tested in both light and dark mode
- [ ] Each page can stand alone (no required reading order, though recommended)
- [ ] Progressive: simple → complex within each page

---

## Estimated SVG Count

| Section | Pages | SVGs per Page | Total SVGs |
|---|---|---|---|
| Home | 1 | 4 | 4 |
| Getting Started | 3 | 4 | 12 |
| Guide | 8 | 7 | 56 |
| Recipes | 6 | 5 | 30 |
| API Surface | 1 | 0 | 0 |
| Developer Guide | 3 | 2 | 6 |
| Gallery | 1 | 12 | 12 |
| **Total** | **23** | — | **~120** |

Down from 224+ SVGs in the old wiki, but each one is intentional and beautiful.
