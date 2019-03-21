import cv2
import traceback
from infrastructure.communication_pi.comm_pi import *
from domain.image_analysis.opencv_callable.DetectQR import *
from domain.image_analysis.DetectBlurriness import *
from domain.image_analysis_pathfinding.RobotDetector import *

DEBUG = True


class SequenceQR:

    def __init__(self):
        self.comm = Communication_pi() #injection ici por favor
        self.comm.connectToPi()

    def detectQR(self):
        x_sign = True
        increment_x_sign = 0
        while True:
            if x_sign:
                self.comm.sendCoordinates("50,0,0\n")
                increment_x_sign += 1
                if increment_x_sign == 6:
                    x_sign = False
            else:
                self.comm.sendCoordinates("-50,0,0\n")
                increment_x_sign -= 1
                if increment_x_sign == 0:
                    x_sign = True

            while True:
                img = self.comm.getImage()
                if detect_blurriness(img) is False:
                    break

            if DEBUG:
                cv2.imshow("qr", img)
                cv2.waitKey(0)

            try:
                str = decode(img)
                print(str)
                if str is not None:
                    break
            except Exception as ex:
                print(ex)

        self.comm.disconnectFromPi()


seq = SequenceQR()
seq.detectQR()