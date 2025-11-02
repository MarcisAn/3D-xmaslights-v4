import sys

def clamp(x):
    return max(0, min(x, 100))


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
        bitstring = 0
        bitlen = 0
        for frame in self.frames:
            for led in frame:
                for v in led:
                    if not 0 <= v < 32:
                        raise ValueError(f"Value {v} out of 5-bit range (0–31)")
                    bitstring = (bitstring << 5) | v
                    bitlen += 5

        # Round up to nearest byte
        num_bytes = (bitlen + 7) // 8
        return bitstring.to_bytes(num_bytes, 'big')


builder = AnimationBuilder(2)

builder.light(0,0,0,1)
builder.update()
builder.light(1, 1, 0, 1)
builder.update()


# print(builder.frames)
# print(builder.pack_bytes())

sys.stdout.buffer.write(builder.pack_bytes())
sys.stdout.flush()

with open("led_data.bin", "wb") as f:
    f.write(builder.pack_bytes())
