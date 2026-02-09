"""Polygon - A closed polygon entity."""

from __future__ import annotations

import math
from typing import Union
from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike

# A vertex can be a static coordinate, an Entity (uses its position),
# or (Entity, anchor_name) to track a specific anchor.
VertexInput = Union[CoordLike, Entity, tuple[Entity, str]]


class Polygon(Entity):
    """
    A closed polygon defined by a list of vertices.

    Vertices can be static coordinates or entity references. Entity-reference
    vertices track the referenced entity's position at render time — when
    the entity moves, the polygon deforms automatically.

    Polygons can be filled, stroked, or both. Use classmethods like
    ``Polygon.star()``, ``Polygon.hexagon()`` for common shapes.

    Attributes:
        vertices: List of resolved Coord objects (computed at access time)
        fill: Fill color (or None for no fill)
        stroke: Stroke color (or None for no stroke)
        stroke_width: Stroke width

    Anchors:
        - "center": Centroid of the polygon
        - "v0", "v1", ...: Individual vertices (resolved from specs)

    Examples:
        >>> # Triangle from static points
        >>> tri = Polygon([(0, 0), (50, 100), (100, 0)], fill="blue")

        >>> # Entity-reference vertices (reactive)
        >>> a, b, c = Point(0, 0), Point(100, 0), Point(50, 80)
        >>> tri = Polygon([a, b, c], fill="coral")
        >>> b.move_to(120, 30)  # triangle deforms automatically

        >>> # Mixed static and entity-reference
        >>> tri = Polygon([(0, 0), dot, (rect, "top_right")], fill="teal")

        >>> # In a cell (relative coordinates 0-1)
        >>> cell.add_polygon([(0.5, 0), (1, 1), (0, 1)], fill="red")

        >>> # Using shape classmethods
        >>> cell.add_polygon(Polygon.hexagon(), fill="purple")
    """

    def __init__(
        self,
        vertices: list[VertexInput],
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
            vertices: List of vertex specs (at least 3). Each can be:
                - ``(x, y)`` tuple or ``Coord`` — static vertex
                - ``Entity`` — tracks the entity's position
                - ``(Entity, "anchor_name")`` — tracks a specific anchor
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

        # Normalize vertex specs:
        #   tuple[float, float] → Coord (static)
        #   Entity → kept as-is (reactive)
        #   (Entity, str) → kept as-is (reactive + anchor)
        self._vertex_specs: list[Coord | Entity | tuple[Entity, str]] = []
        for v in vertices:
            if isinstance(v, Entity):
                self._vertex_specs.append(v)
            elif isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], Entity):
                self._vertex_specs.append(v)  # (Entity, anchor_name)
            else:
                self._vertex_specs.append(Coord(*v))  # CoordLike → Coord

        # Position is centroid
        centroid = self._calculate_centroid()
        super().__init__(centroid.x, centroid.y, z_index)

        self._fill = Color(fill) if fill else None
        self._stroke = Color(stroke) if stroke else None
        self.stroke_width = float(stroke_width)
        self.opacity = float(opacity)
        self.fill_opacity = fill_opacity
        self.stroke_opacity = stroke_opacity

    def _resolve_vertex(self, spec: Coord | Entity | tuple[Entity, str]) -> Coord:
        """Resolve a single vertex spec to a Coord."""
        if isinstance(spec, Coord):
            return spec
        if isinstance(spec, Entity):
            return spec.position
        # (Entity, anchor_name)
        return spec[0].anchor(spec[1])

    def _calculate_centroid(self) -> Coord:
        """Calculate the centroid (center of mass) of the polygon."""
        resolved = [self._resolve_vertex(s) for s in self._vertex_specs]
        x = sum(v.x for v in resolved) / len(resolved)
        y = sum(v.y for v in resolved) / len(resolved)
        return Coord(x, y)

    @property
    def vertices(self) -> list[Coord]:
        """The polygon vertices (resolved from specs at access time)."""
        return [self._resolve_vertex(s) for s in self._vertex_specs]

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
        return ["center"] + [f"v{i}" for i in range(len(self._vertex_specs))]

    def anchor(self, name: str = "center") -> Coord:
        """Get anchor point by name (resolved from specs)."""
        if name == "center":
            return self._calculate_centroid()
        if name.startswith("v") and name[1:].isdigit():
            idx = int(name[1:])
            if 0 <= idx < len(self._vertex_specs):
                return self._resolve_vertex(self._vertex_specs[idx])
        raise ValueError(f"Polygon has no anchor '{name}'. Available: {self.anchor_names}")
    
    def rotate(self, angle: float, origin: Coord | None = None) -> Polygon:
        """
        Rotate the polygon around a point.

        Only static (Coord) vertices are rotated. Entity-reference vertices
        follow their entity and are not affected by polygon transforms.

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

        new_specs = []
        for spec in self._vertex_specs:
            if isinstance(spec, Coord):
                dx = spec.x - origin.x
                dy = spec.y - origin.y
                new_x = dx * cos_a - dy * sin_a + origin.x
                new_y = dx * sin_a + dy * cos_a + origin.y
                new_specs.append(Coord(new_x, new_y))
            else:
                new_specs.append(spec)  # Entity refs untouched

        self._vertex_specs = new_specs
        centroid = self._calculate_centroid()
        self._position = centroid
        return self
    
    def scale(self, factor: float, origin: Coord | None = None) -> Polygon:
        """
        Scale the polygon around a point.

        Only static (Coord) vertices are scaled. Entity-reference vertices
        follow their entity and are not affected by polygon transforms.

        Args:
            factor: Scale factor (1.0 = no change, 2.0 = double size).
            origin: Center of scaling (default: polygon centroid).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self._calculate_centroid()

        new_specs = []
        for spec in self._vertex_specs:
            if isinstance(spec, Coord):
                new_x = origin.x + (spec.x - origin.x) * factor
                new_y = origin.y + (spec.y - origin.y) * factor
                new_specs.append(Coord(new_x, new_y))
            else:
                new_specs.append(spec)  # Entity refs untouched

        self._vertex_specs = new_specs
        centroid = self._calculate_centroid()
        self._position = centroid
        return self
    
    def move_by(self, dx: float = 0, dy: float = 0) -> Polygon:
        """
        Move the polygon by an offset, updating static vertices.

        Only static (Coord) vertices are translated. Entity-reference vertices
        follow their entity and are not affected by polygon transforms.

        Args:
            dx: Horizontal offset.
            dy: Vertical offset.

        Returns:
            self, for method chaining.
        """
        new_specs = []
        for spec in self._vertex_specs:
            if isinstance(spec, Coord):
                new_specs.append(Coord(spec.x + dx, spec.y + dy))
            else:
                new_specs.append(spec)  # Entity refs untouched
        self._vertex_specs = new_specs
        self._position = Coord(self._position.x + dx, self._position.y + dy)
        return self

    def translate(self, dx: float, dy: float) -> Polygon:
        """
        Move the polygon by an offset (alias for move_by).

        Args:
            dx: Horizontal offset.
            dy: Vertical offset.

        Returns:
            self, for method chaining.
        """
        return self.move_by(dx, dy)
    
    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box (resolved from specs)."""
        verts = self.vertices
        min_x = min(v.x for v in verts)
        min_y = min(v.y for v in verts)
        max_x = max(v.x for v in verts)
        max_y = max(v.y for v in verts)
        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        """Render to SVG polygon element."""
        points_str = " ".join(f"{v.x},{v.y}" for v in self.vertices)
        
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

    # ---- Shape classmethods ------------------------------------------------

    @classmethod
    def triangle(
        cls,
        size: float = 1.0,
        center: tuple[float, float] = (0.5, 0.5),
    ) -> list[tuple[float, float]]:
        """Generate equilateral triangle vertices (pointing up)."""
        return _triangle(size, center)

    @classmethod
    def square(
        cls,
        size: float = 0.8,
        center: tuple[float, float] = (0.5, 0.5),
    ) -> list[tuple[float, float]]:
        """Generate square vertices."""
        return _square(size, center)

    @classmethod
    def diamond(
        cls,
        size: float = 0.8,
        center: tuple[float, float] = (0.5, 0.5),
    ) -> list[tuple[float, float]]:
        """Generate diamond (rotated square) vertices."""
        return _diamond(size, center)

    @classmethod
    def hexagon(
        cls,
        size: float = 0.8,
        center: tuple[float, float] = (0.5, 0.5),
    ) -> list[tuple[float, float]]:
        """Generate regular hexagon vertices."""
        return _hexagon(size, center)

    @classmethod
    def star(
        cls,
        points: int = 5,
        size: float = 0.8,
        inner_ratio: float = 0.4,
        center: tuple[float, float] = (0.5, 0.5),
    ) -> list[tuple[float, float]]:
        """Generate star vertices."""
        return _star(points, size, inner_ratio, center)

    @classmethod
    def regular_polygon(
        cls,
        sides: int,
        size: float = 0.8,
        center: tuple[float, float] = (0.5, 0.5),
    ) -> list[tuple[float, float]]:
        """Generate regular polygon with N sides."""
        return _regular_polygon(sides, size, center)

    @classmethod
    def squircle(
        cls,
        size: float = 0.8,
        center: tuple[float, float] = (0.5, 0.5),
        n: float = 4,
        points: int = 32,
    ) -> list[tuple[float, float]]:
        """Generate squircle (superellipse) vertices."""
        return _squircle(size, center, n, points)

    @classmethod
    def rounded_rect(
        cls,
        size: float = 0.8,
        center: tuple[float, float] = (0.5, 0.5),
        corner_radius: float = 0.2,
        points_per_corner: int = 8,
    ) -> list[tuple[float, float]]:
        """Generate rectangle with rounded corners vertices."""
        return _rounded_rect(size, center, corner_radius, points_per_corner)


# =============================================================================
# Shape Helper Functions (internal)
# =============================================================================

def _triangle(
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


def _square(
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


def _diamond(
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


def _hexagon(
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


def _star(
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


def _regular_polygon(
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


def _squircle(
    size: float = 0.8,
    center: tuple[float, float] = (0.5, 0.5),
    n: float = 4,
    points: int = 32,
) -> list[tuple[float, float]]:
    """
    Generate a squircle (superellipse) - a shape between square and circle.

    Args:
        size: Scale factor (1.0 fills the cell).
        center: Center point in relative coordinates.
        n: Squareness parameter (2=circle, 4=squircle, 6+=rounded square).
        points: Number of vertices (higher = smoother).
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


def _rounded_rect(
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
