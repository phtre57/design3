import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im) : 
  decodedObjects = pyzbar.decode(im)
 
  for obj in decodedObjects:
    if (obj.type == "QRCODE"):
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')
        return obj