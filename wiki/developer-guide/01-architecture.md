
# Architecture Overview

Understanding PyFreeform's internal structure.

## Package Structure

```
pyfreeform/
├── core/
│   ├── point.py          # Immutable 2D coordinate
│   ├── entity.py         # Base entity class
│   ├── connection.py     # Dynamic links
│   └── pathable.py       # Protocol for parametric paths
├── entities/
│   ├── dot.py
│   ├── line.py
│   ├── curve.py          # Bézier implementation
│   ├── ellipse.py        # Parametric ellipse
│   ├── polygon.py        # + shape helpers
│   ├── text.py
│   └── rect.py
├── grid/
│   ├── grid.py           # 2D cell array
│   └── cell.py           # Builder methods
├── scene/
│   └── scene.py          # Main container
├── config/
│   ├── palette.py        # Color schemes
│   └── styles.py         # Style dataclasses
└── image.py              # Image/Layer processing
```

## Key Design Patterns

### Entity-Component Pattern
- Entity base class with common behavior
- Specific entities inherit and add features

![Entity-Component pattern visualization using actual entities](./_images/01-architecture/01-entity-component-pattern.svg)

### Builder Pattern
- Cell methods return entities
- Method chaining for configuration

![Builder pattern visualization showing method chaining progression](./_images/01-architecture/02-builder-pattern.svg)

### Protocol-Based Design
- Pathable protocol for extensibility
- Runtime type checking

![Protocol-based design showing pathable entities with along= positioning](./_images/01-architecture/03-protocol-pattern.svg)

### Immutable Point
- NamedTuple for safety
- Vector operations

![Immutable Point pattern showing safe coordinate sharing](./_images/01-architecture/04-immutable-point.svg)

### Architecture Layering
- Core, entities, grid, scene, config layers
- Clear dependency direction

![Architecture layering showing dependency hierarchy between modules](./_images/01-architecture/05-architecture-layering.svg)

### Component Composition
- Entities composed from core building blocks
- Flexible combinations

![Component composition showing how entities are assembled from core parts](./_images/01-architecture/06-component-composition.svg)

## See Also
- [Entity System](02-entity-system.md)
- [Creating Entities](03-creating-entities.md)
