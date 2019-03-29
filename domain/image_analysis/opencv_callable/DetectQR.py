import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from domain.QRCodeDictionnary import *
from util.Logger import Logger

logger = Logger(__name__)

DEBUG = False


def decode(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    if DEBUG:
        cv2.imshow('ROBOT FRAME', im)
        cv2.waitKey()

    decodedObjects = pyzbar.decode(im)

    for obj in decodedObjects:
        if obj.type == "QRCODE":
            # print('Type : ', obj.type)
            # print('Data : ', obj.data,'\n')
            data = obj.data
            data = str(data, "utf-8")
            code = data.split('-')[0]
            return QR_CODE_VALUE_DICTIONARY[code]

        raise Exception("Could not decode QR")
