import cv2
import time
import numpy as np

LENGTH = 640
HEIGHT = 480

cap = cv2.VideoCapture(2)

while True:
    if cap.isOpened():
        break

# cap.set(3, 1600)
# cap.set(4, 1200)
# cap.set(3, 640)
# cap.set(4, 480)

img = None
while True:
    ret, img = cap.read()
    img = cv2.resize(img, (320, 240))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img[..., 1] = img[..., 1] * 1
    img[..., 2] = img[..., 2] * 1
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    cv2.circle(img, (round(320 / 2), round(240 / 2)), 3, [255, 51, 51])
    cv2.imshow('ok', img)
    cv2.imwrite('./embark.jpg', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # if ret:
    # break

print(ret)

# img = cv2.resize(img, (LENGTH, HEIGHT))

cv2.destroyAllWindows()

cap.release()