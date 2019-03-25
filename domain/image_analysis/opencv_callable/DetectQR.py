import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from domain.QRCodeDictionnary import *

def decode(im):
    decodedObjects = pyzbar.decode(im)

    for obj in decodedObjects:
        if obj.type == "QRCODE":
            # print('Type : ', obj.type)
            # print('Data : ', obj.data,'\n')
            data = obj.data
            data = str(data, "utf-8")
            code = data[0]
            return QR_CODE_VALUE_DICTIONARY[code]

        raise Exception("Could not decode QR")
