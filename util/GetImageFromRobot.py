import time
import cv2
from infrastructure.communication_pi.comm_pi import *


def take_image(comm_pi):
    image = comm_pi.getImage()
    cv2.imshow("test", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("piece11.jpg", image)


comm_pi = Communication_pi()
comm_pi.connectToPi()
#comm_pi.changeServoVert('6000')
#comm_pi.changeServoHori('2000')
take_image(comm_pi)
comm_pi.disconnectFromPi()