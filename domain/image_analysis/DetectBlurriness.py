from imutils import paths
import argparse
import cv2

BLUR_TRESHOLD = 30


def detect_blurriness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    actualBlur = laplacian(gray)

    if actualBlur > BLUR_TRESHOLD:
        return False

    return True


def laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

