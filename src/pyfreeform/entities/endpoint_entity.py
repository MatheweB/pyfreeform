"""EndpointEntity - Base class for entities with start/end points and per-end caps."""

from __future__ import annotations

from abc import abstractmethod

from ..animation import typed_methods
from ..color import Color, apply_brightness
from ..config.caps import CapName, collect_markers, resolve_cap
from ..core.coord import Coord
from ..core.entity import Entity
from ..core.relcoord import RelCoord
from ..gradient import Gradient


class EndpointEntity(Entity):
    """Base class for entities with start/end points and per-end caps.

    Shared by Line and Curve. Provides:
    - color property with Color wrapping
    - relative_start / relative_end properties
    - rotation_center (midpoint of start → end)
    - effective_start_cap / effective_end_cap resolution
    - get_required_markers() for SVG marker collection
    - adjust_relative_end() helper for move_by implementations
    """

    # -- typed animation methods (factory-generated) --
    animate_color = typed_methods.animate_color
    animate_width = typed_methods.animate_width

    def __init__(
        self,
        x: float,
        y: float,
        z_index: int = 0,
        *,
        width: float = 1,
        color: str | tuple[int, int, int] = "black",
        cap: CapName = "round",
        start_cap: CapName | None = None,
        end_cap: CapName | None = None,
        opacity: float = 1.0,
        color_brightness: float | None = None,
    ) -> None:
        super().__init__(x, y, z_index)
        self._relative_end: RelCoord | None = None
        self.width = float(width)
        if color_brightness is not None and not isinstance(color, Gradient):
            color = apply_brightness(color, color_brightness)
        self._color = color if isinstance(color, Gradient) else Color(color)
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)

    # --- Relative coordinates ---

    @property
    def relative_start(self) -> RelCoord | None:
        """Relative start position (fraction of reference frame), or None."""
        return self._relative_at

    @relative_start.setter
    def relative_start(self, value: RelCoord | None) -> None:
        self._relative_at = value

    @property
    def relative_end(self) -> RelCoord | None:
        """Relative end position (fraction of reference frame), or None."""
        return self._relative_end

    @relative_end.setter
    def relative_end(self, value: RelCoord | None) -> None:
        self._relative_end = value

    # --- Color ---

    @property
    def color(self) -> str:
        """The stroke paint as a string (color or gradient ref)."""
        if isinstance(self._color, Gradient):
            return self._color.to_svg_ref()
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int] | Gradient) -> None:
        if isinstance(value, Gradient):
            self._color = value
        else:
            self._color = Color(value)

    def _iter_paints(self):
        yield self._color

    # --- Geometry ---

    @property
    def start(self) -> Coord:
        """The starting point (same as position)."""
        return self.position

    @property
    @abstractmethod
    def end(self) -> Coord:
        """The ending point."""

    @property
    def rotation_center(self) -> Coord:
        """Natural pivot for rotation/scale: midpoint between start and end."""
        return self.start.midpoint(self.end)

    # --- Cap handling ---

    @property
    def effective_start_cap(self) -> str:
        """Resolved cap for the start end."""
        return resolve_cap(self.cap, self.start_cap)

    @property
    def effective_end_cap(self) -> str:
        """Resolved cap for the end end."""
        return resolve_cap(self.cap, self.end_cap)

    def get_required_markers(self) -> list[tuple[str, str]]:
        """Collect SVG marker definitions needed by this entity's caps."""
        return collect_markers(self.cap, self.start_cap, self.end_cap, self.width, self.color)

    # --- Relative property support ---

    def _has_relative_properties(self) -> bool:
        return super()._has_relative_properties() or self._relative_end is not None

    def adjust_relative_end(self, dx: float, dy: float) -> None:
        """Adjust relative end coordinates by a pixel delta.

        Used by Line.move_by and Curve.move_by to shift the relative end
        position in tandem with the start when the entity is in relative mode.
        """
        if self._relative_end is not None:
            ref = self._reference or self._surface
            if ref is not None:
                _, _, ref_w, ref_h = ref.ref_frame()
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                erx, ery = self._relative_end
                self._relative_end = RelCoord(erx + drx, ery + dry)
