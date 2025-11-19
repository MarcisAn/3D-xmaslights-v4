import time
import sys
import csv
import requests

def clamp(x):
    return max(0, min(x, 255))


class AnimationBuilder:
    frames = []
    light_state = []
    cords = []

    def __init__(self, frame_interval_ms) -> None:
        for _ in range(400):
            self.light_state.append((0,0,0))
        with open("../../data/cords.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            cords = []
            for row in reader:
                cords.append((int(row["x"]), int(row["y"]), int(row["z"])))
            self.cords = cords
        self.interval = frame_interval_ms

    def light(self, index, red, green, blue):
        self.light_state[index] = (clamp(red), clamp(green), clamp(blue))

    def update(self):
        self.frames.append(self.light_state.copy())

    def wait(self, number_of_frames):
        for _ in range(number_of_frames):
            self.frames.append(self.light_state.copy())

    def done(self):
        color_bytes = []
        for frame in self.frames:
            for led in frame:
                for v in led:
                    color_bytes.append(clamp(v))

        print(len(color_bytes))
        req = requests.post(
            # "https://ledserver.andersons-m.lv/animationIsGenerated",
            "http://localhost:3000/animationIsGenerated",
            data=bytearray(color_bytes),
        )
        requests.post(
            # "https://ledserver.andersons-m.lv/setAnimationSpeed",
            "http://localhost:3000/setAnimationSpeed",
            json={"interval": self.interval},
        )
        print(req.status_code)
