"""
PyFreeform - A minimalist, art-focused Python drawing library.
"""

__version__ = "0.5.0"

# Core
# Utilities
from .color import Color, ColorLike

# Configuration
from .config.caps import CapName, cap_shape, register_cap
from .config.palette import Palette
from .config.styles import (
    BorderStyle,
    FillStyle,
    PathStyle,
    ShapeStyle,
    TextStyle,
)
from .core.connection import Connectable, Connection
from .core.coord import Coord, CoordLike
from .core.positions import AnchorSpec
from .core.relcoord import RelCoord, RelCoordLike
from .core.entity import Entity
from .core.pathable import Pathable

# Core (Surface protocol)
from .core.surface import Surface
from .core.tangent import get_angle_at
from .display import display
from .entities.curve import Curve

# Entities
from .entities.dot import Dot
from .entities.ellipse import Ellipse
from .entities.entity_group import EntityGroup
from .entities.line import Line
from .entities.path import Path
from .entities.point import Point
from .entities.polygon import Polygon
from .entities.rect import Rect
from .entities.text import Text
from .grid.cell import Cell
from .grid.cell_group import CellGroup

# Grid
from .grid.grid import Grid

# Image
from .image.image import Image
from .image.layer import Layer

# Layout
from .layout import align, between, distribute, stack

# Scene
from .scene.scene import Scene

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
    "AnchorSpec",
    "BorderStyle",
    "CapName",
    "Cell",
    "CellGroup",
    "Color",
    "ColorLike",
    "Connectable",
    "Connection",
    "Coord",
    "CoordLike",
    "Curve",
    "Dot",
    "Ellipse",
    "Entity",
    "EntityGroup",
    "FillStyle",
    "Grid",
    "Image",
    "Layer",
    "Line",
    "Palette",
    "Path",
    "PathStyle",
    "Pathable",
    "Point",
    "Polygon",
    "Rect",
    "RelCoord",
    "RelCoordLike",
    "Scene",
    "ShapeStyle",
    "Surface",
    "Text",
    "TextStyle",
    "__version__",
    "align",
    "between",
    "cap_shape",
    "display",
    "distribute",
    "get_angle_at",
    "map_range",
    "register_cap",
    "stack",
]
