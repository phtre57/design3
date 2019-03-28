import socketio
import time
from util.Logger import *

logger = Logger(__name__)

URL = 'http://192.168.0.38:4000'

class Communication_pi:
    def __init__(self, url=URL):
        self.ready = True
        self.sio = socketio.Client()
        self.sio.connect(url)

        @self.sio.on('readySignal')
        def sendCoord(message):
            logger.log_info("Self ready switched to True...")
            self.ready = True

    def connectToPi(self):
        logger.log_info("Connecte au serveur...")

    def disconnectFromPi(self):
        logger.log_info("Deconnecte du pi...")

    def changeCondensateur(self):
        logger.log_info("Signal envoyee pour condensateur...")

    def sendCoordinates(self, x, y):
        commande = str(x) + "," + str(y) + ",0\n"
        self.sio.emit(commande)
        logger.log_info("Coordonnees envoyees: " + str(x) + str(y))
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def sendAngle(self, angle):
        logger.log_info("Angle envoyees: " + str(angle))

    def getImage(self):
        logger.log_info("Get image du robot...")

    def changeServoHori(self, commande):
        logger.log_info("Servo horizontal envoyees: " + commande)

    def changeServoVer(self, commande):
        logger.log_info("Servo vertical envoyees: " + commande)

    def moveArm(self, commande):
        logger.log_info("Bouge le bras envoyees: " + commande)

    def getTension(self):
        logger.log_info("Tension recu: ")