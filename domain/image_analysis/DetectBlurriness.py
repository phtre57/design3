from imutils import paths
import argparse
import cv2

CONST_TRESHOLD = 30

def detect_blurriness():
    image = cv2.imread("blurry.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = laplacian(gray)
    text = "Not Blurry en criss"

    if fm < CONST_TRESHOLD:
        text = "Blurry en criss"

    cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)

def laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


if __name__ == "__main__":
    detect_blurriness()