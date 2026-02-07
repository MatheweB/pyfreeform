"""Entity - Base class for all drawable objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from weakref import WeakSet

from .point import Point

if TYPE_CHECKING:
    from .surface import Surface
    from .connection import Connection


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
        self._position = Point(x, y)
        self._cell: Surface | None = None
        self._connections: WeakSet[Connection] = WeakSet()
        self._data: dict[str, Any] = {}
        self._z_index = z_index
    
    @property
    def z_index(self) -> int:
        """Layer ordering (higher values render on top)."""
        return self._z_index
    
    @z_index.setter
    def z_index(self, value: int) -> None:
        self._z_index = value
    
    @property
    def position(self) -> Point:
        """Current position of the entity."""
        return self._position
    
    @position.setter
    def position(self, value: Point | tuple[float, float]) -> None:
        """Set position (accepts Point or tuple)."""
        if isinstance(value, tuple):
            value = Point(*value)
        self._position = value
    
    @property
    def x(self) -> float:
        """X coordinate of position."""
        return self._position.x
    
    @property
    def y(self) -> float:
        """Y coordinate of position."""
        return self._position.y
    
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
    
    def move_to(self, x: float | Point, y: float | None = None) -> Entity:
        """
        Move entity to absolute position.
        
        Args:
            x: X coordinate, or a Point.
            y: Y coordinate (required if x is not a Point).
        
        Returns:
            self, for method chaining.
        """
        if isinstance(x, Point):
            self._position = x
        elif y is not None:
            self._position = Point(x, y)
        else:
            raise ValueError("Must provide both x and y, or a Point")
        return self
    
    def move_by(self, dx: float = 0, dy: float = 0) -> Entity:
        """
        Move entity by a relative offset.
        
        Args:
            dx: Horizontal offset.
            dy: Vertical offset.
        
        Returns:
            self, for method chaining.
        """
        self._position = Point(self._position.x + dx, self._position.y + dy)
        return self
    
    def move_to_cell(self, cell: Cell, at: tuple[float, float] | str = "center") -> Entity:
        """
        Move entity to a position within a cell.
        
        Args:
            cell: The target cell.
            at: Position within cell - either a relative (rx, ry) tuple
                where (0,0) is top-left and (1,1) is bottom-right,
                or a named position like "center", "top_left", etc.
        
        Returns:
            self, for method chaining.
        """
        self._cell = cell
        self._position = cell.relative_to_absolute(at)
        return self
    
    # --- Connection methods ---
    
    def connect(
        self,
        other: Entity,
        style: Any | None = None,
        start_anchor: str = "center",
        end_anchor: str = "center",
    ) -> Connection:
        """
        Create a connection to another entity.

        Args:
            other: The entity to connect to.
            style: Visual style — ConnectionStyle object or dict with
                   "width", "color", "z_index" keys.
            start_anchor: Anchor name on this entity.
            end_anchor: Anchor name on the other entity.

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
        )
        return connection
    
    # --- Transform methods ---
    
    def rotate(self, angle: float, origin: Point | tuple[float, float] | None = None) -> Entity:
        """
        Rotate entity around a point.
        
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
            # Default: rotate around own position (no visible change for simple entities)
            return self
        
        if isinstance(origin, tuple):
            origin = Point(*origin)
        
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Rotate position around origin
        dx = self._position.x - origin.x
        dy = self._position.y - origin.y
        new_x = dx * cos_a - dy * sin_a + origin.x
        new_y = dx * sin_a + dy * cos_a + origin.y
        self._position = Point(new_x, new_y)
        
        return self
    
    def scale(self, factor: float, origin: Point | tuple[float, float] | None = None) -> Entity:
        """
        Scale entity around a point.
        
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
            origin = Point(*origin)
        
        new_x = origin.x + (self._position.x - origin.x) * factor
        new_y = origin.y + (self._position.y - origin.y) * factor
        self._position = Point(new_x, new_y)
        
        return self
    
    def translate(self, dx: float, dy: float) -> Entity:
        """
        Move entity by an offset (alias for move_by).
        
        Args:
            dx: Horizontal offset.
            dy: Vertical offset.
        
        Returns:
            self, for method chaining.
        """
        return self.move_by(dx, dy)

    def offset_from(self, anchor_name: str, dx: float = 0, dy: float = 0) -> Point:
        """
        Get a point offset from a named anchor.

        Sugar for ``entity.anchor(name) + Point(dx, dy)``.

        Args:
            anchor_name: Name of the anchor (e.g., "center", "top_left").
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.

        Returns:
            The offset point.
        """
        return self.anchor(anchor_name) + Point(dx, dy)

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

        self.move_by(tx - s_cx, ty - s_cy)
        return self

    # --- Abstract methods for subclasses ---
    
    @property
    @abstractmethod
    def anchor_names(self) -> list[str]:
        """List of available anchor names for this entity."""
        pass
    
    @abstractmethod
    def anchor(self, name: str) -> Point:
        """
        Get anchor point by name.
        
        Args:
            name: Anchor name (e.g., "center", "start", "end").
        
        Returns:
            The anchor position as a Point.
        
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
    def bounds(self) -> tuple[float, float, float, float]:
        """
        Get bounding box of this entity.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        pass

    def inner_bounds(self) -> tuple[float, float, float, float]:
        """
        Largest axis-aligned rectangle fully inside this entity.

        Override for non-rectangular shapes (e.g. circles, ellipses)
        to return the inscribed rectangle. Default: same as bounds().

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        return self.bounds()

    def fit_within(
        self,
        target: Entity | tuple[float, float, float, float],
        scale: float = 1.0,
        recenter: bool = True,
        *,
        at: tuple[float, float] | None = None,
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

        Returns:
            self, for method chaining.

        Example:
            >>> dot = cell.add_dot(radius=15, color="navy")
            >>> label = cell.add_text("0.5", color="white", font_size=50)
            >>> label.fit_within(dot)
            >>> # Position in top-left of a rect's inner bounds:
            >>> label.fit_within(rect, at=(0.25, 0.25))
        """
        if not (0.0 < scale <= 1.0):
            raise ValueError(f"scale must be between 0.0 and 1.0, got {scale}")

        # Resolve target bounds
        if isinstance(target, Entity):
            t_min_x, t_min_y, t_max_x, t_max_y = target.inner_bounds()
        else:
            t_min_x, t_min_y, t_max_x, t_max_y = target

        target_w = t_max_x - t_min_x
        target_h = t_max_y - t_min_y

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

            # Get entity's current bounding box
            e_min_x, e_min_y, e_max_x, e_max_y = self.bounds()
            entity_w = e_max_x - e_min_x
            entity_h = e_max_y - e_min_y

            # Scale factors
            scale_x = available_w / entity_w if entity_w > 0 else 1.0
            scale_y = available_h / entity_h if entity_h > 0 else 1.0
            factor = min(scale_x, scale_y, 1.0)

            entity_center = Point(
                (e_min_x + e_max_x) / 2, (e_min_y + e_max_y) / 2,
            )
            if factor < 0.999:
                self.scale(factor, origin=entity_center)

            # Move to target position
            new_bounds = self.bounds()
            new_cx = (new_bounds[0] + new_bounds[2]) / 2
            new_cy = (new_bounds[1] + new_bounds[3]) / 2
            self.move_by(target_x - new_cx, target_y - new_cy)

            return self

        # --- Default mode (at=None) ---
        target_cx = (t_min_x + t_max_x) / 2
        target_cy = (t_min_y + t_max_y) / 2

        # Get entity's current bounding box
        e_min_x, e_min_y, e_max_x, e_max_y = self.bounds()
        entity_w = e_max_x - e_min_x
        entity_h = e_max_y - e_min_y

        # Calculate available space
        available_w = target_w * scale
        available_h = target_h * scale

        # Scale factors
        scale_x = available_w / entity_w if entity_w > 0 else 1.0
        scale_y = available_h / entity_h if entity_h > 0 else 1.0
        factor = min(scale_x, scale_y, 1.0)  # Don't scale up

        # Scale around entity center if needed
        entity_cx = (e_min_x + e_max_x) / 2
        entity_cy = (e_min_y + e_max_y) / 2

        if factor < 0.999:
            self.scale(factor, origin=Point(entity_cx, entity_cy))

        # Recenter within target
        if recenter:
            new_bounds = self.bounds()
            new_cx = (new_bounds[0] + new_bounds[2]) / 2
            new_cy = (new_bounds[1] + new_bounds[3]) / 2
            self.move_by(target_cx - new_cx, target_cy - new_cy)

        return self

    def fit_to_cell(
        self,
        scale: float = 1.0,
        recenter: bool = True,
        *,
        at: tuple[float, float] | None = None,
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

        Returns:
            self, for method chaining

        Raises:
            ValueError: If entity has no cell or scale is out of range
            TypeError: If ``at`` is a string (named anchors sit on cell
                       edges where available space is 0)

        Example:
            >>> ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45)
            >>> ellipse.fit_to_cell(0.85)  # Auto-constrain to 85% of cell
            >>> dot = cell.add_dot(radius=200)
            >>> dot.fit_to_cell(1.0, at=(0.25, 0.25))  # Fit in top-left quadrant
        """
        # Validation
        if self._cell is None:
            raise ValueError("Cannot fit to cell: entity has no cell")

        if not (0.0 < scale <= 1.0):
            raise ValueError(f"scale must be between 0.0 and 1.0, got {scale}")

        cell = self._cell

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

            # Get entity's current bounding box
            e_min_x, e_min_y, e_max_x, e_max_y = self.bounds()
            entity_w = e_max_x - e_min_x
            entity_h = e_max_y - e_min_y

            # Calculate scale factors
            scale_x = available_w / entity_w if entity_w > 0 else 1.0
            scale_y = available_h / entity_h if entity_h > 0 else 1.0
            factor = min(scale_x, scale_y, 1.0)  # Don't scale up

            # Scale around entity center if needed
            entity_center = Point(
                (e_min_x + e_max_x) / 2,
                (e_min_y + e_max_y) / 2,
            )
            if factor < 0.999:
                self.scale(factor, origin=entity_center)

            # Move to target position
            new_bounds = self.bounds()
            new_cx = (new_bounds[0] + new_bounds[2]) / 2
            new_cy = (new_bounds[1] + new_bounds[3]) / 2
            self.move_by(target.x - new_cx, target.y - new_cy)

            return self

        # --- Default mode (at=None) ---

        # Get entity's current bounding box
        entity_min_x, entity_min_y, entity_max_x, entity_max_y = self.bounds()
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
        scale_factor = min(scale_x, scale_y, 1.0)  # Don't scale up, only down

        # If already fits, skip scaling (optimization)
        if scale_factor >= 0.999:  # Allow small floating point error
            if recenter:
                # Just recenter without scaling
                cell_center = Point(
                    cell_x + cell_width / 2,
                    cell_y + cell_height / 2
                )
                entity_center_x = (entity_min_x + entity_max_x) / 2
                entity_center_y = (entity_min_y + entity_max_y) / 2
                offset_x = cell_center.x - entity_center_x
                offset_y = cell_center.y - entity_center_y
                self.move_by(offset_x, offset_y)
            return self

        # Calculate entity's current center (before scaling)
        entity_center = Point(
            (entity_min_x + entity_max_x) / 2,
            (entity_min_y + entity_max_y) / 2
        )

        # Scale around entity's current center
        self.scale(scale_factor, origin=entity_center)

        # Recenter in cell if requested
        if recenter:
            # Get new bounds after scaling
            new_min_x, new_min_y, new_max_x, new_max_y = self.bounds()
            new_center_x = (new_min_x + new_max_x) / 2
            new_center_y = (new_min_y + new_max_y) / 2

            # Calculate offset to cell center
            cell_center_x = cell_x + cell_width / 2
            cell_center_y = cell_y + cell_height / 2

            offset_x = cell_center_x - new_center_x
            offset_y = cell_center_y - new_center_y

            self.move_by(offset_x, offset_y)

        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"
