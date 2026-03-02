from __future__ import annotations

from typing import TypeAlias

from .relcoord import NAMED_POSITIONS, NamedPosition, RelCoord

AnchorSpec: TypeAlias = str | RelCoord | tuple[float, float]

__all__ = ["NAMED_POSITIONS", "AnchorSpec", "NamedPosition"]
