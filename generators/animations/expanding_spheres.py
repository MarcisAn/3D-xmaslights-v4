import random
import math
from AnimationBuilder import AnimationBuilder

INTERVAL_MS = 15
builder = AnimationBuilder(INTERVAL_MS)

NUM_LEDS = len(builder.cords)

# -------------------------------
# Parameters
# -------------------------------
SPHERE_SPAWN_PROB = 0.04  # chance to spawn a new sphere each frame
SPHERE_MAX_RADIUS = 100.6
SPHERE_GROW_RATE = 1
MAX_SPHERES = 1
TOTAL_FRAMES = 900


# -------------------------------
# Sphere object
# -------------------------------
class ExpandingSphere:
    def __init__(self, color):
        idx = random.randrange(NUM_LEDS)
        self.cx, self.cy, self.cz = builder.cords[idx]
        self.radius = 0.0
        self.dead = False
        self.color = color

    def update(self):
        self.radius += SPHERE_GROW_RATE
        if self.radius > SPHERE_MAX_RADIUS:
            self.dead = True


spheres = []

colors = [
    (0, 160, 255),
    (255, 0, 160),
    (0, 255, 177),
    (255, 112, 10),
]

# -------------------------------
# Main loop
# -------------------------------
for frame in range(TOTAL_FRAMES):

    # Spawn new spheres
    if len(spheres) < MAX_SPHERES and random.random() < SPHERE_SPAWN_PROB:
        color = random.choice(colors)
        spheres.append(ExpandingSphere(color))

    # Clear LEDs
    for i in range(NUM_LEDS):
        builder.light(i, 0, 0, 0)

    # Update spheres and light LEDs
    updated = []
    for sph in spheres:
        sph.update()
        if sph.dead:
            continue
        updated.append(sph)
        color = sph.color
        for i in range(NUM_LEDS):
            x, y, z = builder.cords[i]
            dx = x - sph.cx
            dy = y - sph.cy
            dz = z - sph.cz
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)

            if dist <= sph.radius:
                # FULL sphere: brightness highest at center, fades to edge
                t = dist / sph.radius
                brightness = 1.0 - (t * t)  # smooth quadratic fade

                
                # Color: cyan glow
                r = int(color[0]* brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)

                builder.light(i, r, g, b)

    spheres = updated
    builder.update()

builder.done()
