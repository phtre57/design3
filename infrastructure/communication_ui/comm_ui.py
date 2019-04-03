import socketio
import base64
import cv2


class Communication_ui():
    def __init__(self):
        self.sio = self.__init_conn()

    def __init_conn(self):
        if (__debug__):
            try:
                sio = socketio.Client()
                sio.connect('http://localhost:4001?token=robot')

                @sio.on('validation')
                def on_validation(v):
                    sio.disconnect()
            except Exception:
                print(
                    'Can\'t connect to UI backend, ignore if in testing mode')

            return sio

    def SendImage(self, frame, dest):
        if (__debug__):
            _, buffer = cv2.imencode('.jpg', frame)
            encoded = base64.b64encode(buffer)
            self.sio.emit('eventFromRobot', {
                'data': encoded,
                'type': 'img',
                'dest': dest
            })

    def sendStopSignal(self):
        if (__debug__):
            self.sio.emit('sendStopSignal', 'Stop')

    def SendText(self, val, dest):
        if (__debug__):
            self.sio.emit('eventFromRobot', {
                'data': val,
                'type': 'text',
                'dest': dest
            })

    def SendLog(self, val, dest):
        if (__debug__):
            self.sio.emit('sendLog', {
                'data': val,
                'type': 'text',
                'dest': dest
            })
