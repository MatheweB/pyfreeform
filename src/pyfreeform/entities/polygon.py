"""Polygon - A closed polygon entity."""

from __future__ import annotations

import math
from ..color import Color
from ..core.entity import Entity
from ..core.point import Point


class Polygon(Entity):
    """
    A closed polygon defined by a list of vertices.
    
    Polygons can be filled, stroked, or both. Use helper functions
    in `pyfreeform.shapes` for common shapes like triangles, hexagons, stars.
    
    Attributes:
        vertices: List of Point objects defining the polygon
        fill: Fill color (or None for no fill)
        stroke: Stroke color (or None for no stroke)
        stroke_width: Stroke width
    
    Anchors:
        - "center": Centroid of the polygon
        - "v0", "v1", ...: Individual vertices
    
    Examples:
        >>> # Triangle from points
        >>> tri = Polygon([(0, 0), (50, 100), (100, 0)], fill="blue")
        
        >>> # In a cell (relative coordinates 0-1)
        >>> cell.add_polygon([(0.5, 0), (1, 1), (0, 1)], fill="red")
        
        >>> # Using shape helpers
        >>> from pyfreeform import shapes
        >>> cell.add_polygon(shapes.hexagon(), fill="purple")
    """
    
    def __init__(
        self,
        vertices: list[Point | tuple[float, float]],
        fill: str | tuple[int, int, int] | None = "black",
        stroke: str | tuple[int, int, int] | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
    ) -> None:
        """
        Create a polygon from vertices.

        Args:
            vertices: List of points (at least 3).
            fill: Fill color (None for transparent).
            stroke: Stroke color (None for no stroke).
            stroke_width: Stroke width in pixels.
            z_index: Layer ordering (higher = on top).
            opacity: Opacity for both fill and stroke (0.0-1.0).
            fill_opacity: Override opacity for fill only (None = use opacity).
            stroke_opacity: Override opacity for stroke only (None = use opacity).
        """
        if len(vertices) < 3:
            raise ValueError("Polygon requires at least 3 vertices")

        # Convert to Points
        self._vertices = [
            Point(*v) if isinstance(v, tuple) else v
            for v in vertices
        ]

        # Position is centroid
        centroid = self._calculate_centroid()
        super().__init__(centroid.x, centroid.y, z_index)

        self._fill = Color(fill) if fill else None
        self._stroke = Color(stroke) if stroke else None
        self.stroke_width = float(stroke_width)
        self.opacity = float(opacity)
        self.fill_opacity = fill_opacity
        self.stroke_opacity = stroke_opacity
    
    def _calculate_centroid(self) -> Point:
        """Calculate the centroid (center of mass) of the polygon."""
        x = sum(v.x for v in self._vertices) / len(self._vertices)
        y = sum(v.y for v in self._vertices) / len(self._vertices)
        return Point(x, y)
    
    @property
    def vertices(self) -> list[Point]:
        """The polygon vertices."""
        return list(self._vertices)
    
    @property
    def fill(self) -> str | None:
        """Fill color as string, or None."""
        return self._fill.to_hex() if self._fill else None
    
    @fill.setter
    def fill(self, value: str | tuple[int, int, int] | None) -> None:
        self._fill = Color(value) if value else None
    
    @property
    def stroke(self) -> str | None:
        """Stroke color as string, or None."""
        return self._stroke.to_hex() if self._stroke else None
    
    @stroke.setter
    def stroke(self, value: str | tuple[int, int, int] | None) -> None:
        self._stroke = Color(value) if value else None
    
    @property
    def anchor_names(self) -> list[str]:
        """Available anchors: center and vertices."""
        return ["center"] + [f"v{i}" for i in range(len(self._vertices))]
    
    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        if name == "center":
            return self._calculate_centroid()
        if name.startswith("v") and name[1:].isdigit():
            idx = int(name[1:])
            if 0 <= idx < len(self._vertices):
                return self._vertices[idx]
        raise ValueError(f"Polygon has no anchor '{name}'. Available: {self.anchor_names}")
    
    def rotate(self, angle: float, origin: Point | None = None) -> Polygon:
        """
        Rotate the polygon around a point.
        
        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: polygon centroid).
        
        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self._calculate_centroid()
        
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        new_vertices = []
        for v in self._vertices:
            # Translate to origin
            dx = v.x - origin.x
            dy = v.y - origin.y
            # Rotate
            new_x = dx * cos_a - dy * sin_a + origin.x
            new_y = dx * sin_a + dy * cos_a + origin.y
            new_vertices.append(Point(new_x, new_y))
        
        self._vertices = new_vertices
        # Update position to new centroid
        centroid = self._calculate_centroid()
        self._position = centroid
        return self
    
    def scale(self, factor: float, origin: Point | None = None) -> Polygon:
        """
        Scale the polygon around a point.
        
        Args:
            factor: Scale factor (1.0 = no change, 2.0 = double size).
            origin: Center of scaling (default: polygon centroid).
        
        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self._calculate_centroid()
        
        new_vertices = []
        for v in self._vertices:
            new_x = origin.x + (v.x - origin.x) * factor
            new_y = origin.y + (v.y - origin.y) * factor
            new_vertices.append(Point(new_x, new_y))
        
        self._vertices = new_vertices
        centroid = self._calculate_centroid()
        self._position = centroid
        return self
    
    def translate(self, dx: float, dy: float) -> Polygon:
        """
        Move the polygon by an offset.
        
        Args:
            dx: Horizontal offset.
            dy: Vertical offset.
        
        Returns:
            self, for method chaining.
        """
        self._vertices = [Point(v.x + dx, v.y + dy) for v in self._vertices]
        self._position = Point(self._position.x + dx, self._position.y + dy)
        return self
    
    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box."""
        min_x = min(v.x for v in self._vertices)
        min_y = min(v.y for v in self._vertices)
        max_x = max(v.x for v in self._vertices)
        max_y = max(v.y for v in self._vertices)
        return (min_x, min_y, max_x, max_y)
    
    def to_svg(self) -> str:
        """Render to SVG polygon element."""
        points_str = " ".join(f"{v.x},{v.y}" for v in self._vertices)
        
        parts = [f'<polygon points="{points_str}"']
        
        if self._fill:
            parts.append(f' fill="{self.fill}"')
        else:
            parts.append(' fill="none"')
        
        if self._stroke:
            parts.append(f' stroke="{self.stroke}" stroke-width="{self.stroke_width}"')

        # Opacity
        eff_fill_opacity = self.fill_opacity if self.fill_opacity is not None else self.opacity
        eff_stroke_opacity = self.stroke_opacity if self.stroke_opacity is not None else self.opacity
        if eff_fill_opacity < 1.0:
            parts.append(f' fill-opacity="{eff_fill_opacity}"')
        if eff_stroke_opacity < 1.0:
            parts.append(f' stroke-opacity="{eff_stroke_opacity}"')

        parts.append(' />')
        return ''.join(parts)
    
    def __repr__(self) -> str:
        return f"Polygon({len(self._vertices)} vertices, fill={self.fill!r})"


# =============================================================================
# Shape Helper Functions
# =============================================================================

def triangle(
    size: float = 1.0,
    center: tuple[float, float] = (0.5, 0.5),
) -> list[tuple[float, float]]:
    """
    Generate triangle vertices (equilateral, pointing up).
    
    Args:
        size: Scale factor (1.0 fills the cell).
        center: Center point in relative coordinates.
    
    Returns:
        List of (x, y) tuples for use with add_polygon().
    """
    cx, cy = center
    h = size * 0.5  # Half-height
    w = size * 0.5 * math.sqrt(3) / 2  # Half-width for equilateral
    
    return [
        (cx, cy - h),           # Top
        (cx + w, cy + h * 0.5), # Bottom right
        (cx - w, cy + h * 0.5), # Bottom left
    ]


def square(
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
) -> list[tuple[float, float]]:
    """Generate square vertices."""
    cx, cy = center
    h = size * 0.5
    return [
        (cx - h, cy - h),  # Top-left
        (cx + h, cy - h),  # Top-right
        (cx + h, cy + h),  # Bottom-right
        (cx - h, cy + h),  # Bottom-left
    ]


def diamond(
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
) -> list[tuple[float, float]]:
    """Generate diamond (rotated square) vertices."""
    cx, cy = center
    h = size * 0.5
    return [
        (cx, cy - h),  # Top
        (cx + h, cy),  # Right
        (cx, cy + h),  # Bottom
        (cx - h, cy),  # Left
    ]


def hexagon(
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
) -> list[tuple[float, float]]:
    """Generate regular hexagon vertices."""
    cx, cy = center
    r = size * 0.5
    vertices = []
    for i in range(6):
        angle = math.pi / 6 + i * math.pi / 3  # Start from top-right
        vertices.append((
            cx + r * math.cos(angle),
            cy + r * math.sin(angle),
        ))
    return vertices


def star(
    points: int = 5,
    size: float = 0.8,
    inner_ratio: float = 0.4,
    center: tuple[float, float] = (0.5, 0.5),
) -> list[tuple[float, float]]:
    """
    Generate star vertices.
    
    Args:
        points: Number of star points.
        size: Outer radius scale.
        inner_ratio: Inner radius as fraction of outer (0-1).
        center: Center point.
    """
    cx, cy = center
    outer_r = size * 0.5
    inner_r = outer_r * inner_ratio
    
    vertices = []
    for i in range(points * 2):
        angle = -math.pi / 2 + i * math.pi / points  # Start from top
        r = outer_r if i % 2 == 0 else inner_r
        vertices.append((
            cx + r * math.cos(angle),
            cy + r * math.sin(angle),
        ))
    return vertices


def regular_polygon(
    sides: int,
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
) -> list[tuple[float, float]]:
    """
    Generate regular polygon with N sides.
    
    Args:
        sides: Number of sides (3 = triangle, 4 = square, etc.)
        size: Scale factor.
        center: Center point.
    """
    if sides < 3:
        raise ValueError("Polygon must have at least 3 sides")
    
    cx, cy = center
    r = size * 0.5
    vertices = []
    for i in range(sides):
        angle = -math.pi / 2 + i * 2 * math.pi / sides  # Start from top
        vertices.append((
            cx + r * math.cos(angle),
            cy + r * math.sin(angle),
        ))
    return vertices


def squircle(
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
    n: float = 4,
    points: int = 32,
) -> list[tuple[float, float]]:
    """
    Generate a squircle (superellipse) - a shape between square and circle.
    
    The squircle is the "premium UI" shape used by iOS icons, modern logos,
    and anywhere you want something softer than a square but more structured
    than a circle.
    
    Args:
        size: Scale factor (1.0 fills the cell).
        center: Center point in relative coordinates.
        n: Squareness parameter:
           - n=2: Perfect circle
           - n=4: Classic squircle (iOS icon shape)
           - n=6+: Approaches a square with rounded corners
        points: Number of vertices (higher = smoother).
    
    Returns:
        List of vertices for use with add_polygon().
    
    Examples:
        >>> cell.add_polygon(shapes.squircle(), fill="blue")  # Classic squircle
        >>> cell.add_polygon(shapes.squircle(n=2), fill="red")  # Circle
        >>> cell.add_polygon(shapes.squircle(n=8), fill="green")  # Rounded square
    """
    cx, cy = center
    r = size * 0.5
    
    vertices = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        
        # Superellipse formula: |x/a|^n + |y/b|^n = 1
        # Solved for x,y given angle
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # Sign-preserving power function
        def sgn_pow(val, exp):
            return math.copysign(abs(val) ** exp, val)
        
        x = sgn_pow(cos_a, 2 / n) * r
        y = sgn_pow(sin_a, 2 / n) * r
        
        vertices.append((cx + x, cy + y))
    
    return vertices


def rounded_rect(
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
    corner_radius: float = 0.2,
    points_per_corner: int = 8,
) -> list[tuple[float, float]]:
    """
    Generate a rectangle with rounded corners.
    
    Args:
        size: Scale factor.
        center: Center point.
        corner_radius: Radius of corners as fraction of size (0-0.5).
        points_per_corner: Vertices per corner arc.
    
    Returns:
        List of vertices for use with add_polygon().
    """
    cx, cy = center
    half = size * 0.5
    r = min(corner_radius * size, half)  # Clamp radius
    
    vertices = []
    
    # Generate corners: top-right, bottom-right, bottom-left, top-left
    corners = [
        (cx + half - r, cy - half + r, -math.pi/2, 0),        # Top-right
        (cx + half - r, cy + half - r, 0, math.pi/2),         # Bottom-right
        (cx - half + r, cy + half - r, math.pi/2, math.pi),   # Bottom-left
        (cx - half + r, cy - half + r, math.pi, 3*math.pi/2), # Top-left
    ]
    
    for corner_x, corner_y, start_angle, end_angle in corners:
        for i in range(points_per_corner):
            t = i / points_per_corner
            angle = start_angle + t * (end_angle - start_angle)
            x = corner_x + r * math.cos(angle)
            y = corner_y + r * math.sin(angle)
            vertices.append((x, y))
    
    return vertices
