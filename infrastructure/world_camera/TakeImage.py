from threading import Thread
from util.Logger import Logger
from infrastructure.communication_ui.comm_ui import *

import cv2
import time

logger = Logger(__name__)


class TakeImage:
    def __init__(self, src=0, is_cancer_mac_user=0):
        logger.log_info("Ouverture de la caméra: ")

        self.cam = cv2.VideoCapture(src)

        while self.cam.isOpened() is not True:
            time.sleep(0.05)

        logger.log_info("Fin ouverture de la caméra: ")

        if is_cancer_mac_user:
            self.cam.set(3, 640)
            self.cam.set(4, 480)

        (self.ret, self.frame) = self.cam.read()
        time.sleep(0.05)

        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.ret:
                self.stop()
            else:
                (self.ret, self.frame) = self.cam.read()
                comm_ui = Communication_Ui()
                comm_ui.SendImage(self.fram, WORLD_FEED_IMAGE)

    def read(self):
        return (self.ret, self.frame)

    def stop(self):
        self.stopped = True
