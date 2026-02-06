"""Entity - Base class for all drawable objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from weakref import WeakSet

from .point import Point

if TYPE_CHECKING:
    from ..grid.cell import Cell
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
        self._cell: Cell | None = None
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
    def cell(self) -> Cell | None:
        """The cell containing this entity, if any."""
        return self._cell
    
    @cell.setter
    def cell(self, value: Cell | None) -> None:
        """Set the containing cell."""
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

    def fit_to_cell(self, scale: float = 1.0, recenter: bool = True) -> Entity:
        """
        Automatically scale and position entity to fit within its cell bounds.

        Works for any entity type and handles rotation automatically by using
        the entity's actual bounding box.

        Args:
            scale: Percentage of cell to fill (0.0-1.0).
                   1.0 = fill entire cell, 0.85 = use 85% of cell.
            recenter: If True, center entity in cell after scaling.
                      If False, maintain current position.

        Returns:
            self, for method chaining

        Raises:
            ValueError: If entity has no cell or scale is out of range

        Example:
            >>> ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45)
            >>> ellipse.fit_to_cell(0.85)  # Auto-constrain to 85% of cell
        """
        # Validation
        if self._cell is None:
            raise ValueError("Cannot fit to cell: entity has no cell")

        if not (0.0 < scale <= 1.0):
            raise ValueError(f"scale must be between 0.0 and 1.0, got {scale}")

        # Get entity's current bounding box
        entity_min_x, entity_min_y, entity_max_x, entity_max_y = self.bounds()
        entity_width = entity_max_x - entity_min_x
        entity_height = entity_max_y - entity_min_y

        # Get cell bounds
        cell_x = self._cell.x
        cell_y = self._cell.y
        cell_width = self._cell.width
        cell_height = self._cell.height

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
