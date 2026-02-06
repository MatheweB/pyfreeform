
# Implementing Custom Pathable Paths

Create paths that work with `along=`.

## The Protocol

```python
@runtime_checkable
class Pathable(Protocol):
    def point_at(self, t: float) -> Point:
        """Get point at parameter t (0 to 1)."""
        ...
```

![Built-in pathable entities: line, curve, and ellipse with positioned dots](./_images/04-pathable-protocol/04-builtin-pathables.svg)

![Detailed view of the point_at method: how parameter t maps to positions along a path](./_images/04-pathable-protocol/05-point-at-method-detail.svg)

## Example: Wave Path

```python
from pyfreeform.core.point import Point
import math

class Wave:
    def __init__(self, start, end, amplitude, frequency):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency
    
    def point_at(self, t: float) -> Point:
        # Linear base
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t
        
        # Add wave
        wave = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        y = base_y + wave
        
        return Point(x, y)
```

![Wave path visualization with start and end points](./_images/04-pathable-protocol/01-wave-path-visual.svg)

![Wave parameters: amplitude and frequency variations](./_images/04-pathable-protocol/02-wave-parameters.svg)

## Usage

```python
wave = Wave(
    start=cell.top_left,
    end=cell.bottom_right,
    amplitude=10,
    frequency=3
)

# Works with along=!
cell.add_dot(along=wave, t=0.5, radius=3)
```

![Elements positioned along a wave path using along= parameter](./_images/04-pathable-protocol/03-using-wave-with-along.svg)

![Custom path variations: wave, spiral, and zigzag implementations](./_images/04-pathable-protocol/06-custom-path-variations.svg)

![Practical usage example: combining custom paths with grid iteration and styling](./_images/04-pathable-protocol/07-practical-usage-example.svg)

## See Also
- [Custom Paths](../parametric-art/05-custom-paths.md)
- [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)
