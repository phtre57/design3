import socket
import sys  
import cv2  
import pickle
import time
import numpy as np
import struct ## new        
     
# Host = Adresse ip du serveur (ici Raspberry pi)
# Port = valeur predefinie (doit etre la meme pour le serveur)  
host = '192.168.0.38'
port = 15555    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
	connectToPi()
	time.sleep(2)
	# readySignal()
	time.sleep(2)
	getImage()
	time.sleep(2)
	sendCoordinates("2")
	time.sleep(2)
	deconnectToPi()

def connectToPi():         
	print(host)
	s.connect((host, port))
	print("Connecte au serveur")

def getImage():
	data = b""
	payload_size = struct.calcsize(">L")
	print("payload_size: {}".format(payload_size))

	output = "getImage"
	s.send(output.encode('utf-8'))

	while len(data) < payload_size:
		print("Recv: {}".format(len(data)))
		data = s.recv(4096)

	print("Done Recv: {}".format(len(data)))
	
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack(">L", packed_msg_size)[0]
	print("msg_size: {}".format(msg_size))

	while len(data) < msg_size:
        	data += s.recv(4096)
	frame_data = data[:msg_size]
	data = data[msg_size:]

	frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
	frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

	cv2.imwrite('messigray.png',frame)

def sendCoordinates(str):
	signal = 'sendPosition'
	s.sendall(signal.encode('utf-8'))
	s.sendall(str.encode('utf-8'))
	print("Coordonnees envoyees")

def deconnectToPi():
	s.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()