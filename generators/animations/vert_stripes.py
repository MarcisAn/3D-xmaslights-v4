import random
import colorsys
from AnimationBuilder import AnimationBuilder

INTERVAL_MS = 15
builder = AnimationBuilder(INTERVAL_MS)

NUM_LEDS = len(builder.cords)

# -------------------------------
# Parameters
# -------------------------------
NUM_STRIPES = 5  # number of vertical stripes
STRIPE_SPEED = 0.45  # units per frame (move up)
STRIPE_WIDTH = 100.15  # horizontal width of each stripe
STRIPE_LENGTH = 10.6  # vertical length of stripe
TOTAL_FRAMES = 500
HUE_SPEED = 0.005  # amount hue shifts per frame

# Find min/max Z in your tree for wrapping
MIN_Z = min(builder.cords[i][2] for i in range(NUM_LEDS))
MAX_Z = max(builder.cords[i][2] for i in range(NUM_LEDS))
Z_RANGE = MAX_Z - MIN_Z


# -------------------------------
# Stripe object
# -------------------------------
class RainbowStripe:
    def __init__(self):
        idx = random.randrange(NUM_LEDS)
        self.x, self.y, _ = builder.cords[idx]
        self.z = random.uniform(MIN_Z, MAX_Z)
        self.hue = random.random()  # initial hue 0..1

    def update(self):
        self.z += STRIPE_SPEED
        if self.z > MAX_Z:
            self.z = MIN_Z
        # shift hue for rainbow effect
        self.hue += HUE_SPEED
        if self.hue > 1.0:
            self.hue -= 1.0

    def get_rgb(self):
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        # convert to 0..255 integers
        return int(r * 255), int(g * 255), int(b * 255)


# Initialize stripes
stripes = [RainbowStripe() for _ in range(NUM_STRIPES)]

# -------------------------------
# Main animation loop
# -------------------------------
for frame in range(TOTAL_FRAMES):

    # Clear LEDs
    for i in range(NUM_LEDS):
        builder.light(i, 0, 0, 0)

    # Update stripes and light LEDs
    for stripe in stripes:
        stripe.update()
        sx, sy, sz = stripe.x, stripe.y, stripe.z
        r_c, g_c, b_c = stripe.get_rgb()

        for i in range(NUM_LEDS):
            x, y, z = builder.cords[i]

            # Horizontal proximity check
            if abs(x - sx) < STRIPE_WIDTH and abs(y - sy) < STRIPE_WIDTH:
                # Vertical wrapping for moving stripe
                dz = z - sz
                if dz < 0:
                    dz += Z_RANGE
                if dz <= STRIPE_LENGTH:
                    builder.light(i, r_c, g_c, b_c)

    builder.update()

builder.done()
