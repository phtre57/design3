import cv2

LENGTH = 640
HEIGHT = 480

cap = cv2.VideoCapture(0)
cap.set(3, 1600)
cap.set(4, 1200)
cap.set(3, 640)
cap.set(4, 480)
ret, img = cap.read()

cap.release()
# img = cv2.resize(img, (LENGTH, HEIGHT))

cv2.imwrite('table.jpg', img)
cv2.imshow('ok', img)

cv2.waitKey()