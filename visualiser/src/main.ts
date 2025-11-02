import { all_to_black, createScene, renderVis } from "./counter";
import "./style.css";
import { io } from "socket.io-client";
import { CanvasRecorder } from "./CanvasRecorder.ts";

let server_url = "";
if (import.meta.env.PROD) {
  server_url = "wss://lampinas-server.cvgmerch.lv";
} else {
  server_url = "ws://localhost:3000";
}
const socket = io(server_url, {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 1000,
  reconnectionDelay: 30,
  transports: ["websocket"],
});
let anim_data: any[] = [];
let anim_speed = 10;
let record = false;
let recording = false;
let frame = 0;
let intervalId: number;

function unpack5BitValues(arrayBuffer: ArrayBuffer, count: number) {
  const bytes = new Uint8Array(arrayBuffer);
  let bitString = 0n; // use BigInt for safety
  for (const b of bytes) {
    bitString = (bitString << 8n) | BigInt(b);
  }

  const totalBits = BigInt(count * 5);
  let shift = totalBits - 5n;
  const values = [];

  for (let i = 0; i < count; i++) {
    const value = Number((bitString >> shift) & 0x1Fn); // 0x1F = 5 bits mask
    values.push(value);
    shift -= 5n;
  }

  return values;
}

socket.on("animationData", (data) => {
  console.log(unpack5BitValues(data, 2*400*2));
});


socket.on("reciveAnimation", (data) => {
  clearInterval(intervalId);
  if (record) {
    alert("RECORD START");
    recording = true;
    recorder.start();
  }
  anim_speed = data.speed;
  frame = 0;
  all_to_black();
  anim_data = [];
  data.animation.forEach((frame: string) => {
    let tree_data: number[][] = [];
    let light_data: number[] = [];
    let char_index = 0; // indekss baitam, kuru pašlaik apskatām: 0-lampiņas idekss, 1-red, 2-green, 3-blue
    frame.split("").forEach(function (c: string) {
      light_data.push(c.charCodeAt(0));
      char_index++;
      if (char_index == 4) {
        char_index = 0;
        tree_data.push(light_data);
        light_data = [];
      }
    });
    anim_data.push(tree_data);
  });
  intervalId = window.setInterval(function () {
    if (anim_data.length > 0) {
      renderVis(anim_data[frame]);
    }
    frame++;

    if (frame == anim_data.length) {
      if (record && recording) {
        recorder.stop();
        recorder.save();
        record = false;
      }
      frame = 0;
    }
    //console.log(Math.pow(anim_speed, -1)*400)
  }, Math.pow(anim_speed, -1) * 400);
});

let html = ``;
if (process.env.NODE_ENV == "development") {
  html = `

  <button id="savevideo">save video</button>
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
