import random
from AnimationBuilder import AnimationBuilder

INTERVAL_MS = 15
builder = AnimationBuilder(INTERVAL_MS)

NUM_LEDS = len(builder.cords)

# -------------------------------
# Parameters
# -------------------------------
PILLAR_SPAWN_PROB = 0.05  # chance to spawn a new pillar each frame
PILLAR_SPEED = 1  # units per frame along Z
PILLAR_LENGTH = 100  # height of pillar in coordinate units
MAX_PILLARS = 1
TOTAL_FRAMES = 900

# Color options (you can change or randomize)
COLORS = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0),  # yellow
    (0, 255, 255),  # cyan
]


# -------------------------------
# Pillar object
# -------------------------------
class FallingPillar:
    def __init__(self):
        # pick random LED as spawn position
        self.x = random.randrange(-30,30)
        self.y = random.randrange(-30, 30)

        self.z = 140.0
        self.length = PILLAR_LENGTH
        self.speed = PILLAR_SPEED
        self.dead = False
        self.color = random.choice(COLORS)

    def update(self):
        self.z -= self.speed  # falling down
        # If the pillar is fully below min Z, mark as dead
        min_z = min(builder.cords[i][2] for i in range(NUM_LEDS))
        if self.z + self.length < min_z:
            self.dead = True


# Active pillars
pillars = []

# -------------------------------
# Main animation loop
# -------------------------------
for frame in range(TOTAL_FRAMES):

    # Spawn new pillars
    if len(pillars) < MAX_PILLARS and random.random() < PILLAR_SPAWN_PROB:
        pillars.append(FallingPillar())

    # Clear LEDs
    for i in range(NUM_LEDS):
        builder.light(i, 0, 0, 0)

    # Update pillars and light LEDs
    updated = []
    for pillar in pillars:
        pillar.update()
        if pillar.dead:
            continue
        updated.append(pillar)

        px, py, pz = pillar.x, pillar.y, pillar.z
        r_c, g_c, b_c = pillar.color

        for i in range(NUM_LEDS):
            x, y, z = builder.cords[i]

            # Check if LED is in the vertical pillar column
            # small horizontal radius for “thickness”
            if (
                abs(x - px) < 20
                and abs(y - py) < 20
                and pz <= z <= pz + pillar.length
            ):
                builder.light(i, r_c, g_c, b_c)

    pillars = updated
    builder.update()

builder.done()
