import socketio
import base64
import cv2

sio = socketio.Client()
sio.connect('http://localhost:4000?token=robot')
sio.emit('eventFromRobot', {'data': 'Allo from robot', 'type': 'main' })
sio.disconnect()

sio = socketio.Client()
sio.connect('http://localhost:4000?token=robot')
frame = cv2.imread("img.png")
retval, buffer = cv2.imencode('.png', frame)
encoded = base64.b64encode(buffer)
sio.emit('eventFromRobot', {'data': encoded, 'type': 'img' })
sio.disconnect()