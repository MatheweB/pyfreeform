"""Configuration classes for PyFreeform."""

from .caps import cap_shape, register_cap
from .cap_shapes import register_all as _register_cap_shapes
from .palette import Palette

_register_cap_shapes()
from .styles import (
    BorderStyle,
    ConnectionStyle,
    DotStyle,
    FillStyle,
    LineStyle,
    ShapeStyle,
    TextStyle,
)

__all__ = [
    "BorderStyle",
    "ConnectionStyle",
    "DotStyle",
    "FillStyle",
    "LineStyle",
    "Palette",
    "ShapeStyle",
    "TextStyle",
    "cap_shape",
    "register_cap",
]
