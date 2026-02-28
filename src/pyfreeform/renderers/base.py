"""Base renderer protocol for PyFreeform."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.connection import Connection
    from ..core.entity import Entity
    from ..scene.scene import Scene


class Renderer(ABC):
    """Abstract base class for PyFreeform renderers.

    A renderer converts a Scene (model) into an output string.
    Subclasses implement type-specific rendering for each entity kind.

    The default ``render_entity`` dispatches to ``render_<typename>``
    methods (e.g., ``render_dot``, ``render_rect``) based on the
    entity's class name.
    """

    @abstractmethod
    def render_scene(self, scene: Scene) -> str:
        """Render a complete scene to output string."""

    def render_entity(self, entity: Entity) -> str:
        """Dispatch to type-specific render method.

        Looks up ``render_<classname>`` (lowercase) on this renderer.
        """
        method_name = f"render_{type(entity).__name__.lower()}"
        method = getattr(self, method_name, None)
        if method is None:
            raise TypeError(
                f"{type(self).__name__} has no render method for "
                f"{type(entity).__name__} (expected method '{method_name}')"
            )
        return method(entity)

    @abstractmethod
    def render_connection(self, conn: Connection) -> str:
        """Render a connection to output string."""
