import math
import colorsys
from AnimationBuilder import AnimationBuilder

INTERVAL_MS = 15
builder = AnimationBuilder(INTERVAL_MS)

NUM_LEDS = len(builder.cords)

# -------------------------------
# Parameters
# -------------------------------
NUM_HELICES = 1  # how many helix strands
HELIX_RADIUS = 20.3  # distance from center for LEDs to be lit
HELIX_THICKNESS = 20.15  # how far an LED can deviate from the helix to light
HELIX_TURNS = 3  # number of turns from bottom to top
HELIX_SPEED = 0.12  # rotation speed per frame (radians)
TOTAL_FRAMES = 900
HUE_SPEED = 0.005  # amount hue shifts per frame

# Find min/max Z in your tree
MIN_Z = min(builder.cords[i][2] for i in range(NUM_LEDS))
MAX_Z = max(builder.cords[i][2] for i in range(NUM_LEDS))
Z_RANGE = MAX_Z - MIN_Z

# Initialize hue offsets per helix
hue_offsets = [i / NUM_HELICES for i in range(NUM_HELICES)]

# -------------------------------
# Main loop
# -------------------------------
for frame in range(TOTAL_FRAMES):

    # Clear LEDs
    for i in range(NUM_LEDS):
        builder.light(i, 0, 0, 0)

    for h in range(NUM_HELICES):
        phase_offset = (2 * math.pi / NUM_HELICES) * h  # angular offset
        rotation = frame * HELIX_SPEED
        hue_offset = (hue_offsets[h] + frame * HUE_SPEED) % 1.0  # rainbow shift

        for i in range(NUM_LEDS):
            x, y, z = builder.cords[i]

            # normalize Z from 0..1
            t = (z - MIN_Z) / Z_RANGE

            # compute target angle along helix
            angle = t * HELIX_TURNS * 2 * math.pi + rotation + phase_offset

            # convert polar to Cartesian
            hx = HELIX_RADIUS * math.cos(angle)
            hy = HELIX_RADIUS * math.sin(angle)

            # distance from LED to helix path
            dx = x - hx
            dy = y - hy
            dist = math.sqrt(dx * dx + dy * dy)

            if dist <= HELIX_THICKNESS:
                # compute hue along the helix
                hue = (t + hue_offset) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                r_i = int(r * 255)
                g_i = int(g * 255)
                b_i = int(b * 255)
                builder.light(i, r_i, g_i, b_i)

    builder.update()

builder.done()
