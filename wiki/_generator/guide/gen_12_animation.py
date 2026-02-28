"""Generate animated SVGs for Guide: Animation.

Every SVG here uses real SMIL animations — open in a browser to see them play.
"""

from __future__ import annotations

import math

from pyfreeform import Connection, Dot, Rect, Scene, Path as PPath, Easing
from pyfreeform.entities.text import Text
from pyfreeform.entities.line import Line
from pyfreeform.paths import Wave, Zigzag

from wiki._generator import save


def generate():
    # --- 1. Fade: coral dot fading out ---
    scene = Scene(240, 160, background="#1a1a2e")
    dot = Dot(120, 70, radius=35, color="coral")
    scene.place(dot)
    dot.fade(to=0.0, duration=3.0, easing="ease-in-out")
    scene.place(Text(120, 140, ".fade(to=0.0, duration=3.0)", font_size=11, color="gray"))
    save(scene, "guide/anim-fade.svg")

    # --- 2. Spin: blue rect spinning forever ---
    scene = Scene(240, 160, background="#1a1a2e")
    rect = Rect.at_center((120, 70), 65, 65, fill="dodgerblue", stroke="white", stroke_width=2)
    scene.place(rect)
    rect.spin(360, duration=2.5, repeat=True, easing="linear")
    scene.place(Text(120, 140, ".spin(360, repeat=True)", font_size=11, color="gray"))
    save(scene, "guide/anim-spin.svg")

    # --- 3. Draw: wave drawing itself ---
    scene = Scene(360, 140, background="#1a1a2e")
    wave = PPath(
        Wave(start=(30, 55), end=(330, 55), amplitude=30, frequency=3),
        width=3, color="limegreen",
    )
    scene.place(wave)
    wave.draw(duration=2.5, easing="ease-in-out")
    scene.place(Text(180, 120, ".draw(duration=2.5)", font_size=11, color="gray"))
    save(scene, "guide/anim-draw.svg")

    # --- 4. Easing: four dots racing across with different curves ---
    scene = Scene(440, 210, background="#1a1a2e")
    easing_names = ["linear", "ease-in", "ease-out", "ease-in-out"]
    colors = ["coral", "gold", "skyblue", "mediumpurple"]
    for i, (name, color) in enumerate(zip(easing_names, colors)):
        y = 35 + i * 45
        # Label centered in the left margin
        scene.place(Text(55, y, name, font_size=12, color="gray"))
        # Track line
        scene.place(Line(120, y, 420, y, width=1, color="#333"))
        # Dot that slides from left to right
        d = Dot(120, y, radius=10, color=color)
        scene.place(d)
        d.animate("cx", to=420, duration=3.0, easing=name, repeat=True)
    scene.place(Text(220, 200, "all move the same distance in 3s", font_size=10, color="#555"))
    save(scene, "guide/anim-easing.svg")

    # --- 5. Chaining: rect that fades AND spins ---
    scene = Scene(240, 160, background="#1a1a2e")
    rect = Rect.at_center((120, 70), 60, 60, fill="mediumpurple", stroke="white", stroke_width=1)
    scene.place(rect)
    rect.fade(to=0.3, duration=2.0, easing="ease-in-out")
    rect.spin(360, duration=3.0, repeat=True)
    scene.place(Text(120, 140, ".fade(to=0.3).spin(360)", font_size=11, color="gray"))
    save(scene, "guide/anim-chaining.svg")

    # --- 6. Connection draw: curve drawing between dots ---
    scene = Scene(360, 120, background="#1a1a2e")
    d1 = Dot(40, 50, radius=7, color="white")
    d2 = Dot(320, 50, radius=7, color="white")
    scene.place(d1)
    scene.place(d2)
    conn = Connection(d1, d2, curvature=0.4, color="skyblue", width=2)
    conn.draw(duration=2.0, easing="ease-in-out")
    scene.place(Text(180, 105, "conn.draw(duration=2.0)", font_size=11, color="gray"))
    save(scene, "guide/anim-connection.svg")

    # --- 7. Generic animate: pulsing dot (radius) ---
    scene = Scene(240, 160, background="#1a1a2e")
    pulse = Dot(120, 70, radius=10, color="coral")
    scene.place(pulse)
    pulse.animate("r", to=35, duration=1.2, easing="ease-in-out", repeat=True, bounce=True)
    scene.place(Text(120, 140, '.animate("r", to=35, bounce=True)', font_size=10, color="gray"))
    save(scene, "guide/anim-animate.svg")

    # --- 8. Showcase: everything together ---
    scene = Scene(460, 300, background="#1a1a2e")

    # Self-drawing connection across the top
    da = Dot(30, 35, radius=4, color="white")
    db = Dot(430, 35, radius=4, color="white")
    scene.place(da)
    scene.place(db)
    cn = Connection(da, db, curvature=0.3, color="coral", width=2)
    cn.draw(duration=2.0, delay=0.3, easing="ease-in-out")

    # Spinning rect with fade
    r1 = Rect.at_center((80, 130), 50, 50, fill="mediumpurple", stroke="white", stroke_width=1)
    scene.place(r1)
    r1.spin(360, duration=3.0, repeat=True)
    r1.fade(to=0.3, duration=2.0, easing="ease-in-out")

    # Pulsing dot
    d_pulse = Dot(200, 130, radius=8, color="coral")
    scene.place(d_pulse)
    d_pulse.animate("r", to=28, duration=1.5, easing="ease-in-out", repeat=True, bounce=True)

    # Fading dot
    d_fade = Dot(340, 130, radius=22, color="gold")
    scene.place(d_fade)
    d_fade.fade(to=0.0, duration=3.0, easing="ease-in-out")

    # Self-drawing zigzag
    zz = PPath(
        Zigzag(start=(30, 230), end=(220, 230), amplitude=22, teeth=5),
        width=2, color="skyblue",
    )
    scene.place(zz)
    zz.draw(duration=2.0, easing="ease-in-out")

    # Self-drawing wave
    w2 = PPath(
        Wave(start=(240, 230), end=(440, 230), amplitude=22, frequency=3),
        width=2, color="limegreen",
    )
    scene.place(w2)
    w2.draw(duration=2.5, delay=0.5, easing="ease-in-out")

    # Row of spinning squares
    sq_colors = ["coral", "gold", "skyblue", "limegreen", "mediumpurple"]
    for i, c in enumerate(sq_colors):
        x = 100 + i * 70
        sq = Rect.at_center((x, 280), 14, 14, fill=c)
        scene.place(sq)
        sq.spin(360, duration=1.5 + i * 0.3, repeat=True, easing="linear")

    save(scene, "guide/anim-showcase.svg")


if __name__ == "__main__":
    generate()
