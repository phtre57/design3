import socketio
import base64
import cv2

class Communication_ui():
    def __init__(self):
        self.sio = self.__init_conn()

    def __init_conn(self):
        try:
            sio = socketio.Client()
            sio.connect('http://localhost:4000?token=robot')

            @sio.on('validation')
            def on_validation(v):
                print('validation')
                sio.disconnect()
        except Exception:
            print('Can\'t connect to UI backend, ignore if in testing mode')
                
        return sio

    def SendImage(self, frame, dest):
        _, buffer = cv2.imencode('.jpg', frame)
        encoded = base64.b64encode(buffer)
        self.sio.emit('eventFromRobot', {'data': encoded, 'type': 'img', 'dest': dest})
        
    def SendText(self, val, dest):
        self.sio.emit('eventFromRobot', {'data': val, 'type': 'text', 'dest': dest})

    def SendLog(self, val, dest):
        self.sio.emit('sendLog', {'data': val, 'type': 'text', 'dest': dest})
