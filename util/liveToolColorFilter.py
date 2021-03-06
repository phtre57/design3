import cv2
import numpy as np
import os

from util.color import Color
from domain.image_analysis.opencv_callable.ColorDetector import create_mask_for_color_detector, destroy_the_image

path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
path = os.path.join(path, "./samples/piece")


def nothing(x):
    pass


cv2.namedWindow('result', cv2.WINDOW_NORMAL)
h, s, v = 100, 100, 100
hu, su, vu = 100, 100, 100
fileNo = 0
default_values = 0

# b, c, s = 100, 32, 28
# h, g, e = -1, 156, -4

b, c, s = 61, 24, 100
h, g, e = 0, 69, -4

cv2.createTrackbar('h', 'result', 0, 255, nothing)
cv2.createTrackbar('s', 'result', 0, 255, nothing)
cv2.createTrackbar('v', 'result', 0, 255, nothing)

cv2.createTrackbar('hu', 'result', 0, 255, nothing)
cv2.createTrackbar('su', 'result', 0, 255, nothing)
cv2.createTrackbar('vu', 'result', 0, 255, nothing)

cv2.createTrackbar('fileNo', 'result', 0, 36, nothing)

cv2.createTrackbar('default', 'result', 0, 4, nothing)

cap = cv2.VideoCapture(1)
cap.set(10, b)
cap.set(11, c)
cap.set(12, s)
cap.set(13, h)
cap.set(14, g)
cap.set(15, e)

while True:
    if cap.isOpened():
        break

while (1):
    _, og_frame = cap.read()

    frame = og_frame.copy()
    frame = destroy_the_image(frame)

    # converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h', 'result')
    s = cv2.getTrackbarPos('s', 'result')
    v = cv2.getTrackbarPos('v', 'result')

    hu = cv2.getTrackbarPos('hu', 'result')
    su = cv2.getTrackbarPos('su', 'result')
    vu = cv2.getTrackbarPos('vu', 'result')

    default_values = cv2.getTrackbarPos('default', 'result')

    text = og_frame.copy()
    text = destroy_the_image(text)

    # cv2.imshow('deb', deb)
    # cv2.waitKey()

    if (default_values == 1):
        # Notre filter de bleu
        color = Color()
        color.BLUE()
        lower_hsv, upper_hsv = color.color_code_hsv
        cv2.putText(text, 'Valeur du filter bleu', (10, 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
        cv2.putText(text, color.color_code_hsv_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    elif (default_values == 2):
        # Notre filter de rouge
        color = Color()
        color.RED()
        lower_hsv, upper_hsv = color.color_code_hsv
        cv2.putText(text, 'Valeur du filter rouge', (10, 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
        cv2.putText(text, color.color_code_hsv_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    elif (default_values == 3):
        # Notre filter de vert
        color = Color()
        color.GREEN()
        lower_hsv, upper_hsv = color.color_code_hsv
        cv2.putText(text, 'Valeur du filter vert', (10, 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
        cv2.putText(text, color.color_code_hsv_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    elif (default_values == 4):
        # Notre filter de jaune
        color = Color()
        color.YELLOW()
        lower_hsv, upper_hsv = color.color_code_hsv
        cv2.putText(text, 'Valeur du filter jaune', (10, 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
        cv2.putText(text, color.color_code_hsv_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    else:
        lower_hsv = np.array([h, s, v])
        upper_hsv = np.array([hu, su, vu])
        cv2.putText(text, 'Actual color filter', (10, 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
        hsv_str = str(h) + " " + str(s) + " " + str(v) + " | " + str(
            hu) + " " + str(su) + " " + str(vu)
        cv2.putText(text, hsv_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (70, 0, 255), 2)

    B = cap.get(10)
    C = cap.get(11)
    S = cap.get(12)
    H = cap.get(13)
    G = cap.get(14)
    E = cap.get(15)

    cv2.putText(text,
                str(B) + " " + str(C) + " " + str(S), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)
    cv2.putText(text,
                str(H) + " " + str(G) + " " + str(E), (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    # result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    # text = cv2.cvtColor(text, cv2.COLOR_HSV2BGR)

    numpy_horizontal = np.hstack((result, text))
    numpy_horizontal_concat = np.concatenate((result, text), axis=1)

    cv2.imshow('result', numpy_horizontal)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()