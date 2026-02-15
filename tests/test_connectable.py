"""Tests for connectable surfaces — anchor, connect, and auto-collection."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Connectable, Connection, Coord, Dot, Scene, Surface


# =========================================================================
# Surface anchors
# =========================================================================


class TestSurfaceAnchors:
    def test_anchor_names(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[0][0]
        names = cell.anchor_names
        assert "center" in names
        assert "top_left" in names
        assert "bottom_right" in names
        assert len(names) == 9

    def test_anchor_center(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[0][0]
        center = cell.anchor("center")
        assert center == cell.center

    def test_anchor_top_left(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[0][0]
        tl = cell.anchor("top_left")
        assert tl == cell.top_left

    def test_anchor_bottom_right(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[0][0]
        br = cell.anchor("bottom_right")
        assert br == cell.bottom_right

    def test_anchor_top(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[1][1]
        top = cell.anchor("top")
        assert top.x == cell.center.x
        assert top.y == cell.top_left.y

    def test_anchor_right(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[1][1]
        right = cell.anchor("right")
        assert right.x == cell.top_right.x
        assert right.y == cell.center.y

    def test_anchor_invalid_raises(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[0][0]
        with pytest.raises(ValueError, match="Unknown anchor"):
            cell.anchor("nonexistent")

    def test_anchor_default_is_center(self):
        scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
        cell = scene.grid[0][0]
        assert cell.anchor() == cell.anchor("center")

    def test_scene_anchors(self):
        scene = Scene(100, 200)
        assert scene.anchor("center") == Coord(50, 100)
        assert scene.anchor("top_left") == Coord(0, 0)
        assert scene.anchor("bottom_right") == Coord(100, 200)


# =========================================================================
# Cell-to-Cell connections
# =========================================================================


class TestCellToCell:
    def test_cell_connect_cell(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        conn = cell_a.connect(cell_b)

        assert isinstance(conn, Connection)
        assert conn.start is cell_a
        assert conn.end is cell_b

    def test_both_cells_track_connection(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        conn = cell_a.connect(cell_b)

        assert conn in cell_a.connections
        assert conn in cell_b.connections

    def test_cell_connection_renders(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        cell_a.connect(cell_b, color="red")

        svg = scene.to_svg()
        assert "line" in svg or "path" in svg

    def test_cell_connect_with_anchors(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        conn = cell_a.connect(cell_b, start_anchor="right", end_anchor="left")

        assert conn.start_point == cell_a.anchor("right")
        assert conn.end_point == cell_b.anchor("left")


# =========================================================================
# Entity-to-Cell connections
# =========================================================================


class TestEntityToCell:
    def test_entity_connect_cell(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell = scene.grid[0][0]
        dot = cell.add_dot(color="black")
        cell_b = scene.grid[0][2]

        conn = dot.connect(cell_b)
        assert conn.start is dot
        assert conn.end is cell_b

    def test_cell_connect_entity(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell = scene.grid[0][0]
        dot = scene.grid[0][2].add_dot(color="black")

        conn = cell.connect(dot)
        assert conn.start is cell
        assert conn.end is dot

    def test_mixed_connection_renders(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell = scene.grid[0][0]
        dot = scene.grid[0][2].add_dot(color="black")
        cell.connect(dot, color="blue")

        svg = scene.to_svg()
        assert "blue" in svg


# =========================================================================
# Cross-grid connections
# =========================================================================


class TestCrossGrid:
    def _two_grid_scene(self):
        from pyfreeform import Grid
        scene = Scene(200, 100)
        grid1 = Grid(cols=2, rows=2, cell_size=20, origin=(0, 0))
        grid2 = Grid(cols=2, rows=2, cell_size=20, origin=(100, 0))
        scene.add_grid(grid1)
        scene.add_grid(grid2)
        return scene, grid1, grid2

    def test_cross_grid_cell_connection(self):
        scene, grid1, grid2 = self._two_grid_scene()
        cell_a = grid1[0][0]
        cell_b = grid2[0][0]
        conn = cell_a.connect(cell_b)

        # Scene should auto-collect it
        assert conn in scene.connections

    def test_cross_grid_renders(self):
        scene, grid1, grid2 = self._two_grid_scene()
        grid1[0][0].connect(grid2[0][0], color="green")
        svg = scene.to_svg()
        assert "green" in svg


# =========================================================================
# Connection.data
# =========================================================================


class TestConnectionData:
    def test_connection_data_empty_by_default(self):
        d1 = Dot(10, 10)
        d2 = Dot(20, 20)
        conn = d1.connect(d2)
        assert conn.data == {}

    def test_connection_data_read_write(self):
        d1 = Dot(10, 10)
        d2 = Dot(20, 20)
        conn = d1.connect(d2)
        conn.data["weight"] = 0.5
        conn.data["label"] = "edge"
        assert conn.data["weight"] == 0.5
        assert conn.data["label"] == "edge"


# =========================================================================
# Scene auto-collection
# =========================================================================


class TestSceneAutoCollect:
    def test_entity_connections_auto_collected(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        d1 = scene.grid[0][0].add_dot(color="black")
        d2 = scene.grid[0][2].add_dot(color="black")
        conn = d1.connect(d2)

        assert conn in scene.connections

    def test_cell_connections_auto_collected(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        conn = cell_a.connect(cell_b)

        assert conn in scene.connections

    def test_no_duplicate_connections(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        conn = cell_a.connect(cell_b)

        conns = scene.connections
        assert conns.count(conn) == 1

    def test_scene_as_endpoint(self):
        scene = Scene(100, 100)
        dot = Dot(10, 10)
        scene.add(dot)
        conn = scene.connect(dot, start_anchor="center")

        assert conn in scene.connections


# =========================================================================
# Backward compatibility
# =========================================================================


class TestBackwardCompat:
    def test_entity_entity_still_works(self):
        d1 = Dot(10, 10)
        d2 = Dot(50, 50)
        conn = d1.connect(d2, width=2, color="red")

        assert conn.start is d1
        assert conn.end is d2
        assert conn.color == "red"

    def test_entity_entity_in_scene(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        d1 = scene.grid[0][0].add_dot(color="black")
        d2 = scene.grid[0][2].add_dot(color="black")
        conn = d1.connect(d2)

        svg = scene.to_svg()
        assert "line" in svg or "path" in svg


# =========================================================================
# Disconnect
# =========================================================================


class TestDisconnect:
    def test_disconnect_removes_from_both_endpoints(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        cell_a = scene.grid[0][0]
        cell_b = scene.grid[0][2]
        conn = cell_a.connect(cell_b)

        assert conn in cell_a.connections
        assert conn in cell_b.connections

        conn.disconnect()

        assert conn not in cell_a.connections
        assert conn not in cell_b.connections

    def test_disconnect_entity_cell(self):
        scene = Scene.with_grid(cols=3, rows=1, cell_size=20)
        dot = scene.grid[0][0].add_dot(color="black")
        cell = scene.grid[0][2]
        conn = dot.connect(cell)

        conn.disconnect()

        assert conn not in dot.connections
        assert conn not in cell.connections


# =========================================================================
# Connectable type alias
# =========================================================================


class TestConnectableType:
    def test_connectable_exported(self):
        assert Connectable is not None

    def test_surface_is_connectable(self):
        scene = Scene(100, 100)
        # Surface satisfies the Connectable interface (has anchor, add_connection, etc.)
        assert hasattr(scene, "anchor")
        assert hasattr(scene, "connect")
        assert hasattr(scene, "add_connection")
        assert hasattr(scene, "remove_connection")
        assert hasattr(scene, "connections")
