"""Generate SVGs for Recipe: Hidden Gems."""

import heapq
import math
import random

from pyfreeform import Scene, Palette, PathStyle, Polygon, Dot
from pyfreeform.color import hsl

from wiki._generator import save, sample_image


def generate():
    _generate_maze()
    _generate_dijkstra()
    _generate_sierpinski()
    _generate_phyllotaxis()
    _generate_voronoi_portrait()
    _generate_double_slit()


# ── 1. Random Maze ──────────────────────────────────────────────────────


def _generate_maze(cols=15, rows=12, cell_size=22, seed=42):
    random.seed(seed)
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=cols, rows=rows, cell_size=cell_size, background=colors.background
    )
    g = scene.grid

    for cell in g:
        cell.data["visited"] = False
        cell.data["passages"] = []

    stack = [g[0][0]]
    g[0][0].data["visited"] = True

    while stack:
        current = stack[-1]
        unvisited = [
            n for n in current.neighbors.values()
            if n and not n.data["visited"]
        ]
        if unvisited:
            nxt = random.choice(unvisited)
            nxt.data["visited"] = True
            current.data["passages"].append((nxt.row, nxt.col))
            nxt.data["passages"].append((current.row, current.col))
            stack.append(nxt)
        else:
            stack.pop()

    style = PathStyle(width=3, color=colors.accent, opacity=0.8)
    for cell in g:
        cell.add_border(color=colors.grid, width=1, opacity=0.6, z_index=2)
        for r, c in cell.data["passages"]:
            if (r, c) > (cell.row, cell.col):
                cell.connect(g[r][c], style=style, z_index=1)

    g[0][0].add_dot(radius=0.25, color=colors.primary, z_index=3)
    g[g.num_rows - 1][g.num_columns - 1].add_dot(
        radius=0.25, color=colors.secondary, z_index=3
    )
    save(scene, "recipes/gem-maze.svg")


# ── 2. Dijkstra Wavefront ─────────────────────────────────────────────


def _generate_dijkstra(cols=28, rows=22, cell_size=16, wall_density=0.25, seed=7):
    random.seed(seed)
    scene = Scene.with_grid(
        cols=cols, rows=rows, cell_size=cell_size, background="#08080f"
    )
    g = scene.grid
    start, end = g[0][0], g[g.num_rows - 1][g.num_columns - 1]

    for cell in g:
        cell.data["wall"] = random.random() < wall_density
        cell.data["dist"] = float("inf")
        cell.data["parent"] = None
        cell.data["weight"] = 1.0 + random.random() * 3.0

    for cell in (start, end):
        cell.data["wall"] = False
    for cell in (start.right, start.below, end.left, end.above):
        if cell:
            cell.data["wall"] = False

    start.data["dist"] = 0.0
    pq = [(0.0, start.row, start.col)]
    while pq:
        d, r, c = heapq.heappop(pq)
        cell = g[r][c]
        if d > cell.data["dist"]:
            continue
        for nb in cell.neighbors.values():
            if nb is None or nb.data["wall"]:
                continue
            nd = d + nb.data["weight"]
            if nd < nb.data["dist"]:
                nb.data["dist"] = nd
                nb.data["parent"] = (r, c)
                heapq.heappush(pq, (nd, nb.row, nb.col))

    max_dist = max(
        (c.data["dist"] for c in g if c.data["dist"] < float("inf")), default=1.0
    )
    for cell in g:
        if cell.data["wall"]:
            cell.add_fill(color="#1a1a2e")
        elif cell.data["dist"] < float("inf"):
            t = cell.data["dist"] / max_dist
            cell.add_fill(color=hsl(240 - t * 200, 0.8, 0.18 + t * 0.32))
        cell.add_border(color="#181828", width=0.5, opacity=0.4, z_index=1)

    path_style = PathStyle(width=3, color=hsl(50, 0.95, 0.6), opacity=1.0, z_index=3)
    cur = end
    while cur and cur.data["parent"]:
        pr, pc = cur.data["parent"]
        g[pr][pc].connect(cur, style=path_style)
        cur = g[pr][pc]

    start.add_dot(radius=0.3, color=hsl(120, 0.9, 0.5), z_index=4)
    end.add_dot(radius=0.3, color=hsl(0, 0.9, 0.55), z_index=4)
    save(scene, "recipes/gem-dijkstra.svg")


