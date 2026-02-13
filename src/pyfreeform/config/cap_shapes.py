"""Built-in marker cap shapes.

Add new cap shapes here by calling ``register_cap()``.  Each cap needs
a generator function that receives ``(marker_id, color_hex, size)`` and
returns a complete SVG ``<marker>`` element string.

Arrow shapes
------------

::

    FORWARD  = "M 0 0 L 10 5 L 0 10 z"   (points right -> outward)
    REVERSE  = "M 10 0 L 0 5 L 10 10 z"   (points left  -> inward)

Positioning rule -- refX must always align the marker's reference point
with the path endpoint it's attached to::

    marker-end   -> refX="10"  (right edge = path endpoint)
    marker-start -> refX="0"   (left edge  = path endpoint)

This means each (shape x position) combination needs its own generator::

    cap        position     shape      refX
    ---------  ----------   ---------  ----
    arrow      end          FORWARD    10
    arrow      start        REVERSE     0
    arrow_in   end          REVERSE    10
    arrow_in   start        FORWARD     0
"""

from __future__ import annotations

from .caps import register_cap

_FORWARD = "M 0 0 L 10 5 L 0 10 z"
_REVERSE = "M 10 0 L 0 5 L 10 10 z"


def _make_arrow_gen(path_d: str, ref_x: int):
    """Create an arrow marker generator with the given shape and refX."""

    def _gen(marker_id: str, color: str, size: float) -> str:
        return (
            f'<marker id="{marker_id}" viewBox="0 0 10 10" '
            f'refX="{ref_x}" refY="5" '
            f'markerWidth="{size}" markerHeight="{size}" '
            f'orient="auto" overflow="visible">'
            f'<path d="{path_d}" fill="{color}" />'
            f"</marker>"
        )

    return _gen


def register_all() -> None:
    """Register all built-in cap shapes."""

    # "arrow" -- outward-facing (default): tip points away from the path.
    register_cap(
        "arrow",
        _make_arrow_gen(_FORWARD, ref_x=10),  # end: -> at endpoint
        start_generator=_make_arrow_gen(_REVERSE, ref_x=0),  # start: <- at startpoint
    )

    # "arrow_in" -- inward-facing: tip points into the path.
    register_cap(
        "arrow_in",
        _make_arrow_gen(_REVERSE, ref_x=10),  # end: <- at endpoint
        start_generator=_make_arrow_gen(_FORWARD, ref_x=0),  # start: -> at startpoint
    )
