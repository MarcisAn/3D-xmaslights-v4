import time
import sys

import requests

def clamp(x):
    return max(0, min(x, 255))


class AnimationBuilder:
    frames = []
    light_state = []

    def __init__(self, led_count) -> None:
        for _ in range(led_count):
            self.light_state.append((0,0,0))

    def light(self, index, red, green, blue):
        self.light_state[index] = (clamp(red), clamp(green), clamp(blue))

    def update(self):
        self.frames.append(self.light_state.copy())

    def pack_bytes(self):
        color_bytes = []
        for frame in self.frames:
            for led in frame:
                for v in led:
                    color_bytes.append(clamp(v))
                    
        return color_bytes


builder = AnimationBuilder(400)

for i in range(400):
    if i > 200:
        builder.light(i,0,0,255)
    else:
        builder.light(i, 0, 255 , 0)
    builder.update()


requests.post(
    "http://localhost:3000/animationIsGenerated",
    data=bytearray(builder.pack_bytes()),
)
