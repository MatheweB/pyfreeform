
# Scene API Reference

Complete API documentation for the Scene class.

## Class: Scene

Main container for all drawable objects.

### Constructor

```python
Scene(width: int, height: int, background: str | None = None)
```

![Constructor Example](./_images/scene/example1-constructor.svg)

### Factory Methods

```python
@classmethod
Scene.from_image(source, grid_size=40, cell_size=10, background=None)

@classmethod
Scene.with_grid(cols, rows, cell_size, background=None)
```

![Scene from Image](./_images/scene/example2-from-image.svg)

![Scene with Grid](./_images/scene/example3-with-grid.svg)

### Properties

- `width: int` - Scene width in pixels
- `height: int` - Scene height in pixels
- `background: str | None` - Background color
- `grid: Grid | None` - Primary grid
- `entities: list[Entity]` - All entities
- `connections: list[Connection]` - All connections

![Scene Properties](./_images/scene/example4-properties.svg)

### Methods

#### add()

```python
def add(self, *objects: Entity | Connection | Grid) -> Entity | Connection | Grid
```

Add entities, connections, or grids to the scene. Can add multiple objects at once.

**Parameters**:
- `*objects`: One or more Entity, Connection, or Grid objects

**Returns**: The last added object (for method chaining)

**Example**:
```python
from pyfreeform import Scene, Dot, Line, Connection

scene = Scene(400, 400)

# Add single entity
dot1 = Dot(100, 100, radius=10, color="red")
scene.add(dot1)

# Add multiple entities at once
dot2 = Dot(300, 300, radius=10, color="blue")
line = Line(100, 100, 300, 300, color="gray")
scene.add(dot2, line)

# Add connection
conn = Connection(start=dot1, end=dot2)
scene.add(conn)

# Method chaining
scene.add(Dot(200, 200, radius=5))
```

![Add Connection Example](./_images/scene/example6-add-connection.svg)

#### remove()

```python
def remove(self, obj: Entity | Connection | Grid) -> bool
```

Remove an object from the scene.

**Parameters**:
- `obj`: The entity, connection, or grid to remove

**Returns**: True if object was found and removed, False otherwise

**Example**:
```python
dot = Dot(100, 100, radius=10)
scene.add(dot)

# Later, remove it
was_removed = scene.remove(dot)
```

#### clear()

```python
def clear(self) -> None
```

Remove all objects from the scene (entities, connections, and grids).

**Example**:
```python
scene.clear()  # Empty scene
```

#### save()

```python
def save(self, path: str) -> None
```

Save the scene as an SVG file.

**Parameters**:
- `path`: File path (e.g., "artwork.svg")

**Example**:
```python
scene.save("my_art.svg")
```

#### to_svg()

```python
def to_svg(self) -> str
```

Generate SVG markup as a string (without saving to file).

**Returns**: Complete SVG document as string

**Example**:
```python
svg_content = scene.to_svg()
print(svg_content)  # View raw SVG
```

#### Iteration Support

Scenes support standard Python iteration and length:

```python
# Iterate over all entities
for entity in scene:
    print(entity)

# Count entities
num_entities = len(scene)
```

![Add Entity Example](./_images/scene/example5-add-entity.svg)

![Complete Scene](./_images/scene/example7-complete.svg)

## See Also
- [Scenes Guide](../fundamentals/01-scenes.md)
- [Grid API](grid.md)
