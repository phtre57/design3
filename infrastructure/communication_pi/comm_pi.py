import socket
import sys
import cv2
import pickle
import time
import numpy as np
import struct  # new
import base64
from io import StringIO
from PIL import Image

# Host = Adresse ip du serveur (ici Raspberry pi)
# Port = valeur predefinie (doit etre la meme pour le serveur)
host = '192.168.0.38'
port = 15555


class Communication_pi():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToPi(self):
        print(host)
        self.socket.connect((host, port))
        print("Connecte au serveur")
        time.sleep(5)

    def __recv_msg(self):
        raw_msglen = self.__recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.__recvall(msglen)

    def __recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_msg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.socket.sendall(msg)

    def getImage(self):
        output = "getImage"
        self.socket.send(output.encode('utf-8'))

        data = self.__recv_msg()
        data = str(data, 'utf-8')
        frame_data = base64.b64decode(data)

        with open('test.jpg', 'wb') as f_output:
            f_output.write(frame_data)

        time.sleep(1)

        return cv2.imread('./test.jpg')

    def sendCoordinates(self, str):
        signal = 'sendPosition'
        self.socket.sendall(signal.encode('utf-8'))
        self.socket.sendall(str.encode('utf-8'))
        print("Coordonnees envoyees")
        self.robotReady()

    def disconnectFromPi(self):
        signal = 'deconnect'
        self.socket.sendall(signal.encode('utf-8'))
        self.socket.close()

    def robotReady(self):
        self.socket.recv(255)
        print("Ready signal received")

    def changeCondensateur(self):
        signal = 'condensateurChange'
        self.socket.sendall(signal.encode('utf-8'))
        print("Signal envoye!")

    def changeServoHori(self, str):
        signal = 'servoHori'
        self.socket.sendall(signal.encode('utf-8'))
        self.socket.sendall(str.encode('utf-8'))
        print("Servo Horizontal envoyees")

    def changeServoVert(self, str):
        signal = 'servoVert'
        self.socket.sendall(signal.encode('utf-8'))
        self.socket.sendall(str.encode('utf-8'))
        print("Servo Vertical envoyees")

    def getTension(self):
        signal = 'gettension'
        self.socket.sendall(signal.encode('utf-8'))
        data = self.socket.recv(255)
        data = str(data, "utf-8")
        print("Received tension: " + str(data))

        data = data.replace("\r", "")
        data = data.replace("\n", "")

        return float(data)


def main():
    communication_pi = Communication_pi()
    communication_pi.connectToPi()
    time.sleep(2)
    communication_pi.getImage()
    time.sleep(2)
    communication_pi.sendCoordinates("2")
    time.sleep(2)
    communication_pi.disconnectFromPi()


if __name__ == "__main__":
    # execute only if run as a script
    main()
