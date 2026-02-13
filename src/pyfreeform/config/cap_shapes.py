"""Built-in cap shapes -- add new caps here.

Each shape is a list of ``(x, y)`` vertices in a 10x10 grid.
The ``tip`` says where the shape attaches to the stroke endpoint.

::

    Shape              Vertices                          Tip
    ---------------    --------------------------------  -------
    FORWARD_ARROW  ->  (0,0) (10,5) (0,10)              (10, 5)
    REVERSE_ARROW  <-  (10,0) (0,5) (10,10)             (0, 5)
    DIAMOND            (5,0) (10,5) (5,10) (0,5)        (5, 5)
"""

from __future__ import annotations

from .caps import cap_shape, register_cap

# ── Arrow ────────────────────────────────────────────────────────────
_FORWARD_ARROW = [(0, 0), (10, 5), (0, 10)]
_REVERSE_ARROW = [(10, 0), (0, 5), (10, 10)]

# ── Diamond ──────────────────────────────────────────────────────────
_DIAMOND = [(5, 0), (10, 5), (5, 10), (0, 5)]


def register_all() -> None:
    """Register all built-in cap shapes."""

    # "arrow" -- outward-facing (default): tip points away from the path.
    register_cap(
        "arrow",
        cap_shape(_FORWARD_ARROW, tip=(10, 5)),
        start_generator=cap_shape(_REVERSE_ARROW, tip=(0, 5)),
    )

    # "arrow_in" -- inward-facing: tip points into the path.
    register_cap(
        "arrow_in",
        cap_shape(_REVERSE_ARROW, tip=(10, 5)),
        start_generator=cap_shape(_FORWARD_ARROW, tip=(0, 5)),
    )

    # "diamond" -- symmetric, same in both directions.
    register_cap("diamond", cap_shape(_DIAMOND, tip=(5, 5)))
