import cv2
import numpy as np
import os

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

methods = ['cv2.TM_CCORR_NORMED']

path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
path = os.path.normpath(os.path.join(path, os.pardir))
path = os.path.normpath(os.path.join(path, os.pardir))

squareFrames = [os.path.join(path, "./samples/piece43.jpg"),
os.path.join(path, "./samples/piece41.jpg"),
os.path.join(path, "./samples/sampleio.jpg"),
os.path.join(path, "./samples/failed1.jpg")]

circleFrames = [os.path.join(path, "./samples/failed1.jpg"),
os.path.join(path, "./samples/failed4.jpg"),
os.path.join(path, "./samples/failed5.jpg"),
os.path.join(path, "./samples/sampleio3.jpg"),
os.path.join(path, "./samples/piece43.jpg")]

pentagonFrames = [os.path.join(path, "./samples/piece40.jpg"),
os.path.join(path, "./samples/sampleio2.jpg")]

triangleFrames = [os.path.join(path, "./samples/piece40.jpg"),
os.path.join(path, "./samples/piece41.jpg"),
os.path.join(path, "./samples/failed4.jpg"),
os.path.join(path, "./samples/failed5.jpg"),
os.path.join(path, "./samples/failed7.jpg"),
os.path.join(path, "./samples/sampleio1.jpg")]

# frames = triangleFrames

# for frame in frames:
#     pathimg = frame

#     img_rgb = cv2.imread(pathimg)
#     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

#     pathtpl = os.path.join(path, "./samples/tplCircle.jpg")
#     pathtpl = os.path.join(path, "./samples/tplSquare.jpg")
#     pathtpl = os.path.join(path, "./samples/tplPentagon.jpg")
#     pathtpl = os.path.join(path, "./samples/tplTriangle.jpg")
#     template = cv2.imread(pathtpl,0)

#     cv2.imshow('TEST', template)
#     cv2.waitKey()

#     w, h = template.shape[::-1]
#     res = cv2.matchTemplate(img_gray,template,cv2.TM_CCORR_NORMED)
#     # threshold = 0.90 # Circle
#     threshold = 0.81
#     loc = np.where( res >= threshold)

#     for pt in zip(*loc[::-1]):
#         cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

#     cv2.imshow('TEST', img_rgb)
#     cv2.waitKey()

import cv2
# import imutils
import glob, os
import numpy as np

path1 = os.path.join(path, "./samples/failed6.jpg")
image = cv2.imread(path1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h, w = gray.shape[:2]

pathtpl = os.path.join(path, "./samples/tplCircle.jpg")
for file in glob.glob(pathtpl):
    template = cv2.imread(file)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    found = None
    (tH, tW) = template.shape[:2]
    # cv2.imshow("Template", template)

    tEdged = cv2.Canny(template, 50, 200)

    for scale in np.linspace(1, 2, 20):
        # resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
        resized = cv2.resize(gray, dsize = (0,0), fx = scale, fy = scale)

        r = gray.shape[1] / float(resized.shape[1])

        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, tEdged, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)

    cv2.imshow("Image", image)
    # cv2.imwrite('output.jpg', image)
    cv2.waitKey(0)