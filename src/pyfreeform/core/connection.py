"""Connection - A link between two entities that auto-updates."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .point import Point

if TYPE_CHECKING:
    from .entity import Entity


class Connection:
    """
    A connection between two entities.
    
    Connections link entities together. Unlike static lines, connections
    automatically update when their endpoints move. They're the key to
    maintaining relationships in PyFreeform.
    
    Attributes:
        start: The starting entity
        end: The ending entity
        start_anchor: Name of anchor on start entity
        end_anchor: Name of anchor on end entity
        style: Visual style properties (width, color, etc.)
    
    Examples:
        >>> dot1 = Dot(100, 100)
        >>> dot2 = Dot(200, 200)
        >>> conn = dot1.connect(dot2, style={"width": 2, "color": "red"})
        >>> conn.start_point  # Always current position
        Point(100, 100)
        >>> dot1.move_to(150, 150)
        >>> conn.start_point  # Updated automatically
        Point(150, 150)
    """
    
    DEFAULT_STYLE = {
        "width": 1,
        "color": "black",
        "z_index": 0,
        "cap": "round",
    }
    
    def __init__(
        self,
        start: Entity,
        end: Entity,
        start_anchor: str = "center",
        end_anchor: str = "center",
        style: Any = None,
    ) -> None:
        """
        Create a connection between two entities.

        Args:
            start: The starting entity.
            end: The ending entity.
            start_anchor: Anchor name on start entity.
            end_anchor: Anchor name on end entity.
            style: ConnectionStyle object or dict with "width", "color",
                   "z_index" keys.
        """
        from ..config.styles import ConnectionStyle

        self._start = start
        self._end = end
        self._start_anchor = start_anchor
        self._end_anchor = end_anchor
        if isinstance(style, ConnectionStyle):
            self._style = {**self.DEFAULT_STYLE, **style.to_dict()}
        else:
            self._style = {**self.DEFAULT_STYLE, **(style or {})}
        
        # Register with both entities
        start.add_connection(self)
        end.add_connection(self)
    
    @property
    def start(self) -> Entity:
        """The starting entity."""
        return self._start
    
    @property
    def end(self) -> Entity:
        """The ending entity."""
        return self._end
    
    @property
    def start_anchor(self) -> str:
        """Name of anchor on start entity."""
        return self._start_anchor
    
    @property
    def end_anchor(self) -> str:
        """Name of anchor on end entity."""
        return self._end_anchor
    
    @property
    def start_point(self) -> Point:
        """Current position of the start anchor (always up-to-date)."""
        return self._start.anchor(self._start_anchor)
    
    @property
    def end_point(self) -> Point:
        """Current position of the end anchor (always up-to-date)."""
        return self._end.anchor(self._end_anchor)
    
    @property
    def style(self) -> dict[str, Any]:
        """Visual style properties."""
        return self._style
    
    @property
    def width(self) -> float:
        """Line width."""
        return self._style.get("width", 1)
    
    @width.setter
    def width(self, value: float) -> None:
        self._style["width"] = value
    
    @property
    def color(self) -> str:
        """Line color."""
        return self._style.get("color", "black")
    
    @color.setter
    def color(self, value: str) -> None:
        self._style["color"] = value
    
    @property
    def z_index(self) -> int:
        """Layer ordering (higher values render on top)."""
        return self._style.get("z_index", 0)
    
    @z_index.setter
    def z_index(self, value: int) -> None:
        self._style["z_index"] = value

    @property
    def cap(self) -> str:
        """Cap style for both ends."""
        return self._style.get("cap", "round")

    @property
    def effective_start_cap(self) -> str:
        """Resolved cap for the start end."""
        return self._style.get("start_cap") or self.cap

    @property
    def effective_end_cap(self) -> str:
        """Resolved cap for the end end."""
        return self._style.get("end_cap") or self.cap

    def point_at(self, t: float) -> Point:
        """
        Get a point along the connection.
        
        Args:
            t: Parameter from 0 (start) to 1 (end).
        
        Returns:
            Point at that position along the connection.
        """
        return self.start_point.lerp(self.end_point, t)
    
    def disconnect(self) -> None:
        """Remove this connection from both entities."""
        self._start.remove_connection(self)
        self._end.remove_connection(self)

    def get_required_markers(self) -> list[tuple[str, str]]:
        """
        Collect SVG marker definitions needed by this connection's caps.

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

    def to_svg(self) -> str:
        """Render connection as SVG line element."""
        from ..config.caps import DEFAULT_ARROW_SCALE, is_marker_cap, make_marker_id

        p1 = self.start_point
        p2 = self.end_point
        sc = self.effective_start_cap
        ec = self.effective_end_cap
        has_marker_start = is_marker_cap(sc)
        has_marker_end = is_marker_cap(ec)

        svg_cap = "butt" if (has_marker_start or has_marker_end) else self.cap

        parts = [
            f'<line x1="{p1.x}" y1="{p1.y}" '
            f'x2="{p2.x}" y2="{p2.y}" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="{svg_cap}"'
        ]

        size = self.width * DEFAULT_ARROW_SCALE
        if has_marker_start:
            mid = make_marker_id(sc, self.color, size)
            parts.append(f' marker-start="url(#{mid})"')
        if has_marker_end:
            mid = make_marker_id(ec, self.color, size)
            parts.append(f' marker-end="url(#{mid})"')

        parts.append(" />")
        return "".join(parts)
    
    def __repr__(self) -> str:
        return (
            f"Connection({self._start!r} -> {self._end!r}, "
            f"style={self._style})"
        )
