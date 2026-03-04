"""Gradient paint servers for SVG fill and stroke."""

from __future__ import annotations

import hashlib
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from .color import Color, ColorLike


@dataclass(frozen=True, slots=True)
class GradientStop:
    """A single color stop in a gradient.

    Attributes:
        color: Hex color string (already normalized).
        offset: Position along the gradient (0.0 to 1.0).
        opacity: Stop opacity (0.0 to 1.0, default 1.0).
    """

    color: str
    offset: float
    opacity: float = 1.0

    def to_svg(self) -> str:
        """Render as an SVG ``<stop>`` element."""
        parts = [f'<stop offset="{self.offset}" stop-color="{self.color}"']
        if self.opacity < 1.0:
            parts.append(f' stop-opacity="{self.opacity}"')
        parts.append(" />")
        return "".join(parts)


# ---------------------------------------------------------------------------
# Stop input parsing
# ---------------------------------------------------------------------------

# A single stop can be:
#   "red"                       -> color only, offset auto-distributed
#   ("red", 0.5)                -> color + explicit offset
#   ("red", 0.5, 0.8)          -> color + offset + opacity
_StopInput = Union[
    ColorLike,
    "tuple[ColorLike, float]",
    "tuple[ColorLike, float, float]",
]


def _parse_stops(raw: tuple[_StopInput, ...]) -> tuple[GradientStop, ...]:
    """Normalize flexible stop inputs into a tuple of ``GradientStop``."""
    if len(raw) < 2:
        raise ValueError("Gradients require at least 2 color stops")

    parsed: list[tuple[str, float | None, float]] = []
    for item in raw:
        if isinstance(item, str):
            # Plain color string
            parsed.append((Color(item).to_hex(), None, 1.0))
        elif isinstance(item, tuple):
            if len(item) == 3 and isinstance(item[0], int) and not isinstance(item[0], bool):
                # RGB tuple like (255, 0, 0) — treat as color
                parsed.append((Color(item).to_hex(), None, 1.0))  # type: ignore[arg-type]
            elif len(item) == 2:
                color_val, offset = item
                parsed.append((Color(color_val).to_hex(), float(offset), 1.0))  # type: ignore[arg-type]
            elif len(item) == 3:
                color_val, offset, opacity = item
                parsed.append((Color(color_val).to_hex(), float(offset), float(opacity)))  # type: ignore[arg-type]
            else:
                raise ValueError(f"Invalid stop format: {item!r}")
        else:
            raise ValueError(f"Invalid stop format: {item!r}")

    # Auto-distribute offsets for entries that have None
    n = len(parsed)
    stops: list[GradientStop] = []
    for i, (color, offset, opacity) in enumerate(parsed):
        if offset is None:
            offset = i / (n - 1) if n > 1 else 0.0
        stops.append(GradientStop(color=color, offset=offset, opacity=opacity))

    return tuple(stops)


# ---------------------------------------------------------------------------
# Gradient base
# ---------------------------------------------------------------------------


class Gradient(ABC):
    """Base class for SVG gradient paint servers.

    Gradients can be used anywhere a color is accepted (``fill=``,
    ``stroke=``, ``color=``).  They are emitted as ``<defs>`` entries
    and referenced via ``fill="url(#id)"``.
    """

    def __init__(
        self,
        *stops: _StopInput,
        spread_method: str = "pad",
        gradient_units: str = "objectBoundingBox",
    ) -> None:
        if spread_method not in ("pad", "reflect", "repeat"):
            raise ValueError(
                f"spread_method must be 'pad', 'reflect', or 'repeat', got {spread_method!r}"
            )
        if gradient_units not in ("objectBoundingBox", "userSpaceOnUse"):
            raise ValueError(
                f"gradient_units must be 'objectBoundingBox' or "
                f"'userSpaceOnUse', got {gradient_units!r}"
            )
        self._stops = _parse_stops(stops)
        self._spread_method = spread_method
        self._gradient_units = gradient_units
        self._id = self._compute_id()

    # -- public API ----------------------------------------------------------

    @property
    def gradient_id(self) -> str:
        """Deterministic SVG id for this gradient."""
        return self._id

    @property
    def stops(self) -> tuple[GradientStop, ...]:
        """The normalized color stops."""
        return self._stops

    def to_svg_ref(self) -> str:
        """Return the SVG paint reference string, e.g. ``url(#grad-abc)``."""
        return f"url(#{self._id})"

    @abstractmethod
    def to_svg_def(self) -> str:
        """Render the full ``<linearGradient>`` or ``<radialGradient>`` element."""

    # -- internals -----------------------------------------------------------

    def _stops_svg(self) -> str:
        """Render all ``<stop>`` child elements."""
        return "".join(s.to_svg() for s in self._stops)

    def _spread_attr(self) -> str:
        """Render ``spreadMethod`` attribute (omitted when default 'pad')."""
        if self._spread_method != "pad":
            return f' spreadMethod="{self._spread_method}"'
        return ""

    def _units_attr(self) -> str:
        """Render ``gradientUnits`` attribute (omitted when default)."""
        if self._gradient_units != "objectBoundingBox":
            return f' gradientUnits="{self._gradient_units}"'
        return ""

    @abstractmethod
    def _id_seed(self) -> str:
        """Return a canonical string for deterministic hashing."""

    def _compute_id(self) -> str:
        seed = self._id_seed()
        digest = hashlib.md5(seed.encode(), usedforsecurity=False).hexdigest()
        return f"grad-{digest[:12]}"

    def __repr__(self) -> str:
        colors = ", ".join(s.color for s in self._stops)
        return f"{type(self).__name__}({colors})"


# ---------------------------------------------------------------------------
# LinearGradient
# ---------------------------------------------------------------------------


