"""Generate SVGs for Guide: Gradients."""

import math
import random

from pyfreeform import (
    Dot,
    EntityGroup,
    LinearGradient,
    Polygon,
    RadialGradient,
    Scene,
    between,
)

from wiki._generator import save


def _label_pos(shape, cell):
    """Midpoint between a shape's bottom edge and the cell's bottom edge."""
    bottom = shape.relative_bounds()[3]
    return between((0.5, bottom), (0.5, 1.0))


def generate():
    # --- 1. Basic linear gradient: just two colors ---
    scene = Scene(360, 120, background="#1a1a2e")
    scene.add_rect(fill=LinearGradient("red", "blue"), width=0.9, height=0.6)
    save(scene, "guide/grad-basic-linear.svg")

    # --- 2. Linear gradient angles ---
    scene = Scene.with_grid(cols=4, rows=1, cell_size=90, background="#1a1a2e")
    angles = [0, 45, 90, 135]
    for i, cell in enumerate(scene.grid):
        a = angles[i]
        shape = cell.add_rect(
            fill=LinearGradient("coral", "dodgerblue", angle=a),
            width=0.75,
            height=0.65,
        )
        cell.add_text(f"{a}\u00b0", at=_label_pos(shape, cell), font_size=0.15, color="white")
    save(scene, "guide/grad-angles.svg")

    # --- 3. Multi-stop gradient ---
    scene = Scene(360, 120, background="#1a1a2e")
    scene.add_rect(
        fill=LinearGradient("red", "gold", "limegreen", "dodgerblue", "mediumpurple"),
        width=0.9,
        height=0.6,
    )
    save(scene, "guide/grad-multi-stop.svg")

    # --- 4. Custom offsets: red stays longer, blue compressed at the end ---
    scene = Scene.with_grid(cols=2, rows=1, cell_size=90, background="#1a1a2e")
    # Even distribution
    c0 = scene.grid[0][0]
    shape0 = c0.add_rect(
        fill=LinearGradient("red", "blue", "white"),
        width=0.9,
        height=0.7,
    )
    c0.add_text("even", at=_label_pos(shape0, c0), font_size=0.13, color="white")
    # Custom offsets
    c1 = scene.grid[0][1]
    shape1 = c1.add_rect(
        fill=LinearGradient(("red", 0.0), ("blue", 0.7), ("white", 1.0)),
        width=0.9,
        height=0.7,
    )
    c1.add_text("custom", at=_label_pos(shape1, c1), font_size=0.13, color="white")
    save(scene, "guide/grad-offsets.svg")

    # --- 4b. Hard edges: solid + gradient sections ---
    scene = Scene(360, 100, background="#1a1a2e")
    scene.add_rect(
        fill=LinearGradient(
            ("black", 0.0), ("black", 0.4),
            ("red", 0.4), ("yellow", 1.0),
        ),
        width=0.9,
        height=0.6,
    )
    save(scene, "guide/grad-hard-edge.svg")

    # --- 5. Basic radial gradient ---
    scene = Scene(360, 200, background="#1a1a2e")
    scene.add_ellipse(
        fill=RadialGradient("white", "dodgerblue", "midnightblue"),
        rx=0.35,
        ry=0.35,
    )
    save(scene, "guide/grad-basic-radial.svg")

    # --- 6. Radial gradient with focal point (off-center light) ---
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120, background="#1a1a2e")
    focal_positions = [
        (0.5, 0.5, "centered"),
        (0.3, 0.3, "top-left"),
        (0.7, 0.3, "top-right"),
    ]
    for i, cell in enumerate(scene.grid):
        fx, fy, label = focal_positions[i]
        shape = cell.add_ellipse(
            fill=RadialGradient("white", "dodgerblue", "midnightblue", fx=fx, fy=fy),
            rx=0.42,
            ry=0.42,
        )
        cell.add_text(label, at=_label_pos(shape, cell), font_size=0.11, color="white")
    save(scene, "guide/grad-radial-focal.svg")

    # --- 7. Gradients on different entities ---
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    sunset = LinearGradient("orangered", "gold", angle=90)
    ocean = RadialGradient("lightskyblue", "navy")

    # Rect
    c = scene.grid[0][0]
    s = c.add_rect(fill=sunset, width=0.7, height=0.7)
    c.add_text("rect", at=_label_pos(s, c), font_size=0.12, color="white")
    # Ellipse
    c = scene.grid[0][1]
    s = c.add_ellipse(fill=ocean, rx=0.35, ry=0.35)
    c.add_text("ellipse", at=_label_pos(s, c), font_size=0.12, color="white")
    # Polygon
    c = scene.grid[0][2]
    s = c.add_polygon(Polygon.hexagon(size=0.7), fill=sunset)
    c.add_text("polygon", at=_label_pos(s, c), font_size=0.12, color="white")
    # Dot
    c = scene.grid[0][3]
    s = c.add_dot(radius=0.35, color=ocean)
    c.add_text("dot", at=_label_pos(s, c), font_size=0.12, color="white")
    save(scene, "guide/grad-entities.svg")

    # --- 8. Gradient stroke ---
    scene = Scene(360, 120, background="#1a1a2e")
    scene.add_rect(
        fill=None,
        stroke=LinearGradient("coral", "dodgerblue"),
        stroke_width=4,
        width=0.85,
        height=0.55,
    )
    save(scene, "guide/grad-stroke.svg")

    # --- 9. Fun example: sunset scene ---
    scene = Scene(400, 250, background="#1a1a2e")
    # Sky
    sky = LinearGradient(
        ("midnightblue", 0.0),
        ("darkorange", 0.6),
        ("gold", 0.85),
        ("lightyellow", 1.0),
        angle=90,
    )
    scene.add_rect(fill=sky, width=1.0, height=1.0)
    # Sun
    sun = RadialGradient(
        ("white", 0.0),
        ("gold", 0.3),
        ("orangered", 0.7),
        ("transparent", 1.0),
    )
    scene.add_ellipse(fill=sun, rx=0.12, ry=0.19, at=(0.5, 0.75))
    # Ground
    ground = LinearGradient(("darkgreen", 0.0), ("black", 1.0), angle=90)
    scene.add_rect(fill=ground, width=1.0, height=0.2, at=(0.5, 0.9))
    save(scene, "guide/grad-sunset.svg")

    # --- 10. Fun example: glowing orbs ---
    scene = Scene(400, 200, background="#0a0a1a")
    orb_colors = ["#ff006e", "#00f5d4", "#fee440", "#8338ec", "#3a86ff"]
    for i, c in enumerate(orb_colors):
        x = 0.15 + i * 0.175
        glow = RadialGradient((c, 0.0), ("transparent", 1.0))
        scene.add_ellipse(fill=glow, rx=0.08, ry=0.16, at=(x, 0.5))
        # Bright core
        scene.add_dot(radius=0.02, color=c, at=(x, 0.5))
    save(scene, "guide/grad-glowing-orbs.svg")

    # --- 11. Fun example: gem stones ---
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80, background="#1a1a2e")
    gem_colors = [
        ("ruby", "#e0115f", "#8b0000"),
        ("emerald", "#50c878", "#004d00"),
        ("sapphire", "#0f52ba", "#00008b"),
        ("amethyst", "#9966cc", "#4b0082"),
        ("topaz", "#ffc87c", "#cc7722"),
    ]
    for i, cell in enumerate(scene.grid):
        name, light, dark = gem_colors[i]
        gem_grad = RadialGradient(
            ("white", 0.0, 0.9),
            (light, 0.3),
            (dark, 1.0),
            fx=0.35,
            fy=0.35,
        )
        shape = cell.add_polygon(
            Polygon.hexagon(size=0.75),
            fill=gem_grad,
            stroke=light,
            stroke_width=1,
            stroke_opacity=0.5,
        )
        cell.add_text(name, at=_label_pos(shape, cell), font_size=0.12, color="gray")
    save(scene, "guide/grad-gems.svg")

    # --- 12. Gradient reuse: one gradient, many shapes ---
    scene = Scene.with_grid(cols=6, rows=1, cell_size=60, background="#1a1a2e")
    fire = LinearGradient("yellow", "orangered", "darkred", angle=90)
    for i, cell in enumerate(scene.grid):
        n = 3 + i  # 3 to 8 sides
        verts = Polygon.regular_polygon(n, size=0.7)
        cell.add_polygon(verts, fill=fire)
    save(scene, "guide/grad-reuse.svg")

    # --- 13. EntityGroup with gradients ---
    def make_badge(label, fill_grad, accent):
        g = EntityGroup()
        # Outer ring
        for k in range(12):
            angle = k * (2 * math.pi / 12)
            g.add(Dot(18 * math.cos(angle), 18 * math.sin(angle), radius=4, color=accent))
        # Center
        g.add(Dot(0, 0, radius=12, color=fill_grad))
        return g

    scene = Scene.with_grid(cols=3, rows=1, cell_size=100, background="#1a1a2e")
    badges = [
        ("gold", RadialGradient("lightyellow", "gold", "darkgoldenrod"), "gold"),
        ("silver", RadialGradient("white", "silver", "gray"), "silver"),
        ("bronze", RadialGradient("peachpuff", "#cd7f32", "#8b4513"), "#cd7f32"),
    ]
    for i, cell in enumerate(scene.grid):
        label, grad, accent = badges[i]
        badge = cell.add(make_badge(label, grad, accent))
        cell.add_text(label, at=_label_pos(badge, cell), font_size=0.12, color="white")
    save(scene, "guide/grad-entity-group.svg")

    # --- 14a. Stop opacity: simple fade ---
    scene = Scene(360, 120, background="#1a1a2e")
    # Scatter colorful dots behind
    rng = random.Random(99)
    dot_colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#ff6eb4"]
    for _ in range(50):
        scene.add_dot(
            at=(rng.uniform(0.05, 0.95), rng.uniform(0.1, 0.9)),
            radius=rng.uniform(0.02, 0.04),
            color=rng.choice(dot_colors),
        )
    fade = LinearGradient(
        ("coral", 0.0, 1.0),   # fully opaque
        ("coral", 1.0, 0.0),   # fully transparent
    )
    scene.add_rect(fill=fade, width=1.0, height=1.0)
    save(scene, "guide/grad-simple-fade.svg")

    # --- 14b. Stop opacity: peek-through gradient ---
    scene = Scene(400, 120, background="#1a1a2e")
    # Scatter colorful dots behind
    rng = random.Random(42)
    dot_colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#ff6eb4"]
    for _ in range(60):
        scene.add_dot(
            at=(rng.uniform(0.05, 0.95), rng.uniform(0.1, 0.9)),
            radius=rng.uniform(0.02, 0.04),
            color=rng.choice(dot_colors),
        )
    # Colorful gradient that fades smoothly to transparent in the middle
    bar = LinearGradient(
        ("coral", 0.0, 1.0),
        ("#9b59b6", 0.35, 0.8),
        ("dodgerblue", 0.5, 0.0),   # fully transparent — dots peek through
        ("#9b59b6", 0.65, 0.8),
        ("coral", 1.0, 1.0),
    )
    scene.add_rect(fill=bar, width=1.0, height=1.0)
    save(scene, "guide/grad-stop-opacity.svg")
