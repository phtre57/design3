import time


class Communication_pi_mock():
    def __init__(self):
        print("Init communication mock")

    def connectToPi(self):
        print("Communication mock: connect")

    def getImage(self):
        input('getImage')
        print("Communication mock: getImage")

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
        input('changeServoHori')
        print("Communication mock: changeServoHori ## " + str)

    def changeServoVert(self, str):
        input('changeServoVert')
        print("Communication mock: changeServoVert ## " + str)