"""Built-in cap shapes -- add new caps here.

Each shape is a list of ``(x, y)`` vertices in a 10x10 grid.
The ``tip`` says where the shape attaches to the stroke endpoint.

To add a new cap, define vertices and add an entry to ``CAPS``.
The cap engine registers everything automatically.

::

    Shape              Vertices                          Tip
    ---------------    --------------------------------  -------
    FORWARD_ARROW  ->  (0,0) (10,5) (0,10)              (10, 5)
    REVERSE_ARROW  <-  (10,0) (0,5) (10,10)             (0, 5)
    DIAMOND            (5,0) (10,5) (5,10) (0,5)        (5, 5)
"""

from __future__ import annotations

# ── Arrow ────────────────────────────────────────────────────────────
FORWARD_ARROW = [(0, 0), (10, 5), (0, 10)]
REVERSE_ARROW = [(10, 0), (0, 5), (10, 10)]

# ── Diamond ──────────────────────────────────────────────────────────
DIAMOND = [(5, 0), (10, 5), (5, 10), (0, 5)]

# ── Registration table ───────────────────────────────────────────────
# name → {vertices, tip, [start_vertices, start_tip]}
# Directional caps need separate start/end shapes (like arrows).
# Symmetric caps (like diamond) only need vertices + tip.

CAPS: dict[str, dict[str, object]] = {
    "arrow": {
        "vertices": FORWARD_ARROW,
        "tip": (10, 5),
        "start_vertices": REVERSE_ARROW,
        "start_tip": (0, 5),
    },
    "arrow_in": {
        "vertices": REVERSE_ARROW,
        "tip": (10, 5),
        "start_vertices": FORWARD_ARROW,
        "start_tip": (0, 5),
    },
    "diamond": {
        "vertices": DIAMOND,
        "tip": (5, 5),
    },
}
