"""Cap type registry — extensible marker-based line caps."""

from __future__ import annotations

from typing import Callable

# Registry: cap_name → function(marker_id, color, size) → SVG marker string
_MARKER_CAPS: dict[str, Callable[[str, str, float], str]] = {}

DEFAULT_ARROW_SCALE = 3.0


def register_cap(name: str, generator: Callable[[str, str, float], str]) -> None:
    """
    Register a new marker-based cap type.

    The generator function receives (marker_id, color_hex, size) and must
    return a complete SVG ``<marker>`` element string.

    Example::

        def _diamond_marker(marker_id, color, size):
            return (
                f'<marker id="{marker_id}" viewBox="0 0 10 10" '
                f'refX="5" refY="5" markerWidth="{size}" markerHeight="{size}" '
                f'orient="auto-start-reverse">'
                f'<polygon points="5,0 10,5 5,10 0,5" fill="{color}" />'
                f'</marker>'
            )

        register_cap("diamond", _diamond_marker)
    """
    _MARKER_CAPS[name] = generator


def is_marker_cap(name: str) -> bool:
    """Check if a cap name requires an SVG marker (vs native stroke-linecap)."""
    return name in _MARKER_CAPS


def make_marker_id(cap_name: str, color: str, size: float) -> str:
    """Generate a deterministic marker ID from cap type, color, and size."""
    clean = color.lstrip("#").lower()
    size_str = f"{size:.1f}".replace(".", "_")
    return f"cap-{cap_name}-{clean}-{size_str}"


def get_marker(cap_name: str, color: str, size: float) -> tuple[str, str] | None:
    """
    Get marker ID and SVG for a cap type.

    Returns:
        (marker_id, marker_svg) if the cap needs a marker, else None.
    """
    if not is_marker_cap(cap_name):
        return None
    mid = make_marker_id(cap_name, color, size)
    svg = _MARKER_CAPS[cap_name](mid, color, size)
    return (mid, svg)


# ---------------------------------------------------------------------------
# Built-in marker cap: arrow
# ---------------------------------------------------------------------------

def _arrow_marker(marker_id: str, color: str, size: float) -> str:
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" '
        f'refX="10" refY="5" '
        f'markerWidth="{size}" markerHeight="{size}" '
        f'orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}" />'
        f'</marker>'
    )


register_cap("arrow", _arrow_marker)
