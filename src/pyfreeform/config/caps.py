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


def collect_markers(
    cap: str,
    start_cap: str | None,
    end_cap: str | None,
    width: float,
    color: str,
) -> list[tuple[str, str]]:
    """Collect SVG marker definitions needed for the given cap configuration.

    Returns:
        List of (marker_id, marker_svg) tuples.
    """
    effective_sc = start_cap if start_cap is not None else cap
    effective_ec = end_cap if end_cap is not None else cap
    markers: list[tuple[str, str]] = []
    size = width * DEFAULT_ARROW_SCALE
    for cap_name, for_start in ((effective_sc, True), (effective_ec, False)):
        result = get_marker(cap_name, color, size, for_start=for_start)
        if result is not None:
            markers.append(result)
    return markers


def svg_cap_and_marker_attrs(
    cap: str,
    start_cap: str | None,
    end_cap: str | None,
    width: float,
    color: str,
) -> tuple[str, str]:
    """Compute SVG stroke-linecap value and marker attribute string.

    Returns:
        (svg_cap, marker_attrs_str) where svg_cap is "butt", "round",
        or "square", and marker_attrs_str contains any marker-start/
        marker-end attributes (or empty string).
    """
    effective_sc = start_cap if start_cap is not None else cap
    effective_ec = end_cap if end_cap is not None else cap
    has_marker_start = is_marker_cap(effective_sc)
    has_marker_end = is_marker_cap(effective_ec)

    svg_cap = cap

    parts: list[str] = []
    size = width * DEFAULT_ARROW_SCALE
    if has_marker_start:
        mid = make_marker_id(effective_sc, color, size, for_start=True)
        parts.append(f' marker-start="url(#{mid})"')
    if has_marker_end:
        mid = make_marker_id(effective_ec, color, size, for_start=False)
        parts.append(f' marker-end="url(#{mid})"')

    # When any marker cap is present, use "butt" linecap so the stroke
    # ends flush at the endpoint — prevents round/square caps from
    # poking out past the arrow tip.
    if has_marker_start or has_marker_end:
        svg_cap = "butt"

    return svg_cap, "".join(parts)
