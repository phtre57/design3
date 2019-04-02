import socketio
import time
import cv2
import base64

from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *
from util.Logger import *

logger = Logger(__name__)

URL = 'http://192.168.0.38:4000'

TENSION_FACTOR = 4


class Communication_pi:
    def __init__(self, url=URL):
        logger.log_info("Création de la communication...")
        self.ready = True
        self.image = None
        self.sio = None
        self.tension = None
        self.pinState = 0
        self.url = url
        self.__init()

    def __init(self):
        self.sio = socketio.Client()
        self.sio.connect(self.url)
        self.sio.emit('sendUrl', 'http://192.168.0.53:4001')

        @self.sio.on('readySignal')
        def readySignal(message):
            logger.log_info("Self ready switched to True...")
            self.ready = True

        @self.sio.on('recvPins')
        def recvPings(message):
            self.pinState = int(message)

        @self.sio.on('recvImage')
        def recvImage(message):
            logger.log_info("Image received...")
            frame_data = base64.b64decode(message)

            with open('test.jpg', 'wb') as f_output:
                f_output.write(frame_data)

            time.sleep(0.5)

            img = cv2.imread('./test.jpg')

            comm_ui = Communication_ui()
            comm_ui.SendImage(img, EMBARKED_FEED_IMAGE())

            logger.log_info("self.img changed...")
            self.image = img

        @self.sio.on('sendEmbarkedImage')
        def recvEmbarkedImage(message):
            logger.log_info("Image from embarked received...")
            frame_data = base64.b64decode(message)

            with open('test.jpg', 'wb') as f_output:
                f_output.write(frame_data)

            time.sleep(0.5)

            img = cv2.imread('./test.jpg')

            print('img received from embarked')

            comm_ui = Communication_ui()
            comm_ui.SendImage(img, EMBARKED_FEED_IMAGE())

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
            self.sio.connect(self.url)

        logger.log_info("Fin création de la communication...")

    def waitForReadySignal(self):
        t = time.time()

        while not self.ready:
            tt = time.time()
            if (tt - t > 20):
                self.__init()
                break

            self.sio.sleep(0.2)
            time.sleep(0.2)

    def waitForPinsSignal(self):
        t = time.time()
        self.pinState = 0
        while self.pinState != 1:
            tt = time.time()
            if (tt - t > 20):
                self.__init()
                break

            self.sio.emit('teTuSuePins', 'Cherimoya')
            self.sio.sleep(0.2)
            time.sleep(0.2)

    def disconnectFromPi(self):
        logger.log_info("Deconnecte du pi...")
        self.sio.emit('disconnect', 'bye Pi <3')

    def changeCondensateurHigh(self):
        logger.log_info("Signal envoyee pour condensateur...")
        self.sio.emit('condensateurChangeHigh', 1)
        self.ready = False
        self.waitForReadySignal()

    def changeCondensateurLow(self):
        logger.log_info("Signal envoyee pour condensateur...")
        self.sio.emit('condensateurChangeLow', 1)
        self.ready = False
        self.waitForReadySignal()

    def sendCoordinates(self, x, y):
        commande = str(round(x)) + "," + str(round(y)) + ",0\n"
        logger.log_info("Coordonnees envoyees: " + commande)
        self.sio.emit('sendPosition', commande)
        self.pinState = 1
        self.waitForPinsSignal()

    def sendAngle(self, angle):
        if abs(int(angle)) > 180:
            if angle < 0:
                angle = 360 + angle
            else:
                angle = 360 - angle

        angle = int(angle)
        logger.log_info("Angle envoyees: " + str(round(angle)))
        commande = '0,0,' + str(angle) + '\n'
        self.sio.emit('sendPosition', commande)
        self.pinState = 1
        self.waitForPinsSignal()
        time.sleep(0.2)

    def getImage(self):
        while True:
            try:
                img = self.getImagePi()
                return img
            except Exception:
                logger.log_critical(
                    '401 Image not found - Erreur communication avec le pi getImage'
                )
                pass

    def getImagePi(self):
        logger.log_info("Get image du robot...")
        self.sio.emit('getImage', 'ok')
        self.image = None

        t = time.time()
        while self.image is None:
            tt = time.time()
            if (tt - t > 20):
                self.__init()
                raise Exception('Image not found')
                break

            time.sleep(0.01)

        logger.log_info("After wait image du robot...")
        return self.image

    def changeServoHori(self, commande):
        logger.log_info("Servo horizontal envoyees: " + commande)
        self.sio.emit('servoHori', str(commande))
        self.ready = False
        self.waitForReadySignal()

    def redLightOn(self):
        logger.log_info('Red Light sent on')
        self.sio.emit('redLightDistrictOn', 'Carambole')

    def redLightOff(self):
        logger.log_info('Red Light sent off')
        self.sio.emit('redLightDistrictOff', 'Figue')

    def changeServoVert(self, commande):
        logger.log_info("Servo vertical envoyees: " + commande)
        self.sio.emit('servoVert', str(commande))
        self.ready = False
        self.waitForReadySignal()

    def moveArm(self, commande):
        logger.log_info("Bouge le bras envoyees: " + commande)
        self.sio.emit('bras', commande)
        self.ready = False
        self.waitForReadySignal()

    def getTension(self):
        while True:
            try:
                tension = self.getTensionPi()
                tension = tension * TENSION_FACTOR
                return tension
            except Exception:
                logger.log_critical(
                    '401 Tension not found - Erreur communication avec le pi getTension'
                )
                pass

    def getTensionPi(self):
        self.sio.emit('getTension', 'Mangue')

        self.tension = None
        t = time.time()
        while self.tension is None:
            tt = time.time()
            if (tt - t > 20):
                self.__init()
                raise Exception('Tension not found')

            time.sleep(0.01)

        logger.log_info("Tension recu: " + str(self.tension * TENSION_FACTOR))
        return self.tension
