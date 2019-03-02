import socketio
import base64
import cv2


# class Communication_ui():

#     def __init_conn(self, data, dest, dtype):
#         sio = socketio.Client()
#         sio.connect('http://localhost:4000?token=robot')

#         @sio.on('validation')
#         def on_validation(v):
#             print('validation')
#             sio.disconnect()

#         sio.emit('eventFromRobot', {'data': data, 'type': dtype, 'dest': dest})

#     def SendImage(self, frame, dest):
#         _, buffer = cv2.imencode('.jpg', frame)
#         encoded = base64.b64encode(buffer)
#         self.__init_conn(encoded, dest, 'img')
        
#     def SendText(self, val, dest):
#         self.__init_conn(val, dest, 'text')


def InitConn():
    sio = socketio.Client()
    sio.connect('http://localhost:4000?token=robot')

    @sio.on('validation')
    def on_validation(v):
        print('validation')
        # sio.disconnect()

    return sio

def SendImage(frame, dest):
    sio = InitConn()

    retval, buffer = cv2.imencode('.jpg', frame)
    encoded = base64.b64encode(buffer)
    sio.emit('eventFromRobot', {'data': encoded, 'type': 'img', 'dest': dest})
    
def SendText(val, dest):
    sio = InitConn()

    sio.emit('eventFromRobot', {'data': val, 'type': 'img', 'dest': dest })


