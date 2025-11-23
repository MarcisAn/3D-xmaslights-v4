import random
from AnimationBuilder import AnimationBuilder
import math
import random


class LoopingBallParticle:
    def __init__(self, bounds, radius_range=(30.1, 100.3), loop_time=5.0):
        xmin, xmax, ymin, ymax, zmin, zmax = bounds

        # Base rest position
        self.x0 = random.uniform(xmin, xmax)
        self.y0 = random.uniform(ymin, ymax)
        self.z0 = random.uniform(zmin, zmax)

        # Radius
        self.radius = random.uniform(*radius_range)

        # Amplitudes of swinging motion
        self.ax = random.uniform(30.2, 100.0)
        self.ay = random.uniform(30.2, 100.0)
        self.az = random.uniform(30.2, 100.0)

        # Random phases
        self.phx = random.uniform(0, 2 * math.pi)
        self.phy = random.uniform(0, 2 * math.pi)
        self.phz = random.uniform(0, 2 * math.pi)

        # Loop frequency
        self.omega = 2 * math.pi / loop_time

    def update(self, t):
        """Update particle position based on looped time t."""
        self.x = self.x0 + self.ax * math.sin(self.omega * t + self.phx)
        self.y = self.y0 + self.ay * math.sin(self.omega * t + self.phy)
        self.z = self.z0 + self.az * math.sin(self.omega * t + self.phz)

    def contains_point(self, point):
        px, py, pz = point
        dx = px - self.x
        dy = py - self.y
        dz = pz - self.z
        return dx * dx + dy * dy + dz * dz <= self.radius * self.radius


class LoopingParticleSystem:

    def __init__(
        self, count=10000, bounds=(-200, 200, -200, 200, -200, 400), loop_time=5.0
    ):
        self.particles = [
            LoopingBallParticle(bounds, loop_time=loop_time) for _ in range(count)
        ]
        self.t = 0.0
        self.loop_time = loop_time

    def update(self, dt):
        # Loop time between 0 and loop_time
        self.t = (self.t + dt) % self.loop_time

        for p in self.particles:
            p.update(self.t)

    def is_point_inside_any_particle(self, point):
        return any(p.contains_point(point) for p in self.particles)

    def get_positions(self):
        return [(p.x, p.y, p.z, p.radius) for p in self.particles]


system = LoopingParticleSystem(count=10)
INTERVAL_MS = 20
builder = AnimationBuilder(INTERVAL_MS)

# simulate some frames
for _ in range(300):
    system.update(5.00 / 300)
    for i in range(400):
        if system.is_point_inside_any_particle((builder.cords[i][0], builder.cords[i][1], builder.cords[i][2])):
            builder.light(i, 255, -builder.cords[i][2] + 100, 0)
        else:
            builder.light(i, 0, 0, 0)
    builder.update()

builder.done()
