import socketio
import time
import cv2
import base64

from util.Logger import *

logger = Logger(__name__)

URL = 'http://192.168.0.38:4000'


class Communication_pi:
    def __init__(self, url=URL):
        logger.log_info("Création de la communication...")
        self.ready = True
        self.image = None
        self.sio = socketio.Client()
        self.sio.connect(url)
        self.image = None
        self.tension = None

        @self.sio.on('readySignal')
        def sendCoord(message):
            logger.log_info("Self ready switched to True...")
            self.ready = True

        @self.sio.on('recvImage')
        def recvImage(message):
            logger.log_info("Image received...")
            frame_data = base64.b64decode(message)

            with open('test.jpg', 'wb') as f_output:
                f_output.write(frame_data)

            time.sleep(0.5)

            img = cv2.imread('./test.jpg')
            logger.log_info("self.img changed...")
            self.image = img

        @self.sio.on('recvTension')
        def recvTension(message):
            logger.log_info("Tension received...")
            try:
                self.tension = float(message)
            except Exception:
                self.tension = 0.00
                pass

        @self.sio.on('disconnect')
        def disconnect(message):
            logger.log_info("Disconnected from Pi...")
            self.sio = socketio.Client()
            self.sio.connect(url)

        logger.log_info("Fin création de la communication...")

    def connectToPi(self):
        logger.log_info("Connecte au serveur...")

    def disconnectFromPi(self):
        logger.log_info("Deconnecte du pi...")
        self.sio.emit('disconnect', 'bye Pi <3')

    def changeCondensateur(self):
        logger.log_info("Signal envoyee pour condensateur...")
        self.sio.emit('condensateurChange', 1)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def changeCondensateurHigh(self):
        logger.log_info("Signal envoyee pour condensateur...")
        self.sio.emit('condensateurChangeHigh', 1)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def changeCondensateurLow(self):
        logger.log_info("Signal envoyee pour condensateur...")
        self.sio.emit('condensateurChangeLow', 1)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def sendCoordinates(self, x, y):
        commande = str(round(x)) + "," + str(round(y)) + ",0\n"
        logger.log_info("Coordonnees envoyees: " + commande)
        self.sio.emit('sendPosition', commande)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def sendAngle(self, angle):
        logger.log_info("Angle envoyees: " + str(round(angle)))
        commande = '0,0,' + str(angle) + '\n'
        self.sio.emit('sendPosition', commande)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

        time.sleep(1)
        # if (abs(int(angle)) > 35):
        #     time.sleep(2)
        # if (abs(int(angle)) > 70):
        #     time.sleep(2)
        # if (abs(int(angle)) > 120):
        #     time.sleep(2)
        # if (abs(int(angle)) > 160):
        #     time.sleep(2)

    def getImage(self):
        logger.log_info("Get image du robot...")
        self.sio.emit('getImage', 'ok')

        self.image = None
        while self.image is None:
            time.sleep(0.01)

        logger.log_info("After wait image du robot...")
        return self.image

    def changeServoHori(self, commande):
        logger.log_info("Servo horizontal envoyees: " + commande)
        self.sio.emit('servoHori', str(commande))
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def changeServoVert(self, commande):
        logger.log_info("Servo vertical envoyees: " + commande)
        self.sio.emit('servoVert', str(commande))
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def moveArm(self, commande):
        logger.log_info("Bouge le bras envoyees: " + commande)
        self.sio.emit('bras', commande)
        self.ready = False

        while not self.ready:
            time.sleep(0.2)

    def getTension(self):
        self.sio.emit('getTension', 'Courge spaghetti')

        self.tension = None
        while self.tension is None:
            time.sleep(0.01)

        logger.log_info("Tension recu: " + str(self.tension))
        return self.tension
