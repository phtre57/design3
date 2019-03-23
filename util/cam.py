import cv2
import time

LENGTH = 640
HEIGHT = 480

cap = cv2.VideoCapture(1)

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
    if ret:
        break

print(ret)

# img = cv2.resize(img, (LENGTH, HEIGHT))

cv2.imwrite('zonedep.jpg', img)
cv2.imshow('ok', img)

cv2.waitKey()
cv2.destroyAllWindows()

cap.release()