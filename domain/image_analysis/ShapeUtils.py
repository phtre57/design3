import cv2
import numpy as np
import imutils

def find_where_the_shape_is(shape, color, radius_limit):
    (lower, upper) = color.color_code

    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(shape.frame, lower, upper)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    (cX, cY) = find_center(cnts, radius_limit)

    if (cX == 0 and cY == 0):
        print("Ça pas marché")

    res_contour = get_contour_related_to_center(shape.approx, cX, cY)

    if (res_contour == 0):
        print("Ça pas marché")

    res_contour.append(mask)
    return res_contour

def get_contour_related_to_center(approx, cX, cY):
    is_in = False
    for contour in approx:
        is_in = cv2.pointPolygonTest(contour[1], (cX, cY), False)
        if (is_in):
            res_contour = contour
            res_contour.append((cX, cY))
            return res_contour
    return 0

def find_center(c, radius_limit):
    if(validate_if_contour_is_too_small(c, radius_limit)):
        return

    M = cv2.moments(c)
    if(M["m00"] == 0.0):
        return (0, 0)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)

def validate_if_contour_is_too_small(c, radius_limit):
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    if (radius < radius_limit):
        return True
    else:
        return False