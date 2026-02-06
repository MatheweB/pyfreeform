"""Scene - The main container for entities and rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, TYPE_CHECKING

from ..color import Color
from ..core.connection import Connection
from ..core.entity import Entity
from ..core.surface import Surface
from ..grid.grid import Grid

if TYPE_CHECKING:
    from ..image import Image


class Scene(Surface):
    """
    The main container for all drawable objects in PyFreeform.
    
    A Scene holds entities, grids, and connections. It manages rendering
    to SVG and provides the primary API for creating artwork.
    
    Creating Scenes:
        # From an image (recommended for image-based art)
        scene = Scene.from_image("photo.jpg", grid_size=40)
        
        # With an empty grid
        scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
        
        # Manual (for non-grid art)
        scene = Scene(800, 600, background="#fafafa")
    
    Working with the Grid:
        >>> scene = Scene.from_image("photo.jpg", grid_size=40)
        >>> for cell in scene.grid:
        ...     cell.add_dot(color=cell.color)
        >>> scene.save("art.svg")
    
    Attributes:
        width: Scene width in pixels
        height: Scene height in pixels
        background: Background color (or None for transparent)
        grid: The primary grid (if created with from_image or with_grid)
    """
    
    def __init__(
        self,
        width: int,
        height: int,
        background: str | tuple[int, int, int] | None = None,
    ) -> None:
        """
        Create a new empty scene.
        
        For image-based art, use Scene.from_image() instead.
        For grid-based art, use Scene.with_grid() instead.
        
        Args:
            width: Scene width in pixels.
            height: Scene height in pixels.
            background: Background color (None for transparent).
        """
        self._x = 0.0
        self._y = 0.0
        self._width = int(width)
        self._height = int(height)
        self._background = Color(background) if background else None

        self._entities: list[Entity] = []
        self._connections: list[Connection] = []
        self._grids: list[Grid] = []
        self._primary_grid: Grid | None = None
    
    # =========================================================================
    # FACTORY METHODS
    # =========================================================================
    
    @classmethod
    def from_image(
        cls,
        source: str | Path | Image,
        *,
        grid_size: int = 40,
        cell_size: int = 10,
        background: str | None = None,
    ) -> Scene:
        """
        Create a scene from an image file (one-liner for image-based art).
        
        This is the recommended way to create image-based artwork:
        
            scene = Scene.from_image("photo.jpg", grid_size=40)
            for cell in scene.grid:
                cell.add_dot(color=cell.color)
            scene.save("art.svg")
        
        Args:
            source: Path to image file, or an Image object.
            grid_size: Number of columns (rows auto-calculated from aspect ratio).
            cell_size: Size of each cell in pixels.
            background: Background color (defaults to dark blue).
        
        Returns:
            Scene with grid loaded from image, ready to iterate.
        
        The grid's cells will have typed properties:
            - cell.color: Hex color string
            - cell.brightness: Float 0.0-1.0
            - cell.rgb: Tuple (r, g, b)
            - cell.alpha: Float 0.0-1.0
        """
        from ..image import Image as ImageClass
        
        # Load image if path provided
        if isinstance(source, (str, Path)):
            image = ImageClass.load(source)
        else:
            image = source
        
        # Create grid from image
        grid = Grid.from_image(
            image,
            cols=grid_size,
            cell_size=cell_size,
            load_layers=True,
        )
        
        # Set default background if not specified
        if background is None:
            background = "#1a1a2e"  # Midnight blue
        
        # Create scene sized to grid
        scene = cls(
            width=int(grid.pixel_width),
            height=int(grid.pixel_height),
            background=background,
        )
        
        # Add grid and mark as primary
        scene._grids.append(grid)
        scene._primary_grid = grid
        
        return scene
    
    @classmethod
    def with_grid(
        cls,
        *,
        cols: int = 30,
        rows: int | None = None,
        cell_size: int = 10,
        background: str | None = None,
    ) -> Scene:
        """
        Create a scene with an empty grid (for non-image-based art).
        
            scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
            for cell in scene.grid:
                cell.add_dot(color="coral")
            scene.save("art.svg")
        
        Args:
            cols: Number of columns.
            rows: Number of rows (defaults to same as cols for square grid).
            cell_size: Size of each cell in pixels.
            background: Background color.
        
        Returns:
            Scene with empty grid, ready to iterate.
        """
        if rows is None:
            rows = cols
        
        grid = Grid(cols=cols, rows=rows, cell_size=cell_size)
        
        # Set default background if not specified
        if background is None:
            background = "#1a1a2e"
        
        scene = cls(
            width=int(grid.pixel_width),
            height=int(grid.pixel_height),
            background=background,
        )
        
        scene._grids.append(grid)
        scene._primary_grid = grid
        
        return scene
    
    # =========================================================================
    # PROPERTIES
    # =========================================================================
    
    @property
    def width(self) -> int:
        """Scene width in pixels."""
        return self._width
    
    @property
    def height(self) -> int:
        """Scene height in pixels."""
        return self._height
    
    @property
    def background(self) -> str | None:
        """Background color as string, or None."""
        return self._background.to_hex() if self._background else None
    
    @background.setter
    def background(self, value: str | tuple[int, int, int] | None) -> None:
        self._background = Color(value) if value else None
    
    @property
    def grid(self) -> Grid:
        """
        The primary grid (created by from_image or with_grid).
        
        Raises:
            ValueError: If scene was created without a grid.
        
        Example:
            >>> for cell in scene.grid:
            ...     cell.add_dot(color=cell.color)
        """
        if self._primary_grid is None:
            if self._grids:
                return self._grids[0]
            raise ValueError(
                "Scene has no grid. Create with Scene.from_image() or Scene.with_grid(), "
                "or add a grid with scene.add(grid)."
            )
        return self._primary_grid
    
    @property
    def entities(self) -> list[Entity]:
        """All entities (including those in grids)."""
        result = list(self._entities)
        for grid in self._grids:
            result.extend(grid.all_entities())
        return result
    
    @property
    def connections(self) -> list[Connection]:
        """All connections."""
        return list(self._connections)
    
    @property
    def grids(self) -> list[Grid]:
        """All grids in the scene."""
        return list(self._grids)
    
    # --- Adding objects ---
    
    def add(self, *objects: Entity | Connection | Grid) -> Entity | Connection | Grid:
        """
        Add entities, connections, or grids to the scene.
        
        Args:
            *objects: One or more objects to add.
        
        Returns:
            The last added object (for chaining with single adds).
        
        Examples:
            >>> dot = scene.add(Dot(100, 100))
            >>> scene.add(Dot(200, 200), Dot(300, 300))
        """
        last = None
        for obj in objects:
            if isinstance(obj, Grid):
                self._grids.append(obj)
                last = obj
            elif isinstance(obj, Connection):
                self._connections.append(obj)
                last = obj
            elif isinstance(obj, Entity):
                self._entities.append(obj)
                last = obj
            else:
                raise TypeError(f"Cannot add {type(obj).__name__} to scene")
        return last
    
    def remove(self, obj: Entity | Connection | Grid) -> bool:
        """
        Remove an object from the scene.
        
        Args:
            obj: The object to remove.
        
        Returns:
            True if object was found and removed.
        """
        if isinstance(obj, Grid):
            if obj in self._grids:
                self._grids.remove(obj)
                return True
        elif isinstance(obj, Connection):
            if obj in self._connections:
                self._connections.remove(obj)
                obj.disconnect()
                return True
        elif isinstance(obj, Entity):
            if obj in self._entities:
                self._entities.remove(obj)
                return True
            # Check grids
            for grid in self._grids:
                for cell in grid:
                    if cell.remove(obj):
                        return True
        return False
    
    def clear(self) -> None:
        """Remove all objects from the scene."""
        self._entities.clear()
        self._connections.clear()
        for grid in self._grids:
            grid.clear()
        self._grids.clear()
    
    # --- Iteration ---
    
    def __iter__(self) -> Iterator[Entity]:
        """Iterate over all entities."""
        return iter(self.entities)
    
    def __len__(self) -> int:
        """Total number of entities."""
        return len(self.entities)
    
    # --- Rendering ---
    
    def _collect_markers(self) -> dict[str, str]:
        """Collect unique SVG marker definitions needed by all entities and connections."""
        markers: dict[str, str] = {}  # marker_id -> marker_svg

        for entity in self.entities:
            if hasattr(entity, "get_required_markers"):
                for mid, svg in entity.get_required_markers():
                    markers[mid] = svg

        for connection in self._connections:
            if hasattr(connection, "get_required_markers"):
                for mid, svg in connection.get_required_markers():
                    markers[mid] = svg

        return markers

    def to_svg(self) -> str:
        """
        Render the scene to an SVG string.

        Entities and connections are sorted by z_index before rendering.
        Lower z_index values render first (underneath).
        Higher z_index values render last (on top).

        Returns:
            Complete SVG document as string.
        """
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{self._width}" height="{self._height}" '
            f'viewBox="0 0 {self._width} {self._height}">',
        ]

        # Marker definitions (for arrow caps, etc.)
        markers = self._collect_markers()
        if markers:
            lines.append("  <defs>")
            for svg in markers.values():
                lines.append(f"    {svg}")
            lines.append("  </defs>")

        # Background
        if self._background:
            lines.append(
                f'  <rect width="100%" height="100%" fill="{self.background}" />'
            )

        # Collect all renderable objects with their z_index
        renderables: list[tuple[int, str]] = []

        # Add connections
        for connection in self._connections:
            renderables.append((connection.z_index, connection.to_svg()))

        # Add entities
        for entity in self.entities:
            renderables.append((entity.z_index, entity.to_svg()))

        # Sort by z_index (stable sort preserves add-order for same z_index)
        renderables.sort(key=lambda x: x[0])

        # Render in sorted order
        for _, svg in renderables:
            lines.append(f"  {svg}")

        lines.append("</svg>")
        return "\n".join(lines)
    
    def save(self, path: str | Path) -> None:
        """
        Save the scene to an SVG file.
        
        Args:
            path: File path (will add .svg extension if missing).
        """
        path = Path(path)
        if path.suffix.lower() != ".svg":
            path = path.with_suffix(".svg")
        
        svg_content = self.to_svg()
        path.write_text(svg_content, encoding="utf-8")
    
    def __repr__(self) -> str:
        bg_str = f", background={self.background!r}" if self.background else ""
        return (
            f"Scene({self._width}x{self._height}{bg_str}, "
            f"{len(self.entities)} entities, "
            f"{len(self._connections)} connections)"
        )
