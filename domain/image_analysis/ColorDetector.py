import cv2
import numpy as np
import imutils

from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector

def ColorDetector(frame):
    frame = cv2.GaussianBlur(frame, (5, 5), 1)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2,2),np.uint8)
    
    mask = frame

    mask = cv2.dilate(mask, kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2)) , iterations = 1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
    mask = cv2.GaussianBlur(mask, (1, 1), 0)

    return cv2.Canny(mask,100,200)

frame = cv2.imread("../../image_samples/real_image/pieces.jpg")
edges = ColorDetector(frame)
shapeDetector = ShapeDetector()
shape = shapeDetector.detect(edges, False, 700, 150, 0.02, 10, 10, 90, True)

kernel = np.ones((9, 9), np.uint8)
kernelerode = np.ones((9,9),np.uint8)

shape = shapeDetector.detect(edges, True, 700, 150, 0.02, 10, 10, 90, True)

output = cv2.bitwise_and(frame, frame, mask=edges)

mask = output
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
mask = cv2.erode(mask,kernelerode,iterations = 1)

output = mask
# print(shape)

cv2.imshow('EDGES', output)

cv2.waitKey()