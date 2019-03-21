import socket
import sys
import cv2
import pickle
import time
import numpy as np
import struct  # new

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

    def getImage(self):
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))

        output = "getImage"
        self.socket.send(output.encode('utf-8'))

        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data = self.socket.recv(4096)

        print("Done Recv: {}".format(len(data)))

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))

        while len(data) < msg_size:
            data += self.socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        # cv2.imwrite('messigray.png',frame)
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)

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
