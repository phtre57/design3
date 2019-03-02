const server = require("http").createServer()
const io = require("socket.io")(server)

let robotMainClient = {}

let UIClient = {}

io.on("connection", client => {
  onConnect(client)

  client.on("event", data => { 
    UIClient.emit("event", { data: "chocolat" })
  })

  //event from UI for the start signal
  client.on("start", resp => { 
    console.log("start");
    robotMainClient.emit("start", "started")
  })

  client.on("eventFromRobot", data => {
    if (data.type === "img") {
      console.log(">> Img");
      data.data = String.fromCharCode.apply(null, new Uint16Array(data.data));
    }
    
    UIClient.emit("event", data)
    client.emit("validation", "v")
    // client.disconnect()
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
    console.log("Hi UI");
  } else if(client.handshake.query.token === "MainRobot") {
    robotMainClient = client
    console.log("Hi Main Robot");
  } else {
    // console.log("Hi Robot");
  }
}
