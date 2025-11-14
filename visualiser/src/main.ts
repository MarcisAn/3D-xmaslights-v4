import { all_to_black, createScene, changeLED } from "./counter";
import "./style.css";
import { io } from "socket.io-client";
import { CanvasRecorder } from "./CanvasRecorder.ts";

let server_url = "";
if (import.meta.env.PROD) {
  server_url = "wss://ledserver.andersons-m.lv";
} else {
  server_url = "ws://localhost:3000";
}
// server_url = "wss://ledserver.andersons-m.lv";
const socket = io(server_url, {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 1000,
  reconnectionDelay: 30,
  transports: ["websocket"],
});
let record = false;

let anim_speed = 90;

const LED_COUNT = 400;
socket.on("animationData", (data) => {
  recieveAnimation(data);
});
socket.on("animationSpeed", (data) => {
  anim_speed = data
});
let intervalhandle;

function recieveAnimation(data) {
  const view = new Uint8Array(data);
  const frame_count = view.length / (LED_COUNT * 3);
  for (let frame = 0; frame < frame_count; frame++) {}
  let frame = 0;
  clearInterval(intervalhandle);  
  intervalhandle = setInterval(() => {
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
  }, Math.pow(anim_speed, -1) * 400);
}

// socket.on("reciveAnimation", (data) => {
//   clearInterval(intervalId);
//   if (record) {
//     alert("RECORD START");
//     recording = true;
//     recorder.start();
//   }
//   anim_speed = data.speed;
//   frame = 0;
//   all_to_black();
//   anim_data = [];
//   data.animation.forEach((frame: string) => {
//     let tree_data: number[][] = [];
//     let light_data: number[] = [];
//     let char_index = 0; // indekss baitam, kuru pašlaik apskatām: 0-lampiņas idekss, 1-red, 2-green, 3-blue
//     frame.split("").forEach(function (c: string) {
//       light_data.push(c.charCodeAt(0));
//       char_index++;
//       if (char_index == 4) {
//         char_index = 0;
//         tree_data.push(light_data);
//         light_data = [];
//       }
//     });
//     anim_data.push(tree_data);
//   });
//   intervalId = window.setInterval(function () {
//     if (anim_data.length > 0) {
//       renderVis(anim_data[frame]);
//     }
//     frame++;

//     if (frame == anim_data.length) {
//       if (record && recording) {
//         recorder.stop();
//         recorder.save();
//         record = false;
//       }
//       frame = 0;
//     }
//     //console.log(Math.pow(anim_speed, -1)*400)
//   }, Math.pow(anim_speed, -1) * 400);
// });

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
