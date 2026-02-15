"""Configuration classes for PyFreeform."""

from .caps import CapName, cap_shape, register_cap
from .palette import Palette
from .styles import (
    BorderStyle,
    FillStyle,
    PathStyle,
    ShapeStyle,
    TextStyle,
)

__all__ = [
    "BorderStyle",
    "CapName",
    "FillStyle",
    "Palette",
    "PathStyle",
    "ShapeStyle",
    "TextStyle",
    "cap_shape",
    "register_cap",
]
