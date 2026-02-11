"""EntityGroup - A reusable group of entities that behaves as a single entity."""

from __future__ import annotations

import math

from ..core.coord import Coord, CoordLike
from ..core.entity import Entity


class EntityGroup(Entity):
    """
    A reusable group of entities that behaves as a single entity.

    Define child entities relative to (0, 0). When placed, an SVG ``<g>``
    transform handles positioning and scaling — children are never mutated.

    Works with all placement methods:
    - ``scene.add(group)`` — add to scene at group's position
    - ``cell.add(group)`` — center in cell
    - ``group.fit_to_cell()`` — auto-scale to fit cell bounds

    For reuse, wrap creation in a factory function — each call returns
    a new independent instance.

    Example::

        from pyfreeform import EntityGroup, Dot
        import math

        def make_flower(color="coral", petal_color="gold"):
            g = EntityGroup()
            g.add(Dot(0, 0, radius=10, color=color))
            for i in range(8):
                angle = i * (2 * math.pi / 8)
                x = 15 * math.cos(angle)
                y = 15 * math.sin(angle)
                g.add(Dot(x, y, radius=6, color=petal_color))
            return g

        cell.add(make_flower())
        cell2.add(make_flower(color="blue"))
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z_index: int = 0,
        opacity: float = 1.0,
    ) -> None:
        """
        Create an EntityGroup.

        Args:
            x: Initial x position (default 0).
            y: Initial y position (default 0).
            z_index: Layer ordering (higher = on top).
            opacity: Group-level opacity (0.0 transparent to 1.0 opaque).
        """
        super().__init__(x, y, z_index)
        self._children: list[Entity] = []
        self._scale: float = 1.0
        self._rotation: float = 0.0  # degrees
        self.opacity: float = float(opacity)

    def add(self, entity: Entity) -> Entity:
        """
        Add a child entity to this group.

        The entity's position should be relative to (0, 0) — the group's
        local origin. When the group is placed, all children are offset
        by the group's position via SVG transform.

        Args:
            entity: The entity to add.

        Returns:
            The added entity (for chaining or reference).
        """
        self._children.append(entity)
        return entity

    @property
    def children(self) -> list[Entity]:
        """The child entities in this group (copy)."""
        return list(self._children)

    # =========================================================================
    # ABSTRACT METHOD IMPLEMENTATIONS
    # =========================================================================

    @property
    def anchor_names(self) -> list[str]:
        """Available anchor names."""
        return ["center"]

    def anchor(self, name: str) -> Coord:
        """
        Get anchor point by name.

        Args:
            name: Anchor name (only "center" is supported).

        Returns:
            The anchor position.

        Raises:
            ValueError: If name is not "center".
        """
        if name == "center":
            b = self.bounds()
            return Coord((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        raise ValueError(f"EntityGroup has no anchor '{name}'. Available: {self.anchor_names}")

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Bounding box in absolute coordinates.

        Delegates to ``rotated_bounds(0)`` which recursively computes
        exact analytical bounds for every child under the group's
        rotation and scale.
        """
        return self.rotated_bounds(0, visual=visual)

    def rotated_bounds(
        self,
        angle: float,
        *,
        visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this group rotated by *angle* degrees around origin.

        Each child computes its own tight AABB at the combined rotation
        ``self._rotation + angle``.  The group applies scale and position
        offset on top.  No sampling, no duck-typing — every entity type
        provides its own analytical formula.
        """
        if not self._children:
            if angle == 0:
                return (self.x, self.y, self.x, self.y)
            rad = math.radians(angle)
            cos_a, sin_a = math.cos(rad), math.sin(rad)
            rx = self.x * cos_a - self.y * sin_a
            ry = self.x * sin_a + self.y * cos_a
            return (rx, ry, rx, ry)

        combined = self._rotation + angle
        s = self._scale

        # Group position after outer rotation
        if angle == 0:
            ox, oy = self.x, self.y
        else:
            rad = math.radians(angle)
            cos_a, sin_a = math.cos(rad), math.sin(rad)
            ox = self.x * cos_a - self.y * sin_a
            oy = self.x * sin_a + self.y * cos_a

        g_min_x = math.inf
        g_min_y = math.inf
        g_max_x = -math.inf
        g_max_y = -math.inf

        for child in self._children:
            cb = child.rotated_bounds(combined, visual=visual)
            # Apply scale then offset
            sx0 = cb[0] * s + ox
            sy0 = cb[1] * s + oy
            sx1 = cb[2] * s + ox
            sy1 = cb[3] * s + oy
            if sx0 < g_min_x:
                g_min_x = sx0
            if sy0 < g_min_y:
                g_min_y = sy0
            if sx1 > g_max_x:
                g_max_x = sx1
            if sy1 > g_max_y:
                g_max_y = sy1

        return (g_min_x, g_min_y, g_max_x, g_max_y)

    def to_svg(self) -> str:
        """
        Render to SVG ``<g>`` element with transform.

        Children are rendered inside a ``<g>`` wrapper that applies
        translate and scale transforms. Children are sorted by z_index.

        Returns:
            SVG string, or empty string if no children.
        """
        if not self._children:
            return ""

        transforms = [f"translate({self.x}, {self.y})"]
        if self._rotation != 0:
            transforms.append(f"rotate({self._rotation})")
        if self._scale != 1.0:
            transforms.append(f"scale({self._scale})")
        transform_str = " ".join(transforms)

        sorted_children = sorted(self._children, key=lambda e: e.z_index)
        opacity_attr = f' opacity="{self.opacity}"' if self.opacity < 1.0 else ""
        parts = [f'<g transform="{transform_str}"{opacity_attr}>']
        parts.extend(f"  {child.to_svg()}" for child in sorted_children)
        parts.append("</g>")
        return "\n".join(parts)

    # =========================================================================
    # TRANSFORM OVERRIDES
    # =========================================================================

    def rotate(
        self,
        angle: float,
        origin: CoordLike | None = None,
    ) -> EntityGroup:
        """
        Rotate the group.

        Accumulates an internal rotation angle used by the SVG transform.
        If origin is provided, also orbits the group's position around
        that point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation in absolute coordinates.
                    If None, rotates in place (children rotate around
                    the group's local origin).

        Returns:
            self, for method chaining.
        """
        self._rotation += angle
        if origin is not None:
            super().rotate(angle, origin)
        return self

    def scale(
        self,
        factor: float,
        origin: CoordLike | None = None,
    ) -> EntityGroup:
        """
        Scale the group.

        Accumulates an internal scale factor used by the SVG transform.
        If origin is provided, also adjusts the group's position so that
        the origin point remains fixed (used by fit_to_cell).

        Args:
            factor: Scale factor (0.5 = half size, 2.0 = double).
            origin: Center of scaling in absolute coordinates.

        Returns:
            self, for method chaining.
        """
        self._scale *= factor
        super().scale(factor, origin)
        return self

    @property
    def rotation(self) -> float:
        """Current rotation angle in degrees."""
        return self._rotation

    @property
    def scale_factor(self) -> float:
        """Current cumulative scale factor."""
        return self._scale

    # =========================================================================
    # DEFS COLLECTION (forward to children)
    # =========================================================================

    def get_required_markers(self) -> list[tuple[str, str]]:
        """Collect SVG marker definitions from all children."""
        result: list[tuple[str, str]] = []
        for child in self._children:
            result.extend(child.get_required_markers())
        return result

    def get_required_paths(self) -> list[tuple[str, str]]:
        """Collect SVG path definitions from all children."""
        result: list[tuple[str, str]] = []
        for child in self._children:
            result.extend(child.get_required_paths())
        return result

    def __repr__(self) -> str:
        n = len(self._children)
        extras = []
        if self._scale != 1.0:
            extras.append(f"scale={self._scale:.2f}")
        if self._rotation != 0:
            extras.append(f"rotation={self._rotation:.1f}")
        if self.opacity < 1.0:
            extras.append(f"opacity={self.opacity:.2f}")
        extra_str = f", {', '.join(extras)}" if extras else ""
        return f"EntityGroup({n} children, pos=({self.x:.1f}, {self.y:.1f}){extra_str})"