# ── 3. Sierpinski Triangle ─────────────────────────────────────────────


def _generate_sierpinski(width=440, height=400, depth=7, margin=15):
    scene = Scene(width, height, background="#08080f")

    def mid(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    def draw(v1, v2, v3, d):
        if d == depth:
            cx = (v1[0] + v2[0] + v3[0]) / 3
            cy = (v1[1] + v2[1] + v3[1]) / 3
            color = hsl((cx / width) * 300, 0.85, 0.48 + 0.12 * (1 - cy / height))
            scene.place(Polygon([v1, v2, v3], fill=color, stroke=None, opacity=0.92))
            return
        m12, m23, m13 = mid(v1, v2), mid(v2, v3), mid(v1, v3)
        draw(v1, m12, m13, d + 1)
        draw(m12, v2, m23, d + 1)
        draw(m13, m23, v3, d + 1)

    top = (width / 2, margin)
    bottom_left = (margin, height - margin)
    bottom_right = (width - margin, height - margin)
    draw(top, bottom_left, bottom_right, 0)
    save(scene, "recipes/gem-sierpinski.svg")


# ── 4. Phyllotaxis (Golden Angle Spiral) ───────────────────────────────


def _generate_phyllotaxis(size=400, n_dots=900):
    scene = Scene(size, size, background="#080810")
    cx, cy = size / 2, size / 2
    golden_angle = 137.508
    max_r = size / 2 - 12

    for i in range(1, n_dots + 1):
        angle = math.radians(i * golden_angle)
        r = max_r * math.sqrt(i / n_dots)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)

        t = r / max_r
        radius = 5.0 * (1 - t * 0.55) + 1.0
        color = hsl((50 - t * 170) % 360, 0.88, 0.54 - t * 0.1)
        scene.place(Dot(x, y, radius=radius, color=color, opacity=0.92))

    save(scene, "recipes/gem-phyllotaxis.svg")


# ── 5. Voronoi Portrait (image-based) ────────────────────────────────


def _clip_polygon(verts, x0, y0, x1, y1):
    """Sutherland-Hodgman clip a polygon to an axis-aligned rectangle."""
    def _clip_edge(poly, inside, intersect):
        if not poly:
            return []
        out = []
        prev = poly[-1]
        for curr in poly:
            if inside(curr):
                if not inside(prev):
                    out.append(intersect(prev, curr))
                out.append(curr)
            elif inside(prev):
                out.append(intersect(prev, curr))
            prev = curr
        return out

    def lerp(a, b, t):
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

    p = list(verts)
    for inside, isect in [
        (lambda v: v[0] >= x0, lambda a, b: lerp(a, b, (x0 - a[0]) / (b[0] - a[0]))),
        (lambda v: v[0] <= x1, lambda a, b: lerp(a, b, (x1 - a[0]) / (b[0] - a[0]))),
        (lambda v: v[1] >= y0, lambda a, b: lerp(a, b, (y0 - a[1]) / (b[1] - a[1]))),
        (lambda v: v[1] <= y1, lambda a, b: lerp(a, b, (y1 - a[1]) / (b[1] - a[1]))),
    ]:
        p = _clip_edge(p, inside, isect)
    return p


