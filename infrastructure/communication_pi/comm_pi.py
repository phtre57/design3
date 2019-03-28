import socketio
import time
from util.Logger import *

logger = Logger(__name__)

URL = 'http://192.168.0.38:4000'


class Communication_pi:
    def __init__(self, url=URL):
        self.ready = True
        self.image = None
        self.sio = socketio.Client()
        self.sio.connect(url)

        @self.sio.on('readySignal')
        def sendCoord(message):
            logger.log_info("Self ready switched to True...")
            self.ready = True

        @self.sio.on('receiveImage')
        def receiveImage(image):
            logger.log_info("Received image...")
            self.image = image
            self.ready = True

    def connectToPi(self):
        logger.log_info("Connecte au serveur...")

    def disconnectFromPi(self):
        logger.log_info("Deconnecte du pi...")

    def changeCondensateur(self):
        logger.log_info("Signal envoyee pour condensateur...")

    def sendCoordinates(self, x, y):
        commande = str(x) + "," + str(y) + ",0\n"
        self.sio.emit('sendPosition', commande)
        logger.log_info("Coordonnees envoyees: " + str(x) + str(y))
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def sendAngle(self, angle):
        commande = "0,0" + str(angle) + "\n"
        self.sio.emit('sendAngle', commande)
        logger.log_info("Angle envoyees: " + angle)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def getImage(self):
        logger.log_info("Get image of robot...")

        self.image = None
        img = self.sio.emit('getImage')

        while self.image is None:
            logger.log_info("Waiting for robot image...")
            time.sleep(0.2)


    def changeServoHori(self, commande):
        logger.log_info("Servo horizontal envoyees: " + commande)

    def changeServoVer(self, commande):
        logger.log_info("Servo vertical envoyees: " + commande)

    def moveArm(self, commande):
        logger.log_info("Bouge le bras envoyees: " + commande)

    def getTension(self):
        logger.log_info("Tension recu: ")
