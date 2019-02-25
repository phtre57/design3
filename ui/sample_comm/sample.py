import socketio
import base64
import cv2
import time

sio = socketio.Client()
sio.connect('http://localhost:4000?token=UI')
time.sleep(0.1)
sio.emit('start', 'start')
time.sleep(0.1)
sio.disconnect()

# sio = socketio.Client()
# sio.connect('http://localhost:4000?token=robot')
# sio.emit('eventFromRobot', {'data': 'Allo from robot', 'type': 'main' })
# sio.disconnect()

# sio = socketio.Client()
# sio.connect('http://localhost:4000?token=robot')
# frame = cv2.imread("img.png")
# retval, buffer = cv2.imencode('.png', frame)
# encoded = base64.b64encode(buffer)
# sio.emit('eventFromRobot', {'data': encoded, 'type': 'img' })
# sio.disconnect()