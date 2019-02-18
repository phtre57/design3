import cv2
import numpy as np


def canny(frame, func):
    frame = cv2.GaussianBlur(frame, (5, 5), 1)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2,2),np.uint8)
    
    mask = func(frame)

    return cv2.Canny(mask,100,200)

def dilate_mask(frame):
    mask = cv2.dilate(frame, kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2)) , iterations = 1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask

def dilate_mask_zone_dep(frame):
    mask = cv2.dilate(frame, kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2)) , iterations = 1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8)))
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask

def erode_mask(frame):
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2,2),np.uint8)
    mask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask,kernelerode,iterations = 1)
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask