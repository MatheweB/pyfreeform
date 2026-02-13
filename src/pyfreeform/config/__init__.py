"""Configuration classes for PyFreeform."""

from .caps import CapName, cap_shape, register_cap
from .palette import Palette
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
    "CapName",
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
