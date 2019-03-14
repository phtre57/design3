from imutils import paths
import argparse
import cv2

CONST_TRESHOLD = 30

def detect_blurriness(imagePath):
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = laplacian(gray)

    if fm < CONST_TRESHOLD:
        print("Freakin' blurry")
        return False

    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
    print("Pas blurry")
    return True

def laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


if __name__ == "__main__":
    detect_blurriness("blurry.jpg")