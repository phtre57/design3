from imutils import paths
import argparse
import cv2

BLUR_TRESHOLD = 30

def detect_blurriness(imagePath):
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    actualBlur = laplacian(gray)

    if actualBlur < BLUR_TRESHOLD:
        return False

    return True

def laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


if __name__ == "__main__":
    isBlurry = detect_blurriness("non_blurry.jpg")

    if isBlurry:
        print("Pas blurry")
    else:
        print("Freakin' blurry")
