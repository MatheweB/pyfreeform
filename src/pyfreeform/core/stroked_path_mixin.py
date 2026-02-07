"""Mixin for entities with stroked paths and marker-based caps."""

from __future__ import annotations


class StrokedPathMixin:
    """
    Mixin providing cap/marker handling for stroked path entities.

    Consolidates the cap resolution and SVG marker logic shared by
    Line, Curve, Path, and Connection.
    """

    # Attributes provided by the host class.
    cap: str
    start_cap: str | None
    end_cap: str | None
    width: float
    color: str

    @property
    def effective_start_cap(self) -> str:
        """Resolved cap for the start end."""
        return self.start_cap if self.start_cap is not None else self.cap

    @property
    def effective_end_cap(self) -> str:
        """Resolved cap for the end end."""
        return self.end_cap if self.end_cap is not None else self.cap

    def get_required_markers(self) -> list[tuple[str, str]]:
        """
        Collect SVG marker definitions needed by this entity's caps.

        Returns:
            List of (marker_id, marker_svg) tuples.
        """
        from ..config.caps import DEFAULT_ARROW_SCALE, get_marker

        markers: list[tuple[str, str]] = []
        size = self.width * DEFAULT_ARROW_SCALE
        for cap_name in (self.effective_start_cap, self.effective_end_cap):
            result = get_marker(cap_name, self.color, size)
            if result is not None:
                markers.append(result)
        return markers

    def _svg_cap_and_marker_attrs(self) -> tuple[str, str]:
        """
        Compute the SVG stroke-linecap value and marker attribute string.

        Returns:
            (svg_cap, marker_attrs_str) where svg_cap is "butt", "round",
            or "square", and marker_attrs_str contains any marker-start/
            marker-end attributes (or empty string).
        """
        from ..config.caps import (
            DEFAULT_ARROW_SCALE,
            is_marker_cap,
            make_marker_id,
        )

        sc = self.effective_start_cap
        ec = self.effective_end_cap
        has_marker_start = is_marker_cap(sc)
        has_marker_end = is_marker_cap(ec)

        svg_cap = "butt" if (has_marker_start or has_marker_end) else self.cap

        parts: list[str] = []
        size = self.width * DEFAULT_ARROW_SCALE
        if has_marker_start:
            mid = make_marker_id(sc, self.color, size)
            parts.append(f' marker-start="url(#{mid})"')
        if has_marker_end:
            mid = make_marker_id(ec, self.color, size)
            parts.append(f' marker-end="url(#{mid})"')

        return svg_cap, "".join(parts)

    def _marker_shortening(self) -> tuple[float, float]:
        """
        How much to shorten each end of the stroke for marker caps.

        The stroke is shortened so it ends at the marker's base, preventing
        the line from poking through the narrow tip.  Each marker cap
        declares its own *inset* fraction (1.0 for arrow, 0.5 for diamond,
        etc.) so this works for any registered cap type.

        Returns:
            (start_shorten, end_shorten) in user-space units.
        """
        from ..config.caps import DEFAULT_ARROW_SCALE, get_cap_inset

        marker_size = self.width * DEFAULT_ARROW_SCALE
        sc = self.effective_start_cap
        ec = self.effective_end_cap
        return (
            marker_size * get_cap_inset(sc),
            marker_size * get_cap_inset(ec),
        )
