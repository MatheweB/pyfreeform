"""Configuration classes for PyFreeform."""

from .caps import register_cap
from .palette import Palette
from .styles import (
    DotStyle, LineStyle, FillStyle, BorderStyle,
    ShapeStyle, TextStyle, ConnectionStyle,
)

__all__ = [
    "Palette",
    "DotStyle",
    "LineStyle",
    "FillStyle",
    "BorderStyle",
    "ShapeStyle",
    "TextStyle",
    "ConnectionStyle",
    "register_cap",
]
