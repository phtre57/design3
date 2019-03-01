import socketio
import base64
import cv2

class Communication_ui():

    def __init__(self):
        self.sio = __init_conn()

    def __init_conn(self):
        sio = socketio.Client()
        sio.connect('http://localhost:4000?token=robot')

        @sio.on('validation')
        def on_validation(v):
            print('validation')
            sio.disconnect()

        return sio

    def SendImage(frame, dest):
        retval, buffer = cv2.imencode('.jpg', frame)
        encoded = base64.b64encode(buffer)
        self.sio.emit('eventFromRobot', {'data': encoded, 'type': 'img', 'dest': dest})
        
    def SendText(val, dest):
        self.sio.emit('eventFromRobot', {'data': val, 'type': 'img', 'dest': dest })


