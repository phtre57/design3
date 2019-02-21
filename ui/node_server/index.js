const server = require("http").createServer()
const io = require("socket.io")(server)

robotClient = {}
UIClient = {}

io.on("connection", client => {
  onConnect(client)

  client.on("event", data => { 
    UIClient.emit("event", { data: "chocolat" })
  })

  client.on("eventFromRobot", data => {
    if (data.type === "img") {
      console.log(">> Img");
      
      data.data = String.fromCharCode.apply(null, new Uint16Array(data.data));
    }
    
    UIClient.emit("event", data)
    client.emit("validation", "v")
    client.disconnect()
  })

  client.on("disconnect", () => { 
    console.log("bye")
  })
})

server.listen(4000)
console.log("Started")

function onConnect(client) {
  if (client.handshake.query.token === "UI") {
    UIClient = client
    UIClient.emit("event", { data: "Bienvenue toé" })
    console.log("Hi UI");
  } else {
    robotClient = client
    console.log("Hi Robot");
  }
}
