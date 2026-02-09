"""EntityGroup - A reusable group of entities that behaves as a single entity."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..core.entity import Entity
from ..core.coord import Coord, CoordLike

if TYPE_CHECKING:
    pass


class EntityGroup(Entity):
    """
    A reusable group of entities that behaves as a single entity.

    Define child entities relative to (0, 0). When placed, an SVG ``<g>``
    transform handles positioning and scaling — children are never mutated.

    Works with all placement methods:
    - ``scene.add(group)`` — add to scene at group's position
    - ``cell.place(group)`` — center in cell
    - ``cell.add_entity(group)`` — same as place, add_* naming
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

        cell.place(make_flower())
        cell2.place(make_flower(color="blue"))
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z_index: int = 0,
    ) -> None:
        """
        Create an EntityGroup.

        Args:
            x: Initial x position (default 0).
            y: Initial y position (default 0).
            z_index: Layer ordering (higher = on top).
        """
        super().__init__(x, y, z_index)
        self._children: list[Entity] = []
        self._scale: float = 1.0
        self._rotation: float = 0.0  # degrees

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
        raise ValueError(
            f"EntityGroup has no anchor '{name}'. "
            f"Available: {self.anchor_names}"
        )

    def bounds(self) -> tuple[float, float, float, float]:
        """
        Bounding box in absolute coordinates.

        Accounts for the group's position, scale factor, and rotation.
        Children's bounds are in local coordinates, transformed by
        ``translate(position) rotate(angle) scale(factor)``.

        Returns:
            (min_x, min_y, max_x, max_y) in absolute coordinates.
        """
        if not self._children:
            return (self.x, self.y, self.x, self.y)

        all_bounds = [child.bounds() for child in self._children]
        # Local bounds after scale
        local_min_x = min(b[0] for b in all_bounds) * self._scale
        local_min_y = min(b[1] for b in all_bounds) * self._scale
        local_max_x = max(b[2] for b in all_bounds) * self._scale
        local_max_y = max(b[3] for b in all_bounds) * self._scale

        if self._rotation == 0:
            return (
                self.x + local_min_x,
                self.y + local_min_y,
                self.x + local_max_x,
                self.y + local_max_y,
            )

        # Rotate corners around local origin and find AABB
        angle_rad = math.radians(self._rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        corners = [
            (local_min_x, local_min_y),
            (local_max_x, local_min_y),
            (local_max_x, local_max_y),
            (local_min_x, local_max_y),
        ]
        rotated = [
            (x * cos_a - y * sin_a, x * sin_a + y * cos_a)
            for x, y in corners
        ]

        return (
            self.x + min(rx for rx, _ in rotated),
            self.y + min(ry for _, ry in rotated),
            self.x + max(rx for rx, _ in rotated),
            self.y + max(ry for _, ry in rotated),
        )

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
        parts = [f'<g transform="{transform_str}">']
        for child in sorted_children:
            parts.append(f"  {child.to_svg()}")
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

    # =========================================================================
    # DEFS COLLECTION (forward to children)
    # =========================================================================

    def get_required_markers(self):
        """Collect SVG marker definitions from all children."""
        for child in self._children:
            if hasattr(child, "get_required_markers"):
                yield from child.get_required_markers()

    def get_required_paths(self):
        """Collect SVG path definitions from all children."""
        for child in self._children:
            if hasattr(child, "get_required_paths"):
                yield from child.get_required_paths()

    def __repr__(self) -> str:
        n = len(self._children)
        return (
            f"EntityGroup({n} children, "
            f"pos=({self.x:.1f}, {self.y:.1f}), "
            f"scale={self._scale:.2f})"
        )
