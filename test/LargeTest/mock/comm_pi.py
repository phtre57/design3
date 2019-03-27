import time
import cv2


class Communication_pi_mock():
    def __init__(self):
        print("Init communication mock")

    def connectToPi(self):
        print("Communication mock: connect")

    def getImage(self):
        input('getImage')
        cap = cv2.VideoCapture(2)

        while True:
            if cap.isOpened():
                break

        ret, img = cap.read()
        img = cv2.resize(img, (320, 240))
        cv2.imshow('ok', img)
        cv2.waitKey()
        cap.release()
        print("Communication mock: getImage")
        return img

    def sendCoordinates(self, str):
        input('sendCoordinates')
        print("Communication mock: sendCoordinates ## " + str)

    def disconnectFromPi(self):
        print("Communication mock: disconnect")

    def robotReady(self):
        print("Communication mock: robotReady")

    def changeCondensateur(self):
        print("Communication mock: changeCondensateur")

    def sendAngle(self, angle):
        input('sendAngle')
        print("Communication mock: sendAngle ## " + str(angle))

    def changeServoHori(self, str):
        # input('changeServoHori')
        print("Communication mock: changeServoHori ## " + str)

    def changeServoVert(self, str):
        # input('changeServoVert')
        print("Communication mock: changeServoVert ## " + str)