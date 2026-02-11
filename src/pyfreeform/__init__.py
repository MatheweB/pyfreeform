"""
PyFreeform - A minimalist, art-focused Python drawing library.
"""

__version__ = "0.3.0"

# Core
from .core.coord import Coord, CoordLike, RelCoord, RelCoordLike
from .core.entity import Entity
from .core.connection import Connection
from .core.pathable import FullPathable, Pathable
from .core.tangent import get_angle_at

# Entities
from .entities.dot import Dot
from .entities.line import Line
from .entities.rect import Rect
from .entities.curve import Curve
from .entities.path import Path
from .entities.ellipse import Ellipse
from .entities.text import Text
from .entities.polygon import Polygon
from .entities.entity_group import EntityGroup
from .entities.point import Point

# Core (Surface protocol)
from .core.surface import Surface

# Grid
from .grid.grid import Grid
from .grid.cell import Cell
from .grid.cell_group import CellGroup

# Scene
from .scene.scene import Scene

# Image
from .image.image import Image
from .image.layer import Layer

# Configuration
from .config.caps import register_cap
from .config.palette import Palette
from .config.styles import (
    DotStyle, LineStyle, FillStyle, BorderStyle,
    ShapeStyle, TextStyle, ConnectionStyle,
)

# Utilities
from .color import Color
from .display import display



# =============================================================================
# Utility Functions
# =============================================================================

def map_range(
    value: float,
    in_min: float = 0,
    in_max: float = 1,
    out_min: float = 0,
    out_max: float = 1,
    clamp: bool = False,
) -> float:
    """
    Convert a value from one range to another.

    Think of it like converting between units. If brightness goes from
    0 to 1 but you want a radius between 2 and 10, this does the
    conversion for you:

        radius = map_range(brightness, 0, 1, 2, 10)
        # brightness 0.0 → radius 2
        # brightness 0.5 → radius 6
        # brightness 1.0 → radius 10

    Swap the output range to reverse the direction:

        radius = map_range(brightness, 0, 1, 10, 2)
        # brightness 0.0 → radius 10  (dark = big)
        # brightness 1.0 → radius 2   (bright = small)

    Args:
        value: The input value to convert.
        in_min: Start of the input range (default: 0).
        in_max: End of the input range (default: 1).
        out_min: Start of the output range (default: 0).
        out_max: End of the output range (default: 1).
        clamp: If True, keep the result within the output range.
    """
    # Avoid division by zero
    if in_max == in_min:
        return out_min
    
    # Linear interpolation
    t = (value - in_min) / (in_max - in_min)
    result = out_min + t * (out_max - out_min)
    
    if clamp:
        if out_min <= out_max:
            result = max(out_min, min(out_max, result))
        else:
            result = max(out_max, min(out_min, result))
    
    return result


__all__ = [
    # Version
    "__version__",
    # Core
    "Coord",
    "CoordLike",
    "RelCoord",
    "RelCoordLike",
    "Entity",
    "Connection",
    "Pathable",
    "FullPathable",
    "get_angle_at",
    # Entities
    "Dot",
    "Line",
    "Rect",
    "Curve",
    "Path",
    "Ellipse",
    "Text",
    "Polygon",
    "EntityGroup",
    "Point",
    # Core (Surface protocol)
    "Surface",
    # Grid
    "Grid",
    "Cell",
    "CellGroup",
    # Scene
    "Scene",
    # Image
    "Image",
    "Layer",
    # Configuration
    "register_cap",
    "Palette",
    "DotStyle",
    "LineStyle",
    "FillStyle",
    "BorderStyle",
    "ShapeStyle",
    "TextStyle",
    "ConnectionStyle",
    # Utilities
    "Color",
    "display",
    "map_range",
]
