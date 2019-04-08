import cv2
import numpy as np


def canny(frame, maskFunc, lower=100, upper=200):
    frame = cv2.GaussianBlur(frame, (5, 5), 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mask = maskFunc(frame)

    return cv2.Canny(mask, lower, upper)


def point_zone_dep_mask(frame):
    mask = frame
    kernel = np.ones((10, 10), np.uint8)
    mask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    return mask


def detect_contour_mask(frame):
    mask = frame
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    return mask


def dilate_mask(frame):
    mask = cv2.dilate(
        frame,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)),
        iterations=1)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask


def dilate_mask_zone_dep(frame):
    mask = cv2.dilate(
        frame,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)),
        iterations=1)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)))
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask


def erode_mask(frame):
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask, kernelerode, iterations=1)
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask


def erode_mask_zone_dep(frame):
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask, kernelerode, iterations=1)
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask


def erode_mask_zone_dep_world(frame):
    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask, kernelerode, iterations=1)
    mask = cv2.GaussianBlur(mask, (1, 1), 0)
    return mask
