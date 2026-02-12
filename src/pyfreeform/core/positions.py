from __future__ import annotations


from typing import Literal, TypeAlias, Final, Union

from .relcoord import RelCoord

# Named positions within a surface (relative coordinates)
# Defined as a literal type
NamedPosition: TypeAlias = Literal[
    "center",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "top",
    "bottom",
    "left",
    "right",
]

NAMED_POSITIONS: Final[dict[NamedPosition, RelCoord]] = {
    "center": RelCoord(0.5, 0.5),
    "top_left": RelCoord(0.0, 0.0),
    "top_right": RelCoord(1.0, 0.0),
    "bottom_left": RelCoord(0.0, 1.0),
    "bottom_right": RelCoord(1.0, 1.0),
    "top": RelCoord(0.5, 0.0),
    "bottom": RelCoord(0.5, 1.0),
    "left": RelCoord(0.0, 0.5),
    "right": RelCoord(1.0, 0.5),
}

# Define the Position type to include both named positions and coordinate tuples
Position = Union["RelCoord", tuple[float, float], NamedPosition]
