"""Tests for Entity base class methods, particularly fit_to_cell()."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene
from pyfreeform.entities.point import Point
from pyfreeform.entities.dot import Dot


def test_fit_to_cell_dot():
    """Test fit_to_cell() with a Dot entity."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create a large dot
    dot = cell.add_dot(radius=2.5, color="red")  # Way too big

    # Fit to cell (100% = should shrink to radius 10)
    dot.fit_to_cell(1.0)

    # Should be scaled down to fit
    assert dot.radius <= 10.0
    assert dot.radius > 9.9  # Close to 10

    # Should be centered in cell
    assert abs(dot.x - (cell.x + cell.width / 2)) < 0.1
    assert abs(dot.y - (cell.y + cell.height / 2)) < 0.1


def test_fit_to_cell_ellipse_rotated():
    """Test fit_to_cell() with a rotated Ellipse."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create ellipse with rotation
    ellipse = cell.add_ellipse(rx=2.5, ry=1.5, rotation=45)

    # Fit to 80% of cell
    ellipse.fit_to_cell(0.8)

    # Check bounds fit within cell (with small tolerance for rotation sampling)
    min_x, min_y, max_x, max_y = ellipse.bounds()
    tolerance = 0.5  # Small tolerance for rotation approximation
    assert min_x >= cell.x - tolerance
    assert min_y >= cell.y - tolerance
    assert max_x <= cell.x + cell.width + tolerance
    assert max_y <= cell.y + cell.height + tolerance


def test_fit_to_cell_text():
    """Test fit_to_cell() with Text entity."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create large text (5.0 = 500% of cell height = very large)
    text = cell.add_text("Hello", font_size=5.0)

    # Fit to cell
    text.fit_to_cell(0.9)

    # Should be smaller than original (5.0 * 20 = 100 pixels)
    assert text.font_size < 100

    # Bounds should fit within cell (with tolerance for text approximation)
    min_x, min_y, max_x, max_y = text.bounds()
    tolerance = 2  # Larger tolerance for text approximation
    assert min_x >= cell.x - tolerance
    assert max_x <= cell.x + cell.width + tolerance


def test_fit_to_cell_polygon():
    """Test fit_to_cell() with a Polygon entity."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create a large polygon (square)
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    polygon = cell.add_polygon(vertices=vertices, fill="blue")

    # Fit to 90% of cell
    polygon.fit_to_cell(0.9)

    # Check bounds fit within cell
    min_x, min_y, max_x, max_y = polygon.bounds()
    assert min_x >= cell.x
    assert min_y >= cell.y
    assert max_x <= cell.x + cell.width
    assert max_y <= cell.y + cell.height


def test_fit_to_cell_no_cell():
    """Test that fit_to_cell() raises error when entity has no cell."""
    # Create standalone dot (not in a cell)
    dot = Dot(x=50, y=50, radius=10)

    with pytest.raises(ValueError, match="entity has no cell"):
        dot.fit_to_cell(0.8)


def test_fit_to_cell_invalid_scale_zero():
    """Test that fit_to_cell() rejects scale of 0.0."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]
    dot = cell.add_dot(radius=0.25)

    with pytest.raises(ValueError, match="scale must be between"):
        dot.fit_to_cell(0.0)  # Too small


def test_fit_to_cell_invalid_scale_too_large():
    """Test that fit_to_cell() rejects scale > 1.0."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]
    dot = cell.add_dot(radius=0.25)

    with pytest.raises(ValueError, match="scale must be between"):
        dot.fit_to_cell(1.5)  # Too large


def test_fit_to_cell_no_recenter():
    """Test fit_to_cell(recenter=False) maintains relative position."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create dot at specific position (top-left quadrant)
    dot = cell.add_dot(at=(0.25, 0.25), radius=2.5)
    original_x, original_y = dot.x, dot.y

    # Fit without recentering
    dot.fit_to_cell(0.8, recenter=False)

    # Position should stay roughly the same (small changes from scaling)
    assert abs(dot.x - original_x) < 1.0
    assert abs(dot.y - original_y) < 1.0


