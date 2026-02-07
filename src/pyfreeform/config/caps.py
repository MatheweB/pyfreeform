"""Cap type registry — extensible marker-based line caps."""

from __future__ import annotations

from typing import Callable, NamedTuple


class _CapEntry(NamedTuple):
    generator: Callable[[str, str, float], str]
    inset: float  # fraction of marker width to shorten the stroke (0.0–1.0)


# Registry: cap_name → (_CapEntry)
_MARKER_CAPS: dict[str, _CapEntry] = {}

DEFAULT_ARROW_SCALE = 3.0


def register_cap(
    name: str,
    generator: Callable[[str, str, float], str],
    *,
    inset: float = 1.0,
) -> None:
    """
    Register a new marker-based cap type.

    The generator function receives (marker_id, color_hex, size) and must
    return a complete SVG ``<marker>`` element string.

    Args:
        name: Cap name (e.g. "arrow", "diamond").
        generator: Function producing the SVG ``<marker>`` element.
        inset: Fraction of marker width by which the stroke is shortened
               so it ends at the marker's base rather than poking through
               the tip.  1.0 = full marker width (arrow), 0.5 = half
               (centered shapes like diamond), 0.0 = no shortening.

    Example::

        def _diamond_marker(marker_id, color, size):
            return (
                f'<marker id="{marker_id}" viewBox="0 0 10 10" '
                f'refX="5" refY="5" markerWidth="{size}" markerHeight="{size}" '
                f'orient="auto-start-reverse" overflow="visible">'
                f'<polygon points="5,0 10,5 5,10 0,5" fill="{color}" />'
                f'</marker>'
            )

        register_cap("diamond", _diamond_marker, inset=0.5)
    """
    _MARKER_CAPS[name] = _CapEntry(generator, inset)


def is_marker_cap(name: str) -> bool:
    """Check if a cap name requires an SVG marker (vs native stroke-linecap)."""
    return name in _MARKER_CAPS


def get_cap_inset(name: str) -> float:
    """Return the inset fraction for a marker cap (0.0 if not a marker cap)."""
    entry = _MARKER_CAPS.get(name)
    return entry.inset if entry is not None else 0.0


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
    entry = _MARKER_CAPS.get(cap_name)
    if entry is None:
        return None
    mid = make_marker_id(cap_name, color, size)
    svg = entry.generator(mid, color, size)
    return (mid, svg)


# ---------------------------------------------------------------------------
# Built-in marker cap: arrow
# ---------------------------------------------------------------------------

def _arrow_marker(marker_id: str, color: str, size: float) -> str:
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" '
        f'refX="0" refY="5" '
        f'markerWidth="{size}" markerHeight="{size}" '
        f'orient="auto-start-reverse" overflow="visible">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}" />'
        f'</marker>'
    )


register_cap("arrow", _arrow_marker, inset=1.0)