def _generate_voronoi_portrait(grid_size=100, cell_size=5, density=0.7, seed=42):
    from scipy.spatial import Voronoi
    random.seed(seed)
    bg = "#f4f1eb"
    data_scene = Scene.from_image(
        sample_image("MonaLisa.jpg"),
        grid_size=grid_size, cell_size=cell_size, background=bg,
    )
    g = data_scene.grid
    W, H = int(data_scene.width), int(data_scene.height)

    # Grid-based seeding: walk every cell, place seeds proportional to darkness
    seeds = []
    seed_colors = []
    for cell in g:
        darkness = 1.0 - cell.brightness
        expected = density * darkness ** 3
        n = int(expected) + (1 if random.random() < (expected % 1) else 0)
        cx, cy, cw, ch = cell.bounds
        for _ in range(n):
            seeds.append((cx + random.random() * cw, cy + random.random() * ch))
            seed_colors.append(cell.color)
    n_seeds = len(seeds)

    # Mirror seeds so edge cells are bounded
    pts = list(seeds)
    for x, y in seeds:
        pts.extend([(-x, y), (2 * W - x, y), (x, -y), (x, 2 * H - y)])
    vor = Voronoi(pts)

    # Draw stroke-only polygons colored by the underlying image
    scene = Scene(W, H, background=bg)
    for i in range(n_seeds):
        region = vor.regions[vor.point_region[i]]
        if not region or -1 in region:
            continue
        verts = [(vor.vertices[v][0], vor.vertices[v][1]) for v in region]
        verts = _clip_polygon(verts, 0, 0, W, H)
        if len(verts) < 3:
            continue
        scene.place(
            Polygon(verts, fill=None, stroke=seed_colors[i], stroke_width=0.4)
        )

    save(scene, "recipes/gem-voronoi.svg")


# ── 6. Double-Slit Experiment ────────────────────────────────────────


def _generate_double_slit(
    cols=120, rows=80, cell_size=6, wavelength=8,
    slit_separation=16, slit_width=3, barrier_col=25,
):
    bg = "#f4f1eb"
    scene = Scene.with_grid(
        cols=cols, rows=rows, cell_size=cell_size, background=bg
    )
    g = scene.grid

    slit1 = rows // 2 - slit_separation // 2
    slit2 = rows // 2 + slit_separation // 2
    k = 2 * math.pi / wavelength

    for cell in g:
        cell.data["wall"] = False
        cell.data["amplitude"] = 0.0

    # Build barrier with two slits
    for row in range(rows):
        if abs(row - slit1) > slit_width and abs(row - slit2) > slit_width:
            g[row][barrier_col].data["wall"] = True

    # Compute wave field
    for cell in g:
        if cell.data["wall"]:
            continue
        px = (cell.col + 0.5) * cell_size
        py = (cell.row + 0.5) * cell_size

        if cell.col <= barrier_col:
            cell.data["amplitude"] = math.sin(k * px)
        else:
            amp = 0.0
            for sc in (slit1, slit2):
                for dr in range(-slit_width, slit_width + 1):
                    sx = (barrier_col + 0.5) * cell_size
                    sy = (sc + dr + 0.5) * cell_size
                    d = math.hypot(px - sx, py - sy)
                    if d > 0.1:
                        amp += math.sin(k * (sx + d)) / math.sqrt(d)
            cell.data["amplitude"] = amp

    # Normalize
    max_amp = max(abs(c.data["amplitude"]) for c in g if not c.data["wall"])
    if max_amp > 0:
        for cell in g:
            if not cell.data["wall"]:
                cell.data["amplitude"] /= max_amp

    # Draw: dots sized by |psi|^2, colored by phase
    for cell in g:
        if cell.data["wall"]:
            cell.add_fill(color="#3a3a4a", z_index=0)
        else:
            a = cell.data["amplitude"]
            intensity = a ** 2
            if intensity > 0.01:
                hue = 220 if a >= 0 else 350
                radius = 0.1 + 0.35 * intensity ** 0.3
                cell.add_dot(
                    radius=radius, color=hsl(hue, 0.75, 0.35),
                    opacity=0.3 + intensity * 0.65, z_index=1,
                )

    save(scene, "recipes/gem-double-slit.svg")
