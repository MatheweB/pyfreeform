"""Built-in cap shapes -- add new caps here.

Each shape is an SVG path drawn in a 10x10 grid.  The ``tip`` says
where the shape attaches to the stroke endpoint.

::

    Shape        Path                              Tip
    ----------   --------------------------------  -------
    FORWARD  ->  M 0 0  L 10 5  L 0 10  z          (10, 5)
    REVERSE  <-  M 10 0 L 0 5   L 10 10 z          (0, 5)
"""

from __future__ import annotations

from .caps import cap_shape, register_cap

# Arrow path data
_FORWARD = "M 0 0 L 10 5 L 0 10 z"
_REVERSE = "M 10 0 L 0 5 L 10 10 z"


def register_all() -> None:
    """Register all built-in cap shapes."""

    # "arrow" -- outward-facing (default): tip points away from the path.
    register_cap(
        "arrow",
        cap_shape(_FORWARD, tip=(10, 5)),
        start_generator=cap_shape(_REVERSE, tip=(0, 5)),
    )

    # "arrow_in" -- inward-facing: tip points into the path.
    register_cap(
        "arrow_in",
        cap_shape(_REVERSE, tip=(10, 5)),
        start_generator=cap_shape(_FORWARD, tip=(0, 5)),
    )
