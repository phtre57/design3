import cv2
import numpy as np
import imutils

from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector

def DetectStartZone(frame):
    frame = cv2.GaussianBlur(frame, (5, 5), 1)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2,2),np.uint8)
    
    mask = frame
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask,kernelerode,iterations = 1)
    mask = cv2.GaussianBlur(mask, (1, 1), 0)

    return cv2.Canny(mask,100,200)

frame = cv2.imread("../../image_samples/real_image/globalmonde.jpg")
edges = DetectStartZone(frame)
shapeDetector = ShapeDetector()
shape = shapeDetector.detect(edges, False, 100000, 1000, 0.02, 90, 90, 100, False)
shape = shapeDetector.detect(edges, True, 100000, 1000, 0.02, 90, 90, 100, False)

kernelerode = np.ones((2,2),np.uint8)
kernel = np.ones((9, 9), np.uint8)

edges = cv2.erode(edges,kernelerode,iterations = 1)

output = cv2.bitwise_and(frame, frame, mask=edges)

output = Canny(output)

mask = output
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20)))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

output = mask

shape = shapeDetector.detect(output, True, 1500, 0, 0.02, 90, 90, 100, False)

output = cv2.bitwise_and(frame, frame, mask=output)

print(shape)

cv2.imshow('EDGES', edges)
cv2.imshow('EDGES', output)

cv2.waitKey()