class LinearGradient(Gradient):
    """A linear gradient that transitions colors along a line.

    Example::

        # Simple left-to-right
        LinearGradient("red", "blue")

        # 45-degree angle
        LinearGradient("red", "blue", angle=45)

        # Explicit coordinates
        LinearGradient("red", "blue", x1=0, y1=0, x2=1, y2=1)

        # With explicit stop offsets
        LinearGradient(("red", 0.0), ("gold", 0.3), ("blue", 1.0))
    """

    def __init__(
        self,
        *stops: _StopInput,
        angle: float = 0,
        x1: float | None = None,
        y1: float | None = None,
        x2: float | None = None,
        y2: float | None = None,
        spread_method: str = "pad",
        gradient_units: str = "objectBoundingBox",
    ) -> None:
        """Create a linear gradient.

        Args:
            *stops: Color stops — see module docstring for accepted formats.
            angle: Direction in degrees (0 = right, 90 = down). Ignored
                when explicit coordinates are given.
            x1: Start point x (fraction 0-1 for objectBoundingBox).
            y1: Start point y.
            x2: End point x.
            y2: End point y.
            spread_method: 'pad', 'reflect', or 'repeat'.
            gradient_units: 'objectBoundingBox' or 'userSpaceOnUse'.
        """
        coords = (x1, y1, x2, y2)
        if any(c is not None for c in coords):
            if any(c is None for c in coords):
                raise ValueError("Provide all of x1, y1, x2, y2 or none of them")
            self._x1 = float(x1)  # type: ignore[arg-type]
            self._y1 = float(y1)  # type: ignore[arg-type]
            self._x2 = float(x2)  # type: ignore[arg-type]
            self._y2 = float(y2)  # type: ignore[arg-type]
        else:
            # Convert angle to coordinates.
            # 0° = left-to-right, 90° = top-to-bottom (SVG convention).
            rad = math.radians(angle)
            self._x1 = round(0.5 - 0.5 * math.cos(rad), 6)
            self._y1 = round(0.5 - 0.5 * math.sin(rad), 6)
            self._x2 = round(0.5 + 0.5 * math.cos(rad), 6)
            self._y2 = round(0.5 + 0.5 * math.sin(rad), 6)
        self._angle = float(angle)
        super().__init__(
            *stops,
            spread_method=spread_method,
            gradient_units=gradient_units,
        )

    def to_svg_def(self) -> str:
        return (
            f'<linearGradient id="{self._id}"'
            f' x1="{self._x1}" y1="{self._y1}"'
            f' x2="{self._x2}" y2="{self._y2}"'
            f"{self._spread_attr()}"
            f"{self._units_attr()}"
            f">{self._stops_svg()}</linearGradient>"
        )

    def _id_seed(self) -> str:
        stops = "|".join(f"{s.color}@{s.offset}:{s.opacity}" for s in self._stops)
        return (
            f"linear:{self._x1},{self._y1},{self._x2},{self._y2}"
            f"|{self._spread_method}|{self._gradient_units}|{stops}"
        )


# ---------------------------------------------------------------------------
# RadialGradient
# ---------------------------------------------------------------------------


class RadialGradient(Gradient):
    """A radial gradient that radiates colors from a center point.

    Example::

        # Simple center-out
        RadialGradient("white", "black")

        # Off-center focal point
        RadialGradient("white", "black", fx=0.3, fy=0.3)

        # Custom center and radius
        RadialGradient("red", "blue", cx=0.2, cy=0.2, r=0.8)
    """

    def __init__(
        self,
        *stops: _StopInput,
        cx: float = 0.5,
        cy: float = 0.5,
        r: float = 0.5,
        fx: float | None = None,
        fy: float | None = None,
        fr: float = 0,
        spread_method: str = "pad",
        gradient_units: str = "objectBoundingBox",
    ) -> None:
        """Create a radial gradient.

        Args:
            *stops: Color stops — see module docstring for accepted formats.
            cx: Center x of the end circle (fraction 0-1).
            cy: Center y of the end circle.
            r: Radius of the end circle.
            fx: Focal point x (center of start circle). Defaults to cx.
            fy: Focal point y. Defaults to cy.
            fr: Radius of the start circle (default 0).
            spread_method: 'pad', 'reflect', or 'repeat'.
            gradient_units: 'objectBoundingBox' or 'userSpaceOnUse'.
        """
        self._cx = float(cx)
        self._cy = float(cy)
        self._r = float(r)
        self._fx = float(fx) if fx is not None else None
        self._fy = float(fy) if fy is not None else None
        self._fr = float(fr)
        super().__init__(
            *stops,
            spread_method=spread_method,
            gradient_units=gradient_units,
        )

    def to_svg_def(self) -> str:
        parts = [
            f'<radialGradient id="{self._id}"',
            f' cx="{self._cx}" cy="{self._cy}" r="{self._r}"',
        ]
        if self._fx is not None:
            parts.append(f' fx="{self._fx}"')
        if self._fy is not None:
            parts.append(f' fy="{self._fy}"')
        if self._fr != 0:
            parts.append(f' fr="{self._fr}"')
        parts.append(self._spread_attr())
        parts.append(self._units_attr())
        parts.append(f">{self._stops_svg()}</radialGradient>")
        return "".join(parts)

    def _id_seed(self) -> str:
        stops = "|".join(f"{s.color}@{s.offset}:{s.opacity}" for s in self._stops)
        return (
            f"radial:{self._cx},{self._cy},{self._r}"
            f",{self._fx},{self._fy},{self._fr}"
            f"|{self._spread_method}|{self._gradient_units}|{stops}"
        )


# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------

PaintLike = ColorLike | Gradient
"""Type alias for paint values: named color, hex string, RGB tuple, or Gradient."""
