"""Configuration classes for PyFreeform."""

from .caps import register_cap
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
    "ConnectionStyle",
    "DotStyle",
    "FillStyle",
    "LineStyle",
    "Palette",
    "ShapeStyle",
    "TextStyle",
    "register_cap",
]
