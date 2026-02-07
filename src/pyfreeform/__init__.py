"""
PyFreeform - A minimalist, art-focused Python drawing library.
"""

__version__ = "0.3.0"

# Core
from .core.point import Point
from .core.entity import Entity
from .core.connection import Connection
from .core.pathable import Pathable
from .core.tangent import get_angle_at

# Entities
from .entities.dot import Dot
from .entities.line import Line
from .entities.rect import Rect
from .entities.curve import Curve
from .entities.path import Path
from .entities.ellipse import Ellipse
from .entities.text import Text
from .entities.polygon import (
    Polygon,
    triangle,
    square,
    diamond,
    hexagon,
    star,
    regular_polygon,
    squircle,
    rounded_rect,
)
from .entities.entity_group import EntityGroup

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

# Shape helpers module (for `from pyfreeform import shapes`)
from .entities import polygon as shapes


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
    Map a value from one range to another.
    
    This is a convenience function for creative coding - it's equivalent to
    simple math but reads more clearly in code.
    
    Args:
        value: The input value to map.
        in_min: Input range minimum (default: 0).
        in_max: Input range maximum (default: 1).
        out_min: Output range minimum (default: 0).
        out_max: Output range maximum (default: 1).
        clamp: If True, clamp result to output range.
    
    Returns:
        The mapped value.
    
    Examples:
        >>> # Map brightness (0-1) to rotation (0-360)
        >>> rotation = map_range(cell.brightness, 0, 1, 0, 360)
        
        >>> # Map brightness to radius (small when dark, large when bright)
        >>> radius = map_range(cell.brightness, 0, 1, 2, 10)
        
        >>> # Inverse mapping (bright = small)
        >>> radius = map_range(cell.brightness, 0, 1, 10, 2)
    
    Note:
        You can also just use Python math directly:
        >>> rotation = cell.brightness * 360
        >>> radius = 2 + cell.brightness * 8
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
    "Point",
    "Entity",
    "Connection",
    "Pathable",
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
    # Shape helpers (also available via `shapes.hexagon()`)
    "triangle",
    "square",
    "diamond",
    "hexagon",
    "star",
    "regular_polygon",
    "squircle",
    "rounded_rect",
    "shapes",
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
