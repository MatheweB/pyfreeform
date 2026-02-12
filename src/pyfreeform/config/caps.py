"""Cap type registry — extensible marker-based line caps."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Callable


class _CapEntry(NamedTuple):
    generator: Callable[[str, str, float], str]
    start_generator: Callable[[str, str, float], str] | None = None


# Registry: cap_name → (_CapEntry)
_MARKER_CAPS: dict[str, _CapEntry] = {}

DEFAULT_ARROW_SCALE = 3.0


def register_cap(
    name: str,
    generator: Callable[[str, str, float], str],
    *,
    start_generator: Callable[[str, str, float], str] | None = None,
) -> None:
    """
    Register a new marker-based cap type.

    The generator function receives (marker_id, color_hex, size) and must
    return a complete SVG ``<marker>`` element string.

    Markers should use ``refX``/``refY`` so the tip of the cap aligns
    with the path endpoint.  The cap's body extends backward over the
    stroke, hiding it — no stroke shortening is needed.

    Args:
        name: Cap name (e.g. "arrow", "diamond").
        generator:  Function producing the SVG ``<marker>`` element
                    (used for ``marker-end``).
        start_generator:    Optional separate generator for ``marker-start``.
                            If provided, the start marker uses an explicitly
                            reversed shape instead of relying on SVG2
                            ``orient="auto-start-reverse"``.

    Example::

        def _diamond_marker(marker_id, color, size):
            return (
                f'<marker id="{marker_id}" viewBox="0 0 10 10" '
                f'refX="5" refY="5" markerWidth="{size}" markerHeight="{size}" '
                f'orient="auto" overflow="visible">'
                f'<polygon points="5,0 10,5 5,10 0,5" fill="{color}" />'
                f'</marker>'
            )

        register_cap("diamond", _diamond_marker)
    """
    _MARKER_CAPS[name] = _CapEntry(generator, start_generator)


def is_marker_cap(name: str) -> bool:
    """Check if a cap name requires an SVG marker (vs native stroke-linecap)."""
    return name in _MARKER_CAPS


def make_marker_id(cap_name: str, color: str, size: float, *, for_start: bool = False) -> str:
    """Generate a deterministic marker ID from cap type, color, and size."""
    clean = color.lstrip("#").lower()
    size_str = f"{size:.1f}".replace(".", "_")
    suffix = "-start" if for_start else ""
    return f"cap-{cap_name}-{clean}-{size_str}{suffix}"


def get_marker(
    cap_name: str, color: str, size: float, *, for_start: bool = False
) -> tuple[str, str] | None:
    """
    Get marker ID and SVG for a cap type.

    Args:
        cap_name: Registered cap name.
        color: Stroke color.
        size: Marker size (typically stroke_width * scale).
        for_start: If True and a ``start_generator`` is registered,
                    use it to produce an explicitly reversed marker.

    Returns:
        (marker_id, marker_svg) if the cap needs a marker, else None.
    """
    entry = _MARKER_CAPS.get(cap_name)
    if entry is None:
        return None
    mid = make_marker_id(cap_name, color, size, for_start=for_start)
    gen = entry.start_generator if for_start and entry.start_generator else entry.generator
    svg = gen(mid, color, size)
    return (mid, svg)


# ---------------------------------------------------------------------------
# Built-in marker caps: arrow, arrow_in
# ---------------------------------------------------------------------------
#
# Arrow shapes:
#   FORWARD  = "M 0 0 L 10 5 L 0 10 z"   (points right → outward)
#   REVERSE  = "M 10 0 L 0 5 L 10 10 z"   (points left  → inward)
#
# Positioning rule — refX must always align the marker's reference point
# with the path endpoint it's attached to:
#   marker-end   → refX="10"  (right edge = path endpoint)
#   marker-start → refX="0"   (left edge  = path endpoint)
#
# This means each (shape x position) combination needs its own generator:
#
#   cap        position     shape      refX
#   ─────────  ──────────   ─────────  ────
#   arrow      end          FORWARD    10
#   arrow      start        REVERSE     0
#   arrow_in   end          REVERSE    10
#   arrow_in   start        FORWARD     0

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


# "arrow" — outward-facing (default): tip points away from the path.
register_cap(
    "arrow",
    _make_arrow_gen(_FORWARD, ref_x=10),  # end: → at endpoint
    start_generator=_make_arrow_gen(_REVERSE, ref_x=0),  # start: ← at startpoint
)

# "arrow_in" — inward-facing: tip points into the path.
register_cap(
    "arrow_in",
    _make_arrow_gen(_REVERSE, ref_x=10),  # end: ← at endpoint
    start_generator=_make_arrow_gen(_FORWARD, ref_x=0),  # start: → at startpoint
)
