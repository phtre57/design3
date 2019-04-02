import socketio
import base64
import time
import cv2

from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *


def main():
    URL = 'http://192.168.0.38:4141'
    sioImg = socketio.Client()
    sioImg.connect(URL)

    @sioImg.on('sendEmbarkedImage')
    def recvEmbarkedImage(message):
        frame_data = base64.b64decode(message)

        with open('test.jpg', 'wb') as f_output:
            f_output.write(frame_data)

        time.sleep(0.5)

        img = cv2.imread('./test.jpg')

        cv2.imshow('hi', img)
        cv2.waitKey()

        print('img received from embarked')

        comm_ui = Communication_ui()
        comm_ui.SendImage(img, EMBARKED_FEED_IMAGE())

    sioImg.wait()


main()