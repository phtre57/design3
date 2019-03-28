import cv2
import numpy as np
import os

from util.color import Color
from domain.image_analysis.opencv_callable.ColorDetector import create_mask_for_color_detector, destroy_the_image


def nothing(x):
    pass


def cest_gasant(val):
    if (val > 100):
        return val - 100
    else:
        return (100 - val) * -1


cv2.namedWindow('result', cv2.WINDOW_NORMAL)

cv2.createTrackbar('b', 'result', 100, 200, nothing)
cv2.createTrackbar('c', 'result', 32, 200, nothing)
cv2.createTrackbar('s', 'result', 28, 200, nothing)
cv2.createTrackbar('h', 'result', -1, 200, nothing)
cv2.createTrackbar('g', 'result', 156, 200, nothing)
cv2.createTrackbar('e', 'result', -4, 200, nothing)

b, c, s = 100.0, 32.0, 28.0
h, g, e = -1.0, 156.0, -4.0

cap = cv2.VideoCapture(1)

while True:
    if cap.isOpened():
        break

# frame = cv2.imread(path)
# cv2.imshow('result',frame)
# cv2.waitKey()

while (1):
    _, og_frame = cap.read()
    cap.set(10, b)
    cap.set(11, c)
    cap.set(12, s)
    cap.set(13, h)
    cap.set(14, g)
    cap.set(15, e)

    frame = og_frame.copy()
    # frame = destroy_the_image(frame)

    # converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    b = cv2.getTrackbarPos('b', 'result')
    c = cv2.getTrackbarPos('c', 'result')
    s = cv2.getTrackbarPos('s', 'result')

    h = cv2.getTrackbarPos('h', 'result')
    g = cv2.getTrackbarPos('g', 'result')
    e = cv2.getTrackbarPos('e', 'result')

    b = cest_gasant(b)
    c = cest_gasant(c)
    s = cest_gasant(s)
    h = cest_gasant(h)
    g = cest_gasant(g)
    e = cest_gasant(e)

    text = og_frame.copy()
    text = destroy_the_image(text)

    # cv2.imshow('deb', deb)
    # cv2.waitKey()

    cv2.putText(text, 'Valeur du filter bleu', (10, 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    cv2.putText(text,
                str(b) + " " + str(c) + " " + str(s), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    cv2.putText(text,
                str(h) + " " + str(g) + " " + str(e), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)

    numpy_horizontal = np.hstack((frame, text))
    numpy_horizontal_concat = np.concatenate((frame, text), axis=1)

    cv2.imshow('result', numpy_horizontal)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()