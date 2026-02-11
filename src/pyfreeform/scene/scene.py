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
        self._width = width
        self._height = height
        self._background = Color(background) if background else None

        self._entities: list[Entity] = []
        self._connections: list[Connection] = []
        self._grids: list[Grid] = []
        self._primary_grid: Grid | None = None
        self._viewbox: tuple[float, float, float, float] | None = None
    
    # =========================================================================
    # FACTORY METHODS
    # =========================================================================
    
    @classmethod
    def from_image(
        cls,
        source: str | Path | Image,
        *,
        grid_size: int | None = 40,
        cell_size: int = 10,
        cell_ratio: float = 1.0,
        cell_width: float | None = None,
        cell_height: float | None = None,
        background: str | None = None,
    ) -> Scene:
        """
        Create a scene from an image file (one-liner for image-based art).

        This is the recommended way to create image-based artwork:

            scene = Scene.from_image("photo.jpg", grid_size=40)
            for cell in scene.grid:
                cell.add_dot(color=cell.color)
            scene.save("art.svg")

        Two modes:
            - **grid_size=N** (default): N columns, auto rows from aspect ratio.
              Scene size = cols * cell_size × rows * cell_size.
            - **grid_size=None**: Grid fits the image. Cols/rows derived from
              image dimensions ÷ cell size. Scene size ≈ image dimensions.

        Args:
            source: Path to image file, or an Image object.
            grid_size: Number of columns (rows auto-calculated from aspect ratio).
                       Pass None to derive grid from image dimensions.
            cell_size: Base size of each cell in pixels.
            cell_ratio: Width-to-height ratio (e.g., 2.0 for domino cells).
            cell_width: Explicit cell width (overrides cell_size and cell_ratio).
            cell_height: Explicit cell height (overrides cell_size).
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
            cell_ratio=cell_ratio,
            cell_width=cell_width,
            cell_height=cell_height,
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
        cell_width: float | None = None,
        cell_height: float | None = None,
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
            cell_size: Base size of each cell in pixels.
            cell_width: Explicit cell width (overrides cell_size).
            cell_height: Explicit cell height (overrides cell_size).
            background: Background color.

        Returns:
            Scene with empty grid, ready to iterate.
        """
        if rows is None:
            rows = cols

        grid = Grid(
            cols=cols,
            rows=rows,
            cell_size=cell_size,
            cell_width=cell_width,
            cell_height=cell_height,
        )
        
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
                "or add a grid with scene.add_grid(grid)."
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

    def add_connection(self, connection: Connection) -> Connection:
        """
        Add a connection to the scene.

        Connections created via ``entity.connect()`` are not automatically
        added to the scene — you must call this method to include them
        in the render.

        Args:
            connection: The Connection to add.

        Returns:
            The added connection (for chaining).

        Example:
            >>> conn = dot1.connect(dot2, shape=Line(), style=style)
            >>> scene.add_connection(conn)
        """
        self._connections.append(connection)
        return connection

    def add_grid(self, grid: Grid) -> Grid:
        """
        Add a grid to the scene.

        Grids created via ``Scene.from_image()`` or ``Scene.with_grid()``
        are added automatically. Use this only for manually-created grids.

        Args:
            grid: The Grid to add.

        Returns:
            The added grid (for chaining).
        """
        self._grids.append(grid)
        return grid

    def remove(self, entity: Entity) -> bool:
        """
        Remove an entity from the scene.

        Searches both direct entities and grid cells.

        Args:
            entity: The entity to remove.

        Returns:
            True if entity was found and removed.
        """
        if entity in self._entities:
            self._entities.remove(entity)
            entity.cell = None
            return True
        # Check grids
        for grid in self._grids:
            for cell in grid:
                if cell.remove(entity):
                    return True
        return False

    def remove_connection(self, connection: Connection) -> bool:
        """
        Remove a connection from the scene.

        Args:
            connection: The connection to remove.

        Returns:
            True if connection was found and removed.
        """
        if connection in self._connections:
            self._connections.remove(connection)
            connection.disconnect()
            return True
        return False

    def remove_grid(self, grid: Grid) -> bool:
        """
        Remove a grid from the scene.

        Args:
            grid: The grid to remove.

        Returns:
            True if grid was found and removed.
        """
        if grid in self._grids:
            self._grids.remove(grid)
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
    
    def _collect_markers(self, entities: list[Entity]) -> dict[str, str]:
        """Collect unique SVG marker definitions needed by all entities and connections."""
        markers: dict[str, str] = {}  # marker_id -> marker_svg

        for entity in entities:
            for mid, svg in entity.get_required_markers():
                markers[mid] = svg

        for connection in self._connections:
            for mid, svg in connection.get_required_markers():
                markers[mid] = svg

        return markers

    def _collect_path_defs(self, entities: list[Entity]) -> dict[str, str]:
        """Collect unique SVG path definitions needed by textPath entities."""
        paths: dict[str, str] = {}
        for entity in entities:
            for pid, svg in entity.get_required_paths():
                paths[pid] = svg
        return paths

    def to_svg(self) -> str:
        """
        Render the scene to an SVG string.

        Entities and connections are sorted by z_index before rendering.
        Lower z_index values render first (underneath).
        Higher z_index values render last (on top).

        Returns:
            Complete SVG document as string.
        """
        # Collect entities once (avoids rebuilding the list 3 times)
        all_entities = self.entities

        if self._viewbox is not None:
            vb_x, vb_y, vb_w, vb_h = self._viewbox
            # Scale display height to match the cropped aspect ratio
            display_h = vb_h * self._width / vb_w if vb_w > 0 else self._height
            svg_open = (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{self._width}" height="{display_h:.1f}" '
                f'viewBox="{vb_x} {vb_y} {vb_w} {vb_h}">'
            )
        else:
            svg_open = (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{self._width}" height="{self._height}" '
                f'viewBox="0 0 {self._width} {self._height}">'
            )

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            svg_open,
        ]

        # Definitions (markers for arrow caps, paths for textPath)
        markers = self._collect_markers(all_entities)
        path_defs = self._collect_path_defs(all_entities)
        if markers or path_defs:
            lines.append("  <defs>")
            for svg in markers.values():
                lines.append(f"    {svg}")
            for svg in path_defs.values():
                lines.append(f"    {svg}")
            lines.append("  </defs>")

        # Background
        if self._background:
            if self._viewbox is not None:
                vb_x, vb_y, vb_w, vb_h = self._viewbox
                lines.append(
                    f'  <rect x="{vb_x}" y="{vb_y}" '
                    f'width="{vb_w}" height="{vb_h}" '
                    f'fill="{self.background}" />'
                )
            else:
                lines.append(
                    f'  <rect width="100%" height="100%" fill="{self.background}" />'
                )

        # Collect all renderable objects with their z_index
        renderables: list[tuple[int, str]] = []

        # Add connections
        for connection in self._connections:
            renderables.append((connection.z_index, connection.to_svg()))

        # Add entities
        for entity in all_entities:
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
    
    def crop(self, padding: float = 0) -> Scene:
        """
        Crop the scene viewBox to fit the visual bounds of all content.

        Useful for transparent exports (icons, badges) where you don't
        want dead space around the artwork.

        Args:
            padding: Extra space around the content in pixels.

        Returns:
            self, for method chaining.

        Example::

            scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
            scene.background = None
            cell.add_dot(color="coral")
            scene.crop()       # Tight crop
            scene.crop(10)     # 10px breathing room
            scene.save("icon.svg")
        """
        all_entities = self.entities
        if not all_entities:
            return self

        bounds = [e.bounds(visual=True) for e in all_entities]
        min_x = min(b[0] for b in bounds) - padding
        min_y = min(b[1] for b in bounds) - padding
        max_x = max(b[2] for b in bounds) + padding
        max_y = max(b[3] for b in bounds) + padding

        self._viewbox = (min_x, min_y, max_x - min_x, max_y - min_y)
        return self

    def trim(
        self,
        top: float = 0,
        right: float = 0,
        bottom: float = 0,
        left: float = 0,
    ) -> Scene:
        """
        Remove pixels from one or more edges of the scene.

        Adjusts the viewBox so the specified number of pixels are clipped
        from each side.  Can be chained with :meth:`crop`.

        Args:
            top: Pixels to remove from the top edge.
            right: Pixels to remove from the right edge.
            bottom: Pixels to remove from the bottom edge.
            left: Pixels to remove from the left edge.

        Returns:
            self, for method chaining.

        Example::

            scene.trim(top=20)                # clip 20px from the top
            scene.trim(top=10, bottom=10)     # clip both edges
            scene.crop().trim(left=5, right=5)  # tight crop then shave sides
        """
        if self._viewbox is not None:
            vb_x, vb_y, vb_w, vb_h = self._viewbox
        else:
            vb_x, vb_y, vb_w, vb_h = 0.0, 0.0, float(self._width), float(self._height)

        vb_x += left
        vb_y += top
        vb_w -= left + right
        vb_h -= top + bottom

        self._viewbox = (vb_x, vb_y, vb_w, vb_h)
        return self

    def __repr__(self) -> str:
        bg_str = f", background={self.background!r}" if self.background else ""
        return (
            f"Scene({self._width}x{self._height}{bg_str}, "
            f"{len(self.entities)} entities, "
            f"{len(self._connections)} connections)"
        )
