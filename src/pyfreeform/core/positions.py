from __future__ import annotations

from typing import Final, TypeAlias

from .relcoord import NamedPosition, RelCoord

AnchorSpec: TypeAlias = str | RelCoord | tuple[float, float]

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
