import socketio
from util.Logger import *

logger = Logger(__name__)


class clientSocketIO:

    def connectToPi(self):
        logger.log_info("Connecte au serveur...")

    def disconnectFromPi(self):
        logger.log_info("Deconnecte du pi...")

    def changeCondensateur(self):
        logger.log_info("Signal envoyee pour condensateur...")

    def sendCoordinates(self, x, y):
        logger.log_info("Coordonnees envoyees: " + str(x) + str(y))

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