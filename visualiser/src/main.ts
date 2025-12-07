import { all_to_black, createScene, changeLED } from "./counter";
import "./style.css";
import { io } from "socket.io-client";
import { CanvasRecorder } from "./CanvasRecorder.ts";
import pako from "pako";

let server_url = "";
if (import.meta.env.PROD) {
  server_url = "wss://ledserver.andersons-m.lv";
} else {
  server_url = "ws://localhost:3000";
}
server_url = "wss://ledserver.andersons-m.lv";
const socket = io(server_url, {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 1000,
  reconnectionDelay: 30,
  transports: ["websocket"],
});
let record = false;

const LED_COUNT = 400;
socket.on("animationData", (data) => {
  recieveAnimation(data);
});
socket.on("animationSpeed", (data) => {
  TICK_INTERVAL = data;
});

let frame_count;
let view;
let frame = 0;
let TICK_INTERVAL = 40;
function recieveAnimation(data) {
  const comp_view = new Uint8Array(data);
  view = pako.ungzip(comp_view);
  frame_count = view.length / (LED_COUNT * 3);
  frame = 0;
}

function animation_frame() {
  for (let led = 0; led < LED_COUNT; led++) {
    const red = led * 3 + frame * LED_COUNT * 3;
    changeLED(led, view[red], view[red + 1], view[red + 2]);
  }
  if (frame == frame_count - 1) {
    frame = 0;
    return;
  } else {
    frame++;
  }
}

let nextTick = performance.now() + TICK_INTERVAL;

function loop() {
  const now = performance.now();
  if (now >= nextTick) {
    if (view) {
      animation_frame();
    }

    nextTick += TICK_INTERVAL;
    if (now - nextTick > TICK_INTERVAL) {
      nextTick = now + TICK_INTERVAL;
    }
  }

  // Keep looping as fast as possible
  requestAnimationFrame(loop);
}
loop();

let html = ``;
if (process.env.NODE_ENV == "development") {
  html = `
  <button id="savevideo">RECORD</button>
  <canvas id="canvas">
  </canvas>
`;
} else {
  html = `
  <canvas id="canvas">
  </canvas>
`;
}

document.querySelector<HTMLDivElement>("#app")!.innerHTML = html;
document.getElementById("savevideo")?.addEventListener("click", () => {
  record = true;
});
createScene(document.getElementById("canvas"));
//@ts-ignore
const recorder = new CanvasRecorder(
  //@ts-ignore
  document.getElementById("canvas"),
  4200000
);
