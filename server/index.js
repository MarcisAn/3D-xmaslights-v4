const express = require("express");
const { createServer } = require("node:http");
const { join } = require("node:path");
const { Server } = require("socket.io");
const cors = require("cors");
const { log } = require("node:console");
const spawn = require("child_process").spawn;
const fs = require("fs");
var bodyParser = require("body-parser");

const animations = require("../data/animations.json");

// Server config
const app = express();
app.use(cors());
app.use(express.json());
app.use(bodyParser.raw({ type: "application/octet-stream", limit: "2mb" }));
const server = createServer(app);
const io = new Server(server);

// Store the socket objects for active connections
let sockets = [];
// Store the active animation speed
let frame_interval = 40;

// Called when user picks an animation to play
app.post("/pickAnim", (req, res) => {
  console.log(req.body.name);
  const animation = (result = animations.filter((obj) => {
    return obj.name === req.body.name;
  }));
  console.log(anim);
  
  if (!animation) {
    res.status(400).end();
    return;
  }
  const pythonProcess = spawn("python", [
    "../generators/animations/" + animation.name + ".py"
  ]);
  console.log(pythonProcess.stdout);
  
  console.log("socket count: " + sockets.length);

  res.status(200).end();
});

// Caled by the generator when animation is generated and can be sent out to clients
app.post("/animationIsGenerated", async (req, res) => {
  let buffers = await readBodyAsBuffer(req);
  console.log(buffers);

  sockets.forEach((socket) => {
    socket.emit("animationData", buffers);
  });
  sockets.forEach((socket) => {
    socket.emit("animationSpeed", frame_interval);
  });
  res.status(200).end();
});

app.post("/setAnimationSpeed", (req, res) => {
  frame_interval = req.body.interval
  res.status(200).end();
})

io.on("connection", (socket) => {
  console.log("user connected");
  sockets.push(socket);
  socket.on("disconnect", () => {
    console.log("user disconnected");
    sockets = sockets.filter((item) => item.id !== socket.id);
  });
});

server.listen(3000, () => {
  console.log("server running at http://localhost:3000");
});
const readBodyAsBuffer = (req) => {
  return new Promise((resolve, reject) => {
    let body = [];
    req.on("data", (chunk) => {
      body.push(chunk);
    });
    req.on("end", () => {
      resolve(Buffer.concat(body));
    });
    req.on("error", (err) => {
      reject(err);
    });
  });
};
function spliceBuffers(buffers) {
  const len = buffers
    .map((buffer) => buffer.byteLength)
    .reduce((prevLength, curr) => {
      return prevLength + curr;
    }, 0);

  const tmp = new Uint8Array(len);

  let bufferOffset = 0;

  for (var i = 0; i < buffers.length; i++) {
    tmp.set(new Uint8Array(buffers[i]), bufferOffset);
    bufferOffset += buffers[i].byteLength;
  }

  return tmp;
}
