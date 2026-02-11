"""Entity - Base class for all drawable objects."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from weakref import WeakSet

from .coord import Coord, CoordLike, RelCoord

if TYPE_CHECKING:
    from .surface import Surface
    from .connection import Connection
    from .pathable import Pathable


class Entity(ABC):
    """
    Base class for all drawable objects in PyFreeform.
    
    Entities are objects with identity - they can be moved, connected,
    and tracked. Unlike raw primitives, entities maintain relationships
    with other entities.
    
    Attributes:
        position: Current position (center point for most entities)
        cell: The cell containing this entity (if placed in a grid)
        connections: Set of connections involving this entity
    
    Subclasses must implement:
        - `anchor(name)`: Return anchor point by name
        - `anchor_names`: Property listing available anchor names
        - `to_svg()`: Render to SVG element string
    """
    
    def __init__(self, x: float = 0, y: float = 0, z_index: int = 0) -> None:
        """
        Initialize entity at position.
        
        Args:
            x: Initial x coordinate.
            y: Initial y coordinate.
            z_index: Layer ordering (higher = on top). Default 0.
        """
        self._position = Coord(x, y)
        self._cell: Surface | None = None
        self._connections: WeakSet[Connection] = WeakSet()
        self._data: dict[str, Any] = {}
        self._z_index = z_index

        # Relative coordinate storage
        self._relative_at: RelCoord | None = None
        self._reference: Surface | Entity | None = None
        self._along_path: Pathable | None = None
        self._along_t: float = 0.5
        self._resolving: bool = False
    
    @property
    def z_index(self) -> int:
        """Layer ordering (higher values render on top)."""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        self._z_index = value

    # --- Position resolution ---

    def _resolve_relative(self, rx: float, ry: float) -> Coord | None:
        """Resolve (rx, ry) fractions against this entity's reference frame.

        Returns None if no reference frame is available.
        """
        ref = self._reference or self._cell
        if ref is None:
            return None
        if self._resolving:
            raise ValueError("Circular position reference detected")
        self._resolving = True
        try:
            if isinstance(ref, Entity):
                min_x, min_y, max_x, max_y = ref.bounds()
                return Coord(
                    min_x + rx * (max_x - min_x),
                    min_y + ry * (max_y - min_y),
                )
            else:
                # Surface protocol (Cell, Scene, CellGroup)
                return Coord(
                    ref._x + rx * ref._width,
                    ref._y + ry * ref._height,
                )
        finally:
            self._resolving = False

    def _resolve_size(self, fraction: float, dimension: str = "min") -> float | None:
        """Resolve a size fraction against this entity's reference frame.

        Args:
            fraction: Size as fraction of reference dimension.
            dimension: "width", "height", or "min" (min of both).

        Returns None if no reference frame is available.
        """
        ref = self._reference or self._cell
        if ref is None:
            return None
        if isinstance(ref, Entity):
            min_x, min_y, max_x, max_y = ref.bounds()
            ref_w = max_x - min_x
            ref_h = max_y - min_y
        else:
            ref_w = ref._width
            ref_h = ref._height
        if dimension == "width":
            return fraction * ref_w
        elif dimension == "height":
            return fraction * ref_h
        else:  # "min"
            return fraction * min(ref_w, ref_h)

    def _resolve_position(self) -> Coord:
        """Resolve position from the most specific mode (along > relative > pixel)."""
        if self._along_path is not None:
            return self._along_path.point_at(self._along_t)
        if self._relative_at is not None:
            result = self._resolve_relative(*self._relative_at)
            if result is not None:
                return result
        return self._position

    def _to_pixel_mode(self) -> None:
        """Resolve current position to pixels and clear relative bindings."""
        if self._relative_at is not None or self._along_path is not None:
            self._position = self._resolve_position()
            self._relative_at = None
            self._along_path = None

    @property
    def position(self) -> Coord:
        """Current position of the entity (computed from relative coords if set)."""
        return self._resolve_position()

    @position.setter
    def position(self, value: CoordLike) -> None:
        """Set position in pixels (clears relative bindings)."""
        if isinstance(value, tuple):
            value = Coord(*value)
        self._position = value
        self._relative_at = None
        self._along_path = None

    @property
    def x(self) -> float:
        """X coordinate of position."""
        return self._resolve_position().x

    @property
    def y(self) -> float:
        """Y coordinate of position."""
        return self._resolve_position().y

    @property
    def at(self) -> RelCoord | None:
        """Relative position as (rx, ry) fractions, or None if pixel mode."""
        return self._relative_at

    @at.setter
    def at(self, value: RelCoord | tuple[float, float] | None) -> None:
        """Set relative position (clears along binding)."""
        if value is not None and not isinstance(value, RelCoord):
            value = RelCoord(*value)
        self._relative_at = value
        if value is not None:
            self._along_path = None

    @property
    def cell(self) -> Surface | None:
        """The surface (Cell, Scene, or CellGroup) containing this entity, if any."""
        return self._cell

    @cell.setter
    def cell(self, value: Surface | None) -> None:
        """Set the containing surface."""
        self._cell = value
    
    @property
    def connections(self) -> set[Connection]:
        """Set of connections involving this entity."""
        return set(self._connections)
    
    @property
    def data(self) -> dict[str, Any]:
        """Custom data dictionary for this entity."""
        return self._data
    
    def add_connection(self, connection: Connection) -> None:
        """Register a connection with this entity."""
        self._connections.add(connection)
    
    def remove_connection(self, connection: Connection) -> None:
        """Remove a connection from this entity."""
        self._connections.discard(connection)
    
    # --- Movement methods ---
    
    def _move_to(self, x: float | Coord, y: float | None = None) -> Entity:
        """
        Move entity to absolute pixel position (clears relative bindings).

        Args:
            x: X coordinate, or a Coord.
            y: Y coordinate (required if x is not a Coord).

        Returns:
            self, for method chaining.
        """
        if isinstance(x, Coord):
            self._position = x
        elif y is not None:
            self._position = Coord(x, y)
        else:
            raise ValueError("Must provide both x and y, or a Coord")
        self._relative_at = None
        self._along_path = None
        return self
    
    def _move_by(self, dx: float = 0, dy: float = 0) -> Entity:
        """
        Move entity by a pixel offset.

        In relative mode, converts the pixel offset to a fraction adjustment.
        In along mode, resolves to pixels first, then applies offset.

        Args:
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.

        Returns:
            self, for method chaining.
        """
        if self._along_path is not None:
            # Resolve to pixels, apply offset, switch to pixel mode
            current = self._resolve_position()
            self._position = Coord(current.x + dx, current.y + dy)
            self._along_path = None
            self._relative_at = None
            return self
        if self._relative_at is not None:
            ref = self._reference or self._cell
            if ref is not None:
                # Convert pixel offset to fraction offset
                if isinstance(ref, Entity):
                    min_x, min_y, max_x, max_y = ref.bounds()
                    ref_w = max_x - min_x
                    ref_h = max_y - min_y
                else:
                    ref_w = ref._width
                    ref_h = ref._height
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                rx, ry = self._relative_at
                self._relative_at = RelCoord(rx + drx, ry + dry)
                return self
        self._position = Coord(self._position.x + dx, self._position.y + dy)
        return self
    
    def move_to_cell(self, cell: Surface, at: RelCoord | tuple[float, float] | str = "center") -> Entity:
        """
        Move entity to a position within a cell (stores relative coords).

        Args:
            cell: The target cell/surface.
            at: Position within cell - either a RelCoord / (rx, ry) tuple
                where (0,0) is top-left and (1,1) is bottom-right,
                or a named position like "center", "top_left", etc.

        Returns:
            self, for method chaining.
        """
        from .surface import NAMED_POSITIONS
        self._cell = cell
        if isinstance(at, str):
            at = NAMED_POSITIONS[at]
        if not isinstance(at, RelCoord):
            at = RelCoord(*at)
        self._relative_at = at
        self._along_path = None
        self._reference = None
        return self
    
    # --- Connection methods ---
    
    def connect(
        self,
        other: Entity,
        style: Any | None = None,
        start_anchor: str = "center",
        end_anchor: str = "center",
        shape: Any | None = None,
        segments: int = 32,
    ) -> Connection:
        """
        Create a connection to another entity.

        Args:
            other: The entity to connect to.
            style: Visual style — ConnectionStyle object or dict with
                   "width", "color", "z_index" keys.
            start_anchor: Anchor name on this entity.
            end_anchor: Anchor name on the other entity.
            shape: Visual shape — Line(), Curve(), Path(), or None
                   for invisible.
            segments: Number of Bézier segments for shape rendering.

        Returns:
            The created Connection.
        """
        from .connection import Connection

        connection = Connection(
            start=self,
            end=other,
            start_anchor=start_anchor,
            end_anchor=end_anchor,
            style=style,
            shape=shape,
            segments=segments,
        )
        return connection
    
    # --- Transform methods ---
    
    def rotate(self, angle: float, origin: CoordLike | None = None) -> Entity:
        """
        Rotate entity around a point (switches to pixel mode).

        For simple entities (Dot), this just rotates the position.
        Complex entities (Line, Polygon) override this to rotate their geometry.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: entity position).

        Returns:
            self, for method chaining.
        """
        import math

        if origin is None:
            return self

        if isinstance(origin, tuple):
            origin = Coord(*origin)

        self._to_pixel_mode()

        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        dx = self._position.x - origin.x
        dy = self._position.y - origin.y
        new_x = dx * cos_a - dy * sin_a + origin.x
        new_y = dx * sin_a + dy * cos_a + origin.y
        self._position = Coord(new_x, new_y)

        return self
    
    def scale(self, factor: float, origin: CoordLike | None = None) -> Entity:
        """
        Scale entity around a point (switches to pixel mode).

        For simple entities, this scales the position relative to origin.
        Complex entities override this to scale their geometry.

        Args:
            factor: Scale factor (1.0 = no change, 2.0 = double distance from origin).
            origin: Center of scaling (default: entity position).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            return self

        if isinstance(origin, tuple):
            origin = Coord(*origin)

        self._to_pixel_mode()

        new_x = origin.x + (self._position.x - origin.x) * factor
        new_y = origin.y + (self._position.y - origin.y) * factor
        self._position = Coord(new_x, new_y)

        return self
    
    def _offset_from(self, anchor_name: str, dx: float = 0, dy: float = 0) -> Coord:
        """
        Get a point offset from a named anchor.

        Sugar for ``entity.anchor(name) + Coord(dx, dy)``.

        Args:
            anchor_name: Name of the anchor (e.g., "center", "top_left").
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.

        Returns:
            The offset point.
        """
        return self.anchor(anchor_name) + Coord(dx, dy)

    def place_beside(self, other: Entity, side: str = "right", gap: float = 0) -> Entity:
        """
        Position this entity beside another using bounding boxes.

        Args:
            other: Reference entity to position relative to.
            side: "right", "left", "above", or "below".
            gap: Pixels between bounding boxes.

        Returns:
            self, for method chaining.
        """
        o_min_x, o_min_y, o_max_x, o_max_y = other.bounds()
        s_min_x, s_min_y, s_max_x, s_max_y = self.bounds()
        s_w = s_max_x - s_min_x
        s_h = s_max_y - s_min_y
        s_cx = (s_min_x + s_max_x) / 2
        s_cy = (s_min_y + s_max_y) / 2
        o_cx = (o_min_x + o_max_x) / 2
        o_cy = (o_min_y + o_max_y) / 2

        if side == "right":
            tx, ty = o_max_x + gap + s_w / 2, o_cy
        elif side == "left":
            tx, ty = o_min_x - gap - s_w / 2, o_cy
        elif side == "above":
            tx, ty = o_cx, o_min_y - gap - s_h / 2
        elif side == "below":
            tx, ty = o_cx, o_max_y + gap + s_h / 2
        else:
            raise ValueError(f"Invalid side '{side}'. Use 'right', 'left', 'above', 'below'.")

        self._move_by(tx - s_cx, ty - s_cy)
        return self

    # --- Abstract methods for subclasses ---
    
    @property
    @abstractmethod
    def anchor_names(self) -> list[str]:
        """List of available anchor names for this entity."""
        pass
    
    @abstractmethod
    def anchor(self, name: str) -> Coord:
        """
        Get anchor point by name.

        Args:
            name: Anchor name (e.g., "center", "start", "end").

        Returns:
            The anchor position as a Coord.
        
        Raises:
            ValueError: If anchor name is not valid for this entity.
        """
        pass
    
    @abstractmethod
    def to_svg(self) -> str:
        """
        Render this entity to an SVG element string.
        
        Returns:
            SVG element (e.g., '<circle ... />').
        """
        pass
    
    @abstractmethod
    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """
        Get bounding box of this entity.

        Args:
            visual: If True, include stroke width in the bounds so the
                    result reflects the rendered (visual) extent rather
                    than pure geometry. Default is False (geometric bounds).

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        pass

    def get_required_markers(self) -> list[tuple[str, str]]:
        """Collect SVG marker definitions needed by this entity.

        Returns:
            List of (marker_id, marker_svg) tuples. Empty by default.
        """
        return []

    def get_required_paths(self) -> list[tuple[str, str]]:
        """Collect SVG path definitions needed by this entity (e.g. textPath).

        Returns:
            List of (path_id, path_svg) tuples. Empty by default.
        """
        return []

    def inner_bounds(self) -> tuple[float, float, float, float]:
        """
        Largest axis-aligned rectangle fully inside this entity.

        Override for non-rectangular shapes (e.g. circles, ellipses)
        to return the inscribed rectangle. Default: same as bounds().

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        return self.bounds()

    def _rotated_bounds(
        self, angle: float, *, visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Tight AABB of this entity's geometry rotated by *angle* degrees
        around the origin.

        The default rotates the four corners of ``bounds()``.  Subclasses
        override with exact analytical formulas (e.g. Bezier extrema,
        ellipse extents) so that ``EntityGroup`` can compose tight bounds
        without sampling.
        """
        b = self.bounds(visual=visual)
        if angle == 0:
            return b
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        corners = ((b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3]))
        rx = [x * cos_a - y * sin_a for x, y in corners]
        ry = [x * sin_a + y * cos_a for x, y in corners]
        return (min(rx), min(ry), max(rx), max(ry))

    # --- Rotation algorithms for fitting ---

    @staticmethod
    def _compute_optimal_angle(w: float, h: float, W: float, H: float) -> float:
        """O(1) angle (degrees) that maximizes min(W/bbox_w, H/bbox_h).

        Uses the AABB rotation identity:
            bbox_w(θ) = w·|cos θ| + h·|sin θ|
            bbox_h(θ) = w·|sin θ| + h·|cos θ|

        Only three candidate angles: 0°, 90°, and the balanced angle.
        """
        if w < 1e-9 or h < 1e-9 or W < 1e-9 or H < 1e-9:
            return 0.0

        def scale_at(angle_rad: float) -> float:
            cos_a = abs(math.cos(angle_rad))
            sin_a = abs(math.sin(angle_rad))
            bw = w * cos_a + h * sin_a
            bh = w * sin_a + h * cos_a
            return min(W / bw, H / bh)

        candidates = [0.0, math.pi / 2]

        numerator = H * w - W * h
        denominator = W * w - H * h
        if abs(denominator) > 1e-9:
            theta = math.atan2(numerator, denominator)
            theta = theta % math.pi
            if theta > math.pi / 2:
                theta -= math.pi / 2
            if 0 < theta < math.pi / 2:
                candidates.append(theta)

        best = max(candidates, key=scale_at)
        return math.degrees(best)

    @staticmethod
    def _compute_aspect_match_angle(
        w: float, h: float, target_w: float, target_h: float,
    ) -> float:
        """O(1) angle (degrees) that makes bbox aspect ratio ≈ target_w/target_h.

        Solves: (w·cos θ + h·sin θ) / (w·sin θ + h·cos θ) = r
        giving:  tan θ = (w - r·h) / (r·w - h)
        """
        if w < 1e-9 or h < 1e-9 or target_w < 1e-9 or target_h < 1e-9:
            return 0.0

        r = target_w / target_h
        current_ratio = w / h
        if abs(current_ratio - r) < 1e-6:
            return 0.0  # already matching

        numerator = w - r * h
        denominator = r * w - h

        if abs(denominator) < 1e-9:
            return 90.0

        theta_deg = math.degrees(math.atan(numerator / denominator))

        # If outside [0, 90°], target ratio isn't achievable —
        # return whichever boundary is closer.
        if theta_deg < 0 or theta_deg > 90:
            ratio_90 = h / w
            return 0.0 if abs(current_ratio - r) <= abs(ratio_90 - r) else 90.0

        return theta_deg

    def fit_within(
        self,
        target: Entity | tuple[float, float, float, float],
        scale: float = 1.0,
        recenter: bool = True,
        *,
        at: RelCoord | tuple[float, float] | None = None,
        visual: bool = True,
        rotate: bool = False,
        match_aspect: bool = False,
    ) -> Entity:
        """
        Scale and position entity to fit within another entity's inner bounds.

        Args:
            target: Entity (uses inner_bounds()) or raw (min_x, min_y, max_x, max_y) tuple.
            scale: Fraction of target inner bounds to fill (0.0-1.0].
            recenter: If True, center entity within target after scaling.
                      Ignored when ``at`` is provided.
            at: Optional relative position (rx, ry) within the target's
                inner bounds, where (0,0) is top-left and (1,1) is
                bottom-right. Available space is constrained by the
                nearest edges so the entity never overflows.
            visual: If True (default), include stroke width when measuring
                    bounds so stroked entities don't overflow after fitting.
                    Set to False for pure geometric fitting.
            rotate: If True, find the rotation angle that maximizes how
                    much of the target space the entity fills before
                    scaling.
            match_aspect: If True, rotate the entity so its bounding box
                          aspect ratio matches the target's. Mutually
                          exclusive with ``rotate``.

        Returns:
            self, for method chaining.

        Example:
            >>> dot = cell.add_dot(radius=0.5, color="navy")
            >>> label = cell.add_text("0.5", color="white", font_size=50)
            >>> label.fit_within(dot)
            >>> # Position in top-left of a rect's inner bounds:
            >>> label.fit_within(rect, at=(0.25, 0.25))
        """
        if rotate and match_aspect:
            raise ValueError("rotate and match_aspect are mutually exclusive")

        if not (0.0 < scale <= 1.0):
            raise ValueError(f"scale must be between 0.0 and 1.0, got {scale}")

        # Resolve target bounds
        if isinstance(target, Entity):
            t_min_x, t_min_y, t_max_x, t_max_y = target.inner_bounds()
        else:
            t_min_x, t_min_y, t_max_x, t_max_y = target

        target_w = t_max_x - t_min_x
        target_h = t_max_y - t_min_y

        if rotate or match_aspect:
            b = self.bounds(visual=visual)
            w, h = b[2] - b[0], b[3] - b[1]
            if w > 1e-9 and h > 1e-9:
                if at is not None:
                    rx, ry = at
                    avail_w = min(rx, 1 - rx) * 2 * target_w * scale
                    avail_h = min(ry, 1 - ry) * 2 * target_h * scale
                else:
                    avail_w = target_w * scale
                    avail_h = target_h * scale
                angle = (
                    Entity._compute_optimal_angle(w, h, avail_w, avail_h)
                    if rotate else
                    Entity._compute_aspect_match_angle(w, h, avail_w, avail_h)
                )
                self.rotate(angle)

        if at is not None:
            # --- Position-aware mode ---
            rx, ry = at
            if not (0.0 < rx < 1.0 and 0.0 < ry < 1.0):
                raise ValueError(
                    f"at=({rx}, {ry}) must be inside the bounds "
                    f"(0.0-1.0 exclusive)."
                )

            # Target position in absolute coordinates
            target_x = t_min_x + rx * target_w
            target_y = t_min_y + ry * target_h

            # Available space constrained by nearest edge
            available_w = min(target_x - t_min_x, t_max_x - target_x) * 2 * scale
            available_h = min(target_y - t_min_y, t_max_y - target_y) * 2 * scale

            # Get entity's bounding box
            e_min_x, e_min_y, e_max_x, e_max_y = self.bounds(visual=visual)
            entity_w = e_max_x - e_min_x
            entity_h = e_max_y - e_min_y

            # Scale factors
            scale_x = available_w / entity_w if entity_w > 0 else 1.0
            scale_y = available_h / entity_h if entity_h > 0 else 1.0
            factor = min(scale_x, scale_y)

            entity_center = Coord(
                (e_min_x + e_max_x) / 2, (e_min_y + e_max_y) / 2,
            )
            if abs(factor - 1.0) > 0.001:
                self.scale(factor, origin=entity_center)

            # Move to target position
            new_bounds = self.bounds(visual=visual)
            new_cx = (new_bounds[0] + new_bounds[2]) / 2
            new_cy = (new_bounds[1] + new_bounds[3]) / 2
            self._move_by(target_x - new_cx, target_y - new_cy)

            return self

        # --- Default mode (at=None) ---
        target_cx = (t_min_x + t_max_x) / 2
        target_cy = (t_min_y + t_max_y) / 2

        # Get entity's bounding box
        e_min_x, e_min_y, e_max_x, e_max_y = self.bounds(visual=visual)
        entity_w = e_max_x - e_min_x
        entity_h = e_max_y - e_min_y

        # Calculate available space
        available_w = target_w * scale
        available_h = target_h * scale

        # Scale factors
        scale_x = available_w / entity_w if entity_w > 0 else 1.0
        scale_y = available_h / entity_h if entity_h > 0 else 1.0
        factor = min(scale_x, scale_y)

        # Scale around entity center if needed
        entity_cx = (e_min_x + e_max_x) / 2
        entity_cy = (e_min_y + e_max_y) / 2

        if abs(factor - 1.0) > 0.001:
            self.scale(factor, origin=Coord(entity_cx, entity_cy))

        # Recenter within target
        if recenter:
            new_bounds = self.bounds(visual=visual)
            new_cx = (new_bounds[0] + new_bounds[2]) / 2
            new_cy = (new_bounds[1] + new_bounds[3]) / 2
            self._move_by(target_cx - new_cx, target_cy - new_cy)

        return self

    def fit_to_cell(
        self,
        scale: float = 1.0,
        recenter: bool = True,
        *,
        at: RelCoord | tuple[float, float] | None = None,
        visual: bool = True,
        rotate: bool = False,
        match_aspect: bool = False,
    ) -> Entity:
        """
        Automatically scale and position entity to fit within its cell bounds.

        Works for any entity type and handles rotation automatically by using
        the entity's actual bounding box.

        Args:
            scale: Percentage of available space to fill (0.0-1.0).
                   1.0 = fill entire available area, 0.85 = use 85%.
            recenter: If True, center entity in cell after scaling.
                      If False, maintain current position.
                      Ignored when ``at`` is provided.
            at: Optional cell-relative position (rx, ry) where both values
                are in (0.0, 1.0) exclusive. When provided, the entity is
                positioned at this point and the available space is
                constrained by the nearest cell edges, so the entity never
                overflows.  At (0.5, 0.5) the full cell is available (same
                as the default).  At (0.25, 0.25) only the top-left
                quadrant is usable.
            visual: If True (default), include stroke width when measuring
                    bounds so stroked entities don't overflow after fitting.
                    Set to False for pure geometric fitting.
            rotate: If True, find the rotation angle that maximizes how
                    much of the cell the entity fills before scaling.
            match_aspect: If True, rotate the entity so its bounding box
                          aspect ratio matches the cell's. Mutually
                          exclusive with ``rotate``.

        Returns:
            self, for method chaining

        Raises:
            ValueError: If entity has no cell, scale is out of range,
                        or both ``rotate`` and ``match_aspect`` are True.
            TypeError: If ``at`` is a string (named anchors sit on cell
                       edges where available space is 0).

        Example:
            >>> ellipse = cell.add_ellipse(rx=2.0, ry=1.2, rotation=45)
            >>> ellipse.fit_to_cell(0.85)  # Auto-constrain to 85% of cell
            >>> dot = cell.add_dot(radius=0.8)
            >>> dot.fit_to_cell(1.0, at=(0.25, 0.25))  # Fit in top-left quadrant
        """
        if rotate and match_aspect:
            raise ValueError("rotate and match_aspect are mutually exclusive")

        # Validation
        if self._cell is None:
            raise ValueError("Cannot fit to cell: entity has no cell")

        if not (0.0 < scale <= 1.0):
            raise ValueError(f"scale must be between 0.0 and 1.0, got {scale}")

        cell = self._cell

        if rotate or match_aspect:
            b = self.bounds(visual=visual)
            w, h = b[2] - b[0], b[3] - b[1]
            if w > 1e-9 and h > 1e-9:
                if at is not None:
                    if isinstance(at, str):
                        raise TypeError(
                            f"fit_to_cell(at=) only accepts (rx, ry) tuples, "
                            f"not '{at}'."
                        )
                    rx, ry = at
                    target_pos = cell.relative_to_absolute(at)
                    cell_x, cell_y = cell.x, cell.y
                    cell_w, cell_h = cell.width, cell.height
                    dist_left = target_pos.x - cell_x
                    dist_right = (cell_x + cell_w) - target_pos.x
                    dist_top = target_pos.y - cell_y
                    dist_bottom = (cell_y + cell_h) - target_pos.y
                    avail_w = min(dist_left, dist_right) * 2 * scale
                    avail_h = min(dist_top, dist_bottom) * 2 * scale
                else:
                    avail_w = cell.width * scale
                    avail_h = cell.height * scale
                angle = (
                    Entity._compute_optimal_angle(w, h, avail_w, avail_h)
                    if rotate else
                    Entity._compute_aspect_match_angle(w, h, avail_w, avail_h)
                )
                self.rotate(angle)

        if at is not None:
            # --- Position-aware mode ---
            if isinstance(at, str):
                raise TypeError(
                    f"fit_to_cell(at=) only accepts (rx, ry) tuples, not '{at}'. "
                    f"Named positions are at cell edges where available space is 0."
                )
            rx, ry = at
            if not (0.0 < rx < 1.0 and 0.0 < ry < 1.0):
                raise ValueError(
                    f"at=({rx}, {ry}) must be inside the cell (0.0-1.0 exclusive). "
                    f"Values at edges leave no room for the entity."
                )

            # Target position in absolute coordinates
            target = cell.relative_to_absolute(at)
            cell_x, cell_y = cell.x, cell.y
            cell_w, cell_h = cell.width, cell.height

            # Available space = constrained by nearest edge in each direction
            dist_left = target.x - cell_x
            dist_right = (cell_x + cell_w) - target.x
            dist_top = target.y - cell_y
            dist_bottom = (cell_y + cell_h) - target.y

            available_w = min(dist_left, dist_right) * 2 * scale
            available_h = min(dist_top, dist_bottom) * 2 * scale

            # Get entity's bounding box
            e_min_x, e_min_y, e_max_x, e_max_y = self.bounds(visual=visual)
            entity_w = e_max_x - e_min_x
            entity_h = e_max_y - e_min_y

            # Calculate scale factors
            scale_x = available_w / entity_w if entity_w > 0 else 1.0
            scale_y = available_h / entity_h if entity_h > 0 else 1.0
            factor = min(scale_x, scale_y)

            # Scale around entity center if needed
            entity_center = Coord(
                (e_min_x + e_max_x) / 2,
                (e_min_y + e_max_y) / 2,
            )
            if abs(factor - 1.0) > 0.001:
                self.scale(factor, origin=entity_center)

            # Move to target position
            new_bounds = self.bounds(visual=visual)
            new_cx = (new_bounds[0] + new_bounds[2]) / 2
            new_cy = (new_bounds[1] + new_bounds[3]) / 2
            self._move_by(target.x - new_cx, target.y - new_cy)

            return self

        # --- Default mode (at=None) ---

        # Get entity's bounding box
        entity_min_x, entity_min_y, entity_max_x, entity_max_y = self.bounds(visual=visual)
        entity_width = entity_max_x - entity_min_x
        entity_height = entity_max_y - entity_min_y

        # Get cell bounds
        cell_x = cell.x
        cell_y = cell.y
        cell_width = cell.width
        cell_height = cell.height

        # Calculate available space (with scale factor)
        available_width = cell_width * scale
        available_height = cell_height * scale

        # Calculate scale factors needed to fit
        if entity_width > 0:
            scale_x = available_width / entity_width
        else:
            scale_x = 1.0

        if entity_height > 0:
            scale_y = available_height / entity_height
        else:
            scale_y = 1.0

        # Use smaller scale to maintain aspect ratio and fit within bounds
        scale_factor = min(scale_x, scale_y)

        # If already fits, skip scaling (optimization)
        if abs(scale_factor - 1.0) < 0.001:  # Allow small floating point error
            if recenter:
                # Just recenter without scaling
                cell_center = Coord(
                    cell_x + cell_width / 2,
                    cell_y + cell_height / 2
                )
                entity_center_x = (entity_min_x + entity_max_x) / 2
                entity_center_y = (entity_min_y + entity_max_y) / 2
                offset_x = cell_center.x - entity_center_x
                offset_y = cell_center.y - entity_center_y
                self._move_by(offset_x, offset_y)
            return self

        # Calculate entity's current center (before scaling)
        entity_center = Coord(
            (entity_min_x + entity_max_x) / 2,
            (entity_min_y + entity_max_y) / 2
        )

        # Scale around entity's current center
        self.scale(scale_factor, origin=entity_center)

        # Recenter in cell if requested
        if recenter:
            # Get new bounds after scaling
            new_min_x, new_min_y, new_max_x, new_max_y = self.bounds(visual=visual)
            new_center_x = (new_min_x + new_max_x) / 2
            new_center_y = (new_min_y + new_max_y) / 2

            # Calculate offset to cell center
            cell_center_x = cell_x + cell_width / 2
            cell_center_y = cell_y + cell_height / 2

            offset_x = cell_center_x - new_center_x
            offset_y = cell_center_y - new_center_y

            self._move_by(offset_x, offset_y)

        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"