def test_fit_to_cell_with_recenter():
    """Test fit_to_cell(recenter=True) centers entity in cell."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create dot at off-center position
    dot = cell.add_dot(at=(0.25, 0.25), radius=2.5)

    # Fit with recentering (default)
    dot.fit_to_cell(0.8, recenter=True)

    # Should be centered
    cell_center_x = cell.x + cell.width / 2
    cell_center_y = cell.y + cell.height / 2
    assert abs(dot.x - cell_center_x) < 0.1
    assert abs(dot.y - cell_center_y) < 0.1


def test_fit_to_cell_method_chaining():
    """Test that fit_to_cell() supports method chaining."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Should support chaining
    ellipse = cell.add_ellipse(rx=2.5, ry=1.5).fit_to_cell(0.8)

    assert ellipse is not None
    # Check it's the same type as a fresh ellipse
    fresh_ellipse = cell.add_ellipse(rx=0.05, ry=0.05)
    assert type(ellipse) == type(fresh_ellipse)


def test_fit_to_cell_already_fits():
    """Test that fit_to_cell() scales up entities that are smaller than cell."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    # Create small dot that is smaller than cell
    dot = cell.add_dot(radius=0.15, color="blue")

    # Fit to cell (should scale up to fill)
    dot.fit_to_cell(1.0)

    # Radius should be scaled up to fill the cell (cell is 20x20, so radius ~10)
    assert dot.radius > 3
    min_x, min_y, max_x, max_y = dot.bounds()
    assert max_x - min_x <= cell.width + 0.1
    assert max_y - min_y <= cell.height + 0.1


def test_fit_to_cell_different_scales():
    """Test fit_to_cell() with different scale values."""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=20)

    # Create three identical large dots
    dot1 = scene.grid[0, 0].add_dot(radius=2.5)
    dot2 = scene.grid[0, 1].add_dot(radius=2.5)
    dot3 = scene.grid[0, 2].add_dot(radius=2.5)

    # Fit to different scales
    dot1.fit_to_cell(1.0)  # 100% of cell
    dot2.fit_to_cell(0.5)  # 50% of cell
    dot3.fit_to_cell(0.1)  # 10% of cell

    # Verify scaling relationship
    assert dot1.radius > dot2.radius > dot3.radius
    assert abs(dot1.radius - 10.0) < 0.1  # Full cell radius
    assert abs(dot2.radius - 5.0) < 0.1   # Half cell radius
    assert abs(dot3.radius - 1.0) < 0.1   # 10% cell radius


def test_fit_to_cell_brightness_based_scaling():
    """Test the pattern from Example 14: brightness-based scaling."""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=20)

    # Simulate different brightness values
    cell1 = scene.grid[0, 0]
    cell2 = scene.grid[0, 1]

    # Create ellipses
    ellipse1 = cell1.add_ellipse(rx=5.0, ry=3.0, rotation=0)
    ellipse2 = cell2.add_ellipse(rx=5.0, ry=3.0, rotation=0)

    # Simulate brightness-based scaling: 30% to 100%
    brightness1 = 0.0  # Dark -> 30% scale
    brightness2 = 1.0  # Bright -> 100% scale

    scale1 = 0.3 + brightness1 * 0.7
    scale2 = 0.3 + brightness2 * 0.7

    ellipse1.fit_to_cell(scale1)
    ellipse2.fit_to_cell(scale2)

    # Bright cell should have larger ellipse
    assert ellipse2.rx > ellipse1.rx
    assert ellipse2.ry > ellipse1.ry


# =========================================================================
# Tests for fit_to_cell(at=) — position-aware mode
# =========================================================================


def test_fit_to_cell_at_center_same_as_default():
    """at=(0.5, 0.5) should behave same as default centering."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    # Two identical dots — one default, one with at=center
    dot_default = cell.add_dot(radius=2.0, color="red")
    dot_default.fit_to_cell(0.8)
    r_default = dot_default.radius
    x_default, y_default = dot_default.x, dot_default.y

    scene2 = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell2 = scene2.grid[0, 0]
    dot_at = cell2.add_dot(radius=2.0, color="red")
    dot_at.fit_to_cell(0.8, at=(0.5, 0.5))

    assert abs(dot_at.radius - r_default) < 0.1
    assert abs(dot_at.x - x_default) < 0.1
    assert abs(dot_at.y - y_default) < 0.1


