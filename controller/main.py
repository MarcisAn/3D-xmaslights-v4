
import time
import os
import socketio
from rpi_ws281x import PixelStrip, ws, Color


try:
    os.sched_setaffinity(0, {2})
    print("Pinned process to CPU core 2")
except Exception as e:
    print("CPU affinity not set:", e)
    
    
try:
    os.nice(-10)
    print("Increased process priority")
except:
    print("Could not set high priority")

# ============================================================
# LED STRIP CONFIGURATION
# ============================================================
LED_COUNT = 400
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    strip_type=ws.WS2811_STRIP_GRB,
)
strip.begin()

led_buffer = None

if hasattr(strip, "_leds"):
    led_buffer = strip._leds

elif hasattr(strip, "_led_data"):
    led_buffer = strip._led_data

elif hasattr(strip, "_channel") and hasattr(strip._channel, "leds"):
    led_buffer = strip._channel.leds


# ============================================================
# SERVER SETUP
# ============================================================
SERVER_URL = "wss://ledserver.andersons-m.lv"

sio = socketio.Client(
    reconnection=True, reconnection_attempts=1000, reconnection_delay=0.03
)

# ============================================================
# ANIMATION STATE
# ============================================================
view = None
frame = 0
frame_count = 0

# nanoseconds per tick
TICK_INTERVAL_NS = 40 * 1000000  # ≥8ms safety


def update_tick_interval(interval):
    global TICK_INTERVAL_NS
    TICK_INTERVAL_NS = interval * 1000000  # 8ms minimum


# ============================================================
# SOCKET.IO EVENT HANDLERS
# ============================================================


@sio.on("animationData")
def on_animation_data(data):
    global view, frame_count, frame

    view = bytearray(data)
    frame_bytes = LED_COUNT * 3

    if len(view) % frame_bytes != 0:
        print("ERROR: Animation size mismatch!")
        view = None
        return

    frame_count = len(view) // frame_bytes
    frame = 0

    print(f"Received animation: {frame_count} frames")


@sio.on("animationSpeed")
def on_animation_speed(data):
    update_tick_interval(int(data))
    print(f"Speed updated → {data}")


def animation_frame():
    global frame

    if view is None:
        return

    offset = frame * (LED_COUNT * 3)

    for i in range(LED_COUNT):
        base = offset + i * 3
        r = view[base]
        g = view[base + 1]
        b = view[base + 2]
        strip.setPixelColor(i, Color(g, r, b))

    strip.show()

    frame += 1
    if frame >= frame_count:
        frame = 0


def loop():
    next_tick = time.perf_counter()

    while True:
        now = time.perf_counter_ns()

        # Time for next frame?
        if now >= next_tick:
            animation_frame()

            next_tick += TICK_INTERVAL_NS

            # If we fell behind by more than one frame → resync
            if now - next_tick > TICK_INTERVAL_NS:
                next_tick = now + TICK_INTERVAL_NS

        # micro-sleep to reduce CPU jitter but keep high precision
        time.sleep(0.0004)


print("Connecting to server...")
sio.connect(SERVER_URL)
print("Connected. Starting high-precision loop...")

loop()
