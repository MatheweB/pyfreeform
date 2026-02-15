"""Entity - Base class for all drawable objects."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from ..color import ColorLike
from .binding import Binding
from .connection import Connection
from .coord import Coord, CoordLike
from .relcoord import RelCoord, RelCoordLike
from .positions import NAMED_POSITIONS, AnchorSpec
from .svg_utils import svg_num


if TYPE_CHECKING:
    from ..config.caps import CapName
    from ..config.styles import PathStyle
    from ..entities.path import Path
    from .pathable import Pathable
    from .surface import Surface


class Entity(ABC):
    """
    Base class for all drawable objects in PyFreeform.

    Entities are objects with identity - they can be moved, connected,
    and tracked. Unlike raw primitives, entities maintain relationships
    with other entities.

    Attributes:
        position: Current position (center point for most entities)
        cell: The cell containing this entity (if placed in a grid)
        connections: Connections involving this entity

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
        self._connections: dict[Connection, None] = {}
        self._data: dict[str, Any] = {}
        self._z_index = z_index

        # Relative coordinate storage
        self._relative_at: RelCoord | None = None
        self._reference: Surface | Entity | None = None
        self._along_path: Pathable | None = None
        self._along_t: float = 0.5
        self._resolving: bool = False

        # Non-destructive transforms (accumulated, resolved at render time)
        self._rotation: float = 0.0
        self._scale_factor: float = 1.0

    @property
    def z_index(self) -> int:
        """Layer ordering (higher values render on top)."""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        self._z_index = value

    @property
    def rotation(self) -> float:
        """Rotation angle in degrees (accumulated, non-destructive)."""
        return self._rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        self._rotation = float(value)

    @property
    def scale_factor(self) -> float:
        """Scale factor (accumulated, non-destructive). Default 1.0."""
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value: float) -> None:
        self._scale_factor = float(value)

    @property
    def rotation_center(self) -> Coord:
        """The center point for rotation and scaling transforms.

        Default: entity position. Override for entities where the
        natural pivot differs (e.g., Rect center, Polygon centroid).
        """
        return self.position

    def ref_frame(self) -> tuple[float, float, float, float]:
        """Return (x, y, width, height) of this entity's bounding box.

        Provides a unified interface for both Entity and Surface,
        eliminating the need for isinstance checks when resolving
        relative coordinates.
        """
        min_x, min_y, max_x, max_y = self.bounds()
        return (min_x, min_y, max_x - min_x, max_y - min_y)

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
            ref_x, ref_y, ref_w, ref_h = ref.ref_frame()
            return Coord(ref_x + rx * ref_w, ref_y + ry * ref_h)
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
        _, _, ref_w, ref_h = ref.ref_frame()
        if dimension == "width":
            return fraction * ref_w
        if dimension == "height":
            return fraction * ref_h
        # "min"
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

    def _has_relative_properties(self) -> bool:
        """Return True if this entity has any relative state.

        Subclasses override to include entity-specific relative properties
        (e.g. relative_radius, relative_width, relative_vertices).
        """
        return self._relative_at is not None or self._along_path is not None

    @property
    def is_relative(self) -> bool:
        """True when any property is relative (entity reacts to container changes).

        Check individual properties (``.at``, ``.relative_radius``, etc.)
        to see which specific properties are tracked.
        """
        return self._has_relative_properties()

    def _resolve_to_absolute(self) -> None:
        """Convert all relative properties to absolute values.

        The base class resolves **position** (relative binding → concrete
        ``Coord``).  Subclasses extend this to also resolve **sizing**
        (e.g. radius, width/height) and **geometry** (e.g. vertices,
        endpoints) from relative fractions to absolute values.

        This is an explicit opt-in escape hatch.  The framework never
        calls it automatically — only user code that needs pixel values.
        """
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
        value = Coord.coerce(value)
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
        """Relative position as (rx, ry) fractions, or None if absolute mode."""
        return self._relative_at

    @at.setter
    def at(self, value: RelCoordLike | None) -> None:  # RelCoord | tuple[float, float]
        """Set relative position (clears along binding)."""
        if value is not None:
            value = RelCoord.coerce(value)
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
        """Connections involving this entity (insertion-ordered internally)."""
        return set(self._connections)

    @property
    def data(self) -> dict[str, Any]:
        """Custom data dictionary for this entity."""
        return self._data

    def add_connection(self, connection: Connection) -> None:
        """Register a connection with this entity."""
        self._connections[connection] = None

    def remove_connection(self, connection: Connection) -> None:
        """Remove a connection from this entity."""
        self._connections.pop(connection, None)

    # --- Binding ---

    @property
    def binding(self) -> Binding | None:
        """Current positioning binding, or None if absolutely positioned.

        Returns a ``Binding`` describing how this entity is positioned:
        relative (``at``), along a path (``along`` + ``t``), or ``None``
        for absolute mode.
        """
        if self._along_path is not None:
            return Binding(along=self._along_path, t=self._along_t, reference=self._reference)
        if self._relative_at is not None:
            return Binding(at=self._relative_at, reference=self._reference)
        return None

    @binding.setter
    def binding(self, value: Binding | None) -> None:
        """Set positioning binding (clears previous mode)."""
        if value is None:
            self._relative_at = None
            self._along_path = None
            self._along_t = 0.5
            self._reference = None
            return
        if value.along is not None:
            self._along_path = value.along
            self._along_t = value.t
            self._relative_at = None
        elif value.at is not None:
            self._relative_at = value.at
            self._along_path = None
            self._along_t = 0.5
        if value.reference is not None:
            self._reference = value.reference

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
            # Resolve to absolute position, apply offset, switch to absolute mode
            current = self._resolve_position()
            self._position = Coord(current.x + dx, current.y + dy)
            self._along_path = None
            self._relative_at = None
            return self
        if self._relative_at is not None:
            ref = self._reference or self._cell
            if ref is not None:
                # Convert pixel offset to fraction offset
                _, _, ref_w, ref_h = ref.ref_frame()
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                rx, ry = self._relative_at
                self._relative_at = RelCoord(rx + drx, ry + dry)
                return self
        self._position = Coord(self._position.x + dx, self._position.y + dy)
        return self

    def move_to_cell(self, cell: Surface, at: RelCoordLike = "center") -> Entity:
        """
        Move entity to a position within a cell (stores relative coords).

        Args:
            cell: The target cell/surface.
            at: RelCoordLike within cell - either a RelCoord / (rx, ry) tuple
                where (0,0) is top-left and (1,1) is bottom-right,
                or a named position like "center", "top_left", etc.

        Returns:
            self, for method chaining.
        """

        self._cell = cell
        if isinstance(at, str) and at in NAMED_POSITIONS:
            at = NAMED_POSITIONS[at]
        else:
            raise TypeError(
                f'Cannot use "{at}" for move_to_cell. String must be in NAMED_POSITIONS (e.g. "center")'
            )
        at = RelCoord.coerce(at)
        self._relative_at = at
        self._along_path = None
        self._reference = None
        return self

    # --- Connection methods ---

    def connect(
        self,
        other: Entity | Surface,
        start_anchor: AnchorSpec = "center",
        end_anchor: AnchorSpec = "center",
        *,
        path: Path | None = None,
        curvature: float | None = None,
        visible: bool = True,
        width: float = 1,
        color: ColorLike = "black",
        z_index: int = 0,
        cap: CapName = "round",
        start_cap: CapName | None = None,
        end_cap: CapName | None = None,
        opacity: float = 1.0,
        color_brightness: float | None = None,
        style: PathStyle | None = None,
        segments: int = 32,
    ) -> Connection:
        """
        Create a connection to another entity or surface.

        Args:
            other: The entity or surface to connect to.
            start_anchor: Anchor spec on this entity (name, RelCoord, or tuple).
            end_anchor: Anchor spec on the other object.
            path:   Custom path geometry (e.g. Path.Wave()). For simple arcs
                    use ``curvature`` instead.
            curvature:  Arc curvature (-1 to 1). Positive bows left,
                        negative bows right. Cannot be used with ``path``.
            visible: Whether the connection renders. Default True.
            width: Line width in pixels.
            color: Line color.
            z_index: Layer order (higher = on top).
            cap: Cap style for both ends.
            start_cap: Override cap for start end (e.g. "arrow").
            end_cap: Override cap for end end (e.g. "arrow").
            opacity: Opacity (0.0 transparent to 1.0 opaque).
            color_brightness: Brightness multiplier 0.0 (black) to 1.0 (unchanged).
            style: PathStyle object (overrides individual params).
            segments: Number of Bézier segments for path rendering.

        Returns:
            The created Connection.
        """

        return Connection(
            start=self,
            end=other,
            start_anchor=start_anchor,
            end_anchor=end_anchor,
            path=path,
            curvature=curvature,
            visible=visible,
            width=width,
            color=color,
            z_index=z_index,
            cap=cap,
            start_cap=start_cap,
            end_cap=end_cap,
            opacity=opacity,
            color_brightness=color_brightness,
            style=style,
            segments=segments,
        )

    # --- Distance methods ---

    def distance_to(self, other: Entity | Surface | Coord | tuple[float, float]) -> float:
        """
        Euclidean pixel distance from this entity's position to another.

        Accepts: Entity (uses position), Cell/Surface (uses center),
        Coord, or (x, y) tuple.

        Args:
            other: An Entity, Surface/Cell, Coord, or (x, y) tuple.

        Returns:
            Distance in pixels.
        """
        if isinstance(other, Entity):
            target = other.position
        elif isinstance(other, Coord):
            target = other
        elif isinstance(other, tuple):
            target = Coord(*other)
        elif hasattr(other, "center"):
            target = Coord.coerce(other.center)
        else:
            raise TypeError(
                f"Expected Entity, Surface, Coord, or tuple, got {type(other).__name__}"
            )
        return self.position.distance_to(target)

    # --- Transform methods ---

    def _to_world_space(self, model_point: Coord) -> Coord:
        """Transform a model-space point to world space.

        Applies scale then rotation around ``rotation_center``.
        Identity transforms are short-circuited.
        """
        if self._rotation == 0 and self._scale_factor == 1.0:
            return model_point
        center = self.rotation_center
        delta = model_point - center
        if self._scale_factor != 1.0:
            delta = Coord(delta.x * self._scale_factor, delta.y * self._scale_factor)
        if self._rotation != 0:
            delta = delta.rotated(math.radians(self._rotation))
        return center + delta

    def _build_svg_transform(self) -> str:
        """Build SVG ``transform`` attribute string for current rotation/scale.

        Returns an empty string when both are identity, otherwise a
        fully-formed ``' transform="..."'`` attribute (leading space included).
        """
        has_rot = self._rotation != 0
        has_scale = self._scale_factor != 1.0
        if not has_rot and not has_scale:
            return ""
        center = self.rotation_center
        cx, cy = svg_num(center.x), svg_num(center.y)
        ncx, ncy = svg_num(-center.x), svg_num(-center.y)
        if has_rot and not has_scale:
            return f' transform="rotate({svg_num(self._rotation)} {cx} {cy})"'
        if has_scale and not has_rot:
            s = svg_num(self._scale_factor)
            return f' transform="translate({cx},{cy}) scale({s}) translate({ncx},{ncy})"'
        # Both rotation and scale
        s = svg_num(self._scale_factor)
        return (
            f' transform="translate({cx},{cy})'
            f" rotate({svg_num(self._rotation)})"
            f" scale({s})"
            f' translate({ncx},{ncy})"'
        )

    def _orbit_around(self, angle: float, origin: Coord) -> None:
        """Orbit this entity's rotation_center around *origin* by *angle* degrees.

        Computes the new orbital location lazily from ``rotation_center``
        (which resolves relative coordinates on access), then shifts
        position via ``_move_by`` (which preserves relative mode).
        Does **not** accumulate ``_rotation``.
        """
        center = self.rotation_center
        new_center = center.rotated(math.radians(angle), origin=origin)
        self._move_by(new_center.x - center.x, new_center.y - center.y)

    def _scale_around(self, factor: float, origin: Coord) -> None:
        """Scale this entity's position relative to *origin* (orbit only).

        Computes the new position lazily from ``rotation_center``
        (which resolves relative coordinates on access), then shifts
        position via ``_move_by`` (which preserves relative mode).
        Does **not** accumulate ``_scale_factor``.
        """
        center = self.rotation_center
        new_center = origin + (center - origin) * factor
        self._move_by(new_center.x - center.x, new_center.y - center.y)

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Entity:
        """
        Rotate entity by *angle* degrees.

        Without *origin*, rotates in place. With *origin*, also moves
        the entity around that point (like orbiting).

        Args:
            angle: Rotation in degrees (counterclockwise).
            origin: Point to rotate around. If ``None``, rotates in
                    place around the entity's natural center.

        Returns:
            self, for method chaining.
        """
        if origin is not None:
            self._orbit_around(angle, Coord.coerce(origin))
        self._rotation = (self._rotation + angle) % 360
        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Entity:
        """
        Scale entity by *factor*.

        Without *origin*, scales around the entity's natural center.
        With *origin*, also moves the entity toward/away from that point.

        Args:
            factor: Scale multiplier (1.0 = no change, 2.0 = double).
            origin: Point to scale around. If ``None``, scales around
                    the entity's natural center.

        Returns:
            self, for method chaining.
        """
        if origin is not None:
            self._scale_around(factor, Coord.coerce(origin))
        self._scale_factor *= factor
        return self

    def offset_from(self, anchor_spec: AnchorSpec, dx: float = 0, dy: float = 0) -> Coord:
        """
        Get a point offset from an anchor.

        Sugar for ``entity.anchor(spec) + Coord(dx, dy)``.

        Args:
            anchor_spec: Anchor name, RelCoord, or (rx, ry) tuple.
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.

        Returns:
            The offset point.
        """
        return self.anchor(anchor_spec) + Coord(dx, dy)

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

    def anchor(self, spec: AnchorSpec = "center") -> Coord:
        """
        Get anchor point by name or relative coordinate.

        Args:
            spec: Anchor specification. Can be:
                - A string name (e.g., "center", "start", "top_left", "v0")
                - A RelCoord or (rx, ry) tuple (0.0-1.0 fractions of bounding box)

        Returns:
            The anchor position as a Coord.

        Raises:
            ValueError: If string name is not valid for this entity.
        """
        if isinstance(spec, str):
            return self._named_anchor(spec)
        rc = RelCoord.coerce(spec)
        return self._anchor_from_relcoord(rc)

    @abstractmethod
    def _named_anchor(self, name: str) -> Coord:
        """Entity-specific named anchor resolution.

        Each entity type defines its own named anchors here.
        Called by ``anchor()`` when given a string.
        """

    def _anchor_from_relcoord(self, rc: RelCoord) -> Coord:
        """Resolve a RelCoord against this entity's axis-aligned bounding box.

        Maps (0,0) to the min corner and (1,1) to the max corner of ``bounds()``.
        Override for rotation-aware entities (e.g., Rect).
        """
        min_x, min_y, max_x, max_y = self.bounds()
        return Coord(
            min_x + rc.rx * (max_x - min_x),
            min_y + rc.ry * (max_y - min_y),
        )

    @abstractmethod
    def to_svg(self) -> str:
        """
        Render this entity to an SVG element string.

        Returns:
            SVG element (e.g., '<circle ... />').
        """

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

    def rotated_bounds(
        self,
        angle: float,
        *,
        visual: bool = False,
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
        w: float,
        h: float,
        target_w: float,
        target_h: float,
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
        at: RelCoordLike | None = None,
        visual: bool = True,
        rotate: bool = False,
        match_aspect: bool = False,
    ) -> Entity:
        """
        Scale and position entity to fit within another entity's inner bounds.

        Args:
            target: Entity (uses inner_bounds()) or raw (min_x, min_y, max_x, max_y) tuple.
            scale: Fraction of target inner bounds to fill (0.0-1.0].
            recenter:   If True, center entity within target after scaling.
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
            match_aspect:   If True, rotate the entity so its bounding box
                            aspect ratio matches the target's. Mutually
                            exclusive with ``rotate``.

        Returns:
            self, for method chaining.

        Example:
            ```python
            dot = cell.add_dot(radius=0.5, color="navy")
            label = cell.add_text("0.5", color="white", font_size=50)
            label.fit_within(dot)
            # Position in top-left of a rect's inner bounds:
            label.fit_within(rect, at=(0.25, 0.25))
            ```
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
                    rx, ry = RelCoord.coerce(at)
                    avail_w = min(rx, 1 - rx) * 2 * target_w * scale
                    avail_h = min(ry, 1 - ry) * 2 * target_h * scale
                else:
                    avail_w = target_w * scale
                    avail_h = target_h * scale
                angle = (
                    Entity._compute_optimal_angle(w, h, avail_w, avail_h)
                    if rotate
                    else Entity._compute_aspect_match_angle(w, h, avail_w, avail_h)
                )
                self.rotate(angle)

        if at is not None:
            # --- Position-aware mode ---
            rx, ry = RelCoord.coerce(at)
            if not (0.0 < rx < 1.0 and 0.0 < ry < 1.0):
                raise ValueError(f"at=({rx}, {ry}) must be inside the bounds (0.0-1.0 exclusive).")

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
                (e_min_x + e_max_x) / 2,
                (e_min_y + e_max_y) / 2,
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
        at: RelCoordLike | None = None,
        visual: bool = True,
        rotate: bool = False,
        match_aspect: bool = False,
    ) -> Entity:
        """
        Automatically scale and position entity to fit within its cell bounds.

        Convenience wrapper around :meth:`fit_within` that uses the
        containing cell as the target region.

        Args:
            scale:  Fraction of available space to fill (0.0-1.0).
                    1.0 = fill entire cell, 0.85 = use 85%.
            recenter:   If True, center entity in cell after scaling.
                        Ignored when ``at`` is provided.
            at: RelCoordLike within the cell as (rx, ry) fractions. Constrains
                fitting to the space available at that point so the entity
                doesn't overflow. (0.5, 0.5) uses the full cell (default).
            visual: If True (default), include stroke width in bounds
                    measurement so stroked shapes don't overflow.
            rotate: If True, auto-rotate to maximize cell coverage.
            match_aspect:   If True, rotate to match the cell's aspect ratio.
                            Mutually exclusive with ``rotate``.

        Returns:
            self, for method chaining

        Raises:
            ValueError: If entity has no cell, scale is out of range,
                        or both ``rotate`` and ``match_aspect`` are True.
            TypeError:  If ``at`` is a string (named anchors sit on cell
                        edges where available space is 0).

        Example:
            ```python
            ellipse = cell.add_ellipse(rx=2.0, ry=1.2, rotation=45)
            ellipse.fit_to_cell(0.85)  # Auto-constrain to 85% of cell
            dot = cell.add_dot(radius=0.8)
            dot.fit_to_cell(1.0, at=(0.25, 0.25))  # Fit in top-left quadrant
            ```
        """
        if self._cell is None:
            raise ValueError("Cannot fit to cell: entity has no cell")
        cell = self._cell
        return self.fit_within(
            (cell.x, cell.y, cell.x + cell.width, cell.y + cell.height),
            scale,
            recenter,
            at=at,
            visual=visual,
            rotate=rotate,
            match_aspect=match_aspect,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"
