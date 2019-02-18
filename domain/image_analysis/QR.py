import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    if (obj.type == "QRCODE"):
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')
        return obj

# Main 
if __name__ == '__main__':
 
  # Read image
  im = cv2.imread('../../image_samples/real_image/qr.jpg')
 
  obj = decode(im)
  cv2.imshow('QR', im)

  cv2.waitKey()

     