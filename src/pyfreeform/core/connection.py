"""Connection - A link between two entities that auto-updates."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from .coord import Coord, CoordLike
from .stroked_path_mixin import StrokedPathMixin

if TYPE_CHECKING:
    from .entity import Entity


class Connection(StrokedPathMixin):
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
        Coord(100, 100)
        >>> dot1.move_to(150, 150)
        >>> conn.start_point  # Updated automatically
        Coord(150, 150)
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
    def start_point(self) -> Coord:
        """Current position of the start anchor (always up-to-date)."""
        return self._start.anchor(self._start_anchor)
    
    @property
    def end_point(self) -> Coord:
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
    def start_cap(self) -> str | None:
        """Override cap for the start end, or None."""
        return self._style.get("start_cap")

    @property
    def end_cap(self) -> str | None:
        """Override cap for the end end, or None."""
        return self._style.get("end_cap")

    @property
    def opacity(self) -> float:
        """Opacity (0.0 transparent to 1.0 opaque)."""
        return self._style.get("opacity", 1.0)

    @opacity.setter
    def opacity(self, value: float) -> None:
        self._style["opacity"] = value

    def point_at(self, t: float) -> Coord:
        """
        Get a point along the connection.
        
        Args:
            t: Parameter from 0 (start) to 1 (end).
        
        Returns:
            Coord at that position along the connection.
        """
        return self.start_point.lerp(self.end_point, t)

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t.

        For a linear connection, the angle is constant.

        Args:
            t: Parameter (unused — angle is constant for connections).

        Returns:
            Angle in degrees.
        """
        import math

        p1 = self.start_point
        p2 = self.end_point
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for this connection."""
        p1, p2 = self.start_point, self.end_point
        return f"M {p1.x} {p1.y} L {p2.x} {p2.y}"

    def disconnect(self) -> None:
        """Remove this connection from both entities."""
        self._start.remove_connection(self)
        self._end.remove_connection(self)

    def to_svg(self) -> str:
        """Render connection as SVG line element."""
        p1 = self.start_point
        p2 = self.end_point
        svg_cap, marker_attrs = self._svg_cap_and_marker_attrs()

        parts = [
            f'<line x1="{p1.x}" y1="{p1.y}" '
            f'x2="{p2.x}" y2="{p2.y}" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="{svg_cap}"'
        ]

        if marker_attrs:
            parts.append(marker_attrs)

        if self.opacity < 1.0:
            parts.append(f' opacity="{self.opacity}"')

        parts.append(" />")
        return "".join(parts)
    
    def __repr__(self) -> str:
        return (
            f"Connection({self._start!r} -> {self._end!r}, "
            f"style={self._style})"
        )
