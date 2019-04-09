import cv2
import time

cap = cv2.VideoCapture(1)

while True:
    if cap.isOpened():
        break

cap.set(3, 640)
cap.set(4, 480)


img = None
while True:
    time.sleep(0.5)
    ret, img = cap.read()
    print(ret)
    if ret:
        break

img = cv2.resize(img, (640, 480))
cv2.imshow("test", img)
cv2.waitKey(0)
