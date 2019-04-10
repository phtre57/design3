import time
import cv2

class Communication_pi_mock():
    def __init__(self):
        self.TENSION = 0.0
        self.scan_for_qr = False
        self.image = cv2.imread('./image_samples/real_image/qr.png')
        print("Init communication mock")

    def connectToPi(self):
        print("Communication mock: connect")

    def getTension(self):
        print("Communication mock: getTension")
        self.TENSION = self.TENSION + 1.0
        return self.TENSION

    def changeCondensateurHigh(self):
        print("Communication mock: changeCondensateurHigh")

    def changeCondensateurLow(self):
        print("Communication mock: changeCondensateurLow")

    def getImage(self):
        # cap = cv2.VideoCapture(1)

        # while True:
        #     if cap.isOpened():
        #         break

        # ret, img = cap.read()
        # img = cv2.resize(img, (320, 240))
        # cv2.imshow('ok', img)
        # cv2.waitKey()
        # cap.release()
        img = cv2.imread('./samples/sampleio2.jpg')
        img = cv2.imread('./samples/zonedep9.jpg')

        print("Communication mock: getImage")
        return img

    def sendCoordinates(self, x, y):
        print("Communication mock: sendCoordinates ## " + str(x) + ", " +
              str(y))

    def redLightOff(self):
        print('Red Light Off')

    def redLightOn(self):
        print('Red Light On')

    def moveArm(self, commande):
        print('move Arm')

    def disconnectFromPi(self):
        print("Communication mock: disconnect")

    def robotReady(self):
        print("Communication mock: robotReady")

    def changeCondensateur(self):
        print("Communication mock: changeCondensateur")

    def sendAngle(self, angle):
        print("Communication mock: sendAngle ## " + str(angle))

    def changeServoHori(self, str):
        print("Communication mock: changeServoHori ## " + str)

    def changeServoVert(self, str):
        print("Communication mock: changeServoVert ## " + str)