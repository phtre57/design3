import cv2

# LENGTH = 320
# HEIGHT = 240

cap = cv2.VideoCapture(1)
ret, img = cap.read()
cap.release()
# img = cv2.resize(img, (LENGTH, HEIGHT))

cv2.imwrite('piece_xy.jpg', img)
cv2.imshow('ok', img)

cv2.waitKey()