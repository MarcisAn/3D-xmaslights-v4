const express = require("express");
const { createServer } = require("node:http");
const { join } = require("node:path");
const { Server } = require("socket.io");
const cors = require("cors");
const spawn = require("child_process").spawn;

// Server config
const app = express();
app.use(cors());
app.use(express.json());
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
  pythonProcess.stdout.on("data", (data) => {
    sockets.forEach((socket) => {
      socket.emit("animationData", data);
    });
  });

  res.status(200);
});

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
