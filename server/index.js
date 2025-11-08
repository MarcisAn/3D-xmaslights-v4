const express = require("express");
const { createServer } = require("node:http");
const { join } = require("node:path");
const { Server } = require("socket.io");
const cors = require("cors");
const { log } = require("node:console");
const spawn = require("child_process").spawn;
const fs = require('fs');
var bodyParser = require("body-parser");

// Server config
const app = express();
app.use(cors());
app.use(express.json());
app.use(bodyParser.raw({ type: "application/octet-stream", limit: "2mb" }));
const server = createServer(app);
const io = new Server(server);

// app.get("/", (req, res) => {
//   console.log(sockets.length);
//   res.statusCode(200);
// });

// Called when user picks an animation to play
app.post("/pickAnim", (req, res) => {
  console.log(req.body.name);
  const pythonProcess = spawn("python", ["../generators/AnimBuilder.py"]);
  console.log("socket count: " + sockets.length);

  res.status(200).end();
});

app.post("/animationIsGenerated", async (req, res) => {
  let buffers = await readBodyAsBuffer(req);
  console.log(buffers);
  
  sockets.forEach((socket) => {
    socket.emit("animationData", buffers);
  });
  res.status(200).end()
})

// Store the socket objects for active connections
let sockets = [];

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