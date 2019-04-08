const server = require('http').createServer();
const io = require('socket.io')(server);

let UIClient = {};
let MainBaseStationClient = {};
let CommUIBaseStationClient = {};
let robotImageClient = {};

io.on('connection', client => {
  onConnect(client);

  client.on('event', data => {
    UIClient.emit('event', { data: 'chocolat' });
  });

  //event from UI for the start signal
  client.on('start', resp => {
    console.log('start');
    MainBaseStationClient.emit('start', 'started');
  });

  client.on('sendStopSignal', resp => {
    console.log('Stop Signal');
    UIClient.emit('sendStopSignal', 'Stop');
  });

  // Forward to UI
  client.on('eventFromRobot', data => {
    console.log('eventFromRobot');

    if (data.type === 'img') {
      data.data = String.fromCharCode.apply(null, new Uint16Array(data.data));
    }

    console.log(data.dest);

    UIClient.emit('event', data);
    client.emit('validation', 'v');
    client.disconnect();
  });

  client.on('sendImage', data => {
    if (UIClient == {}) {
      return;
    }

    if (data.type === 'img') {
      data.data = String.fromCharCode.apply(null, new Uint16Array(data.data));
    }

    console.log(data.dest);

    UIClient.emit('event', data);
    client.emit('validation', 'v');
    client.disconnect();
  });

  client.on('sendEmbarkedImage', data => {
    console.log('Got image from embarked');

    console.log(data.dest);

    // if (data.type === 'img') {
    //   data.data = String.fromCharCode.apply(null, new Uint16Array(data.data));
    // }

    UIClient.emit('event', data);
  });

  client.on('sendLog', data => {
    // console.log('sendLog');
    // console.log(data);
    UIClient.emit('event', data);
    client.emit('validation', 'v');
    client.disconnect();
  });

  client.on('disconnect', () => {});
});

server.listen(4001, () => {
  console.log('Started');
});

function onConnect(client) {
  if (client.handshake.query.token === 'UI') {
    UIClient = client;
    console.log('Hi UIClient');
  } else if (client.handshake.query.token === 'MainRobot') {
    MainBaseStationClient = client;
    console.log('Hi MainRobot');
  } else if (client.handshake.query.token === 'RobotImageClient') {
    robotImageClient = client;
    console.log('Hi RobotImageClient');
  }
}
