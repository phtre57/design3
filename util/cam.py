import cv2

cap = cv2.VideoCapture(0)
ret, img = cap.read()
cap.release()
cv2.imwrite('calibration2.jpg', img)
cv2.imshow('ok', img)

cv2.waitKey()