def test_fit_to_cell_at_corner_no_overflow():
    """at=(0.25, 0.25) should constrain to nearest-edge quadrant."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    dot = cell.add_dot(radius=9.99, color="blue")
    dot.fit_to_cell(1.0, at=(0.25, 0.25))

    # Entity must not overflow any cell edge
    min_x, min_y, max_x, max_y = dot.bounds()
    assert min_x >= cell.x - 0.1
    assert min_y >= cell.y - 0.1
    assert max_x <= cell.x + cell.width + 0.1
    assert max_y <= cell.y + cell.height + 0.1

    # Should be positioned at (0.25, 0.25) of cell
    expected_x = cell.x + cell.width * 0.25
    expected_y = cell.y + cell.height * 0.25
    assert abs(dot.x - expected_x) < 1.0
    assert abs(dot.y - expected_y) < 1.0


def test_fit_to_cell_at_corner_smaller_than_center():
    """Entity at corner should be smaller than entity at center (same scale)."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    dot_center = cell.add_dot(radius=9.99, color="red")
    dot_center.fit_to_cell(1.0, at=(0.5, 0.5))

    scene2 = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell2 = scene2.grid[0, 0]
    dot_corner = cell2.add_dot(radius=9.99, color="blue")
    dot_corner.fit_to_cell(1.0, at=(0.25, 0.25))

    # Corner has less available space → smaller radius
    assert dot_corner.radius < dot_center.radius


def test_fit_to_cell_at_rejects_strings():
    """Named positions should be rejected with helpful error."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]
    dot = cell.add_dot(radius=0.1, color="red")

    with pytest.raises(TypeError, match="only accepts"):
        dot.fit_to_cell(0.8, at="top_left")


def test_fit_to_cell_at_rejects_edge_zero():
    """Values at 0.0 should be rejected."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]
    dot = cell.add_dot(radius=0.1, color="red")

    with pytest.raises(ValueError, match="inside the cell"):
        dot.fit_to_cell(0.8, at=(0.0, 0.5))


def test_fit_to_cell_at_rejects_edge_one():
    """Values at 1.0 should be rejected."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]
    dot = cell.add_dot(radius=0.1, color="red")

    with pytest.raises(ValueError, match="inside the cell"):
        dot.fit_to_cell(0.8, at=(0.5, 1.0))


def test_fit_to_cell_at_with_polygon():
    """Position-aware fit with oversized polygon."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    # Large polygon that exceeds cell
    polygon = cell.add_polygon(
        vertices=[(0, 0), (1, 0), (1, 1), (0, 1)],
        fill="green",
    )
    polygon.fit_to_cell(0.8, at=(0.75, 0.75))

    # Must not overflow
    min_x, min_y, max_x, max_y = polygon.bounds()
    assert min_x >= cell.x - 0.1
    assert min_y >= cell.y - 0.1
    assert max_x <= cell.x + cell.width + 0.1
    assert max_y <= cell.y + cell.height + 0.1

    # Center should be near the target position
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    expected_x = cell.x + cell.width * 0.75
    expected_y = cell.y + cell.height * 0.75
    assert abs(cx - expected_x) < 1.0
    assert abs(cy - expected_y) < 1.0


def test_fit_to_cell_at_with_ellipse():
    """Position-aware fit with oversized ellipse."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    ellipse = cell.add_ellipse(rx=2.0, ry=1.5)
    ellipse.fit_to_cell(0.9, at=(0.3, 0.7))

    min_x, min_y, max_x, max_y = ellipse.bounds()
    assert min_x >= cell.x - 0.5
    assert min_y >= cell.y - 0.5
    assert max_x <= cell.x + cell.width + 0.5
    assert max_y <= cell.y + cell.height + 0.5


def test_fit_to_cell_at_method_chaining():
    """fit_to_cell(at=) should support method chaining."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    result = cell.add_dot(radius=2.0).fit_to_cell(0.8, at=(0.5, 0.5))
    assert result is not None


def test_fit_to_cell_backward_compat_no_at():
    """Existing calls without at= must work identically."""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0, 0]

    dot = cell.add_dot(radius=2.5, color="red")
    dot.fit_to_cell(1.0)

    assert dot.radius <= 10.0
    assert dot.radius > 9.9
    assert abs(dot.x - (cell.x + cell.width / 2)) < 0.1
    assert abs(dot.y - (cell.y + cell.height / 2)) < 0.1
