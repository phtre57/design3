import cv2
import time
import numpy as np
import os

from infrastructure.communication_pi.comm_pi import Communication_pi

LENGTH = 640
HEIGHT = 480

path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
path = os.path.join(path, "./samples/piece")

# cap = cv2.VideoCapture(1)

# cap.set(10, 70)
# cap.set(11, 19)
# cap.set(12, 100)
# cap.set(13, -4)
# cap.set(14, -100)
# cap.set(15, -4)

comm_pi = Communication_pi()


def increment_cam_number(path_file):
    file_number = open(path_file).read()

    new_file_number = int(file_number) + 1
    new_file_number = str(new_file_number)

    f = open(path_file, 'w')
    f.write(new_file_number)
    f.close()


def save_frame(img):
    file_no_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "cam_count.txt"))
    file_no = open(file_no_path).read()
    path1 = path + file_no + '.jpg'
    increment_cam_number(file_no_path)
    cv2.imwrite(path1, img)


img = None
while True:
    img = comm_pi.getImage()
    img = cv2.resize(img, (320, 240))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img[..., 1] = img[..., 1] * 1
    # img[..., 2] = img[..., 2] * 1
    # img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    # cv2.circle(img, (round(320 / 2), round(240 / 2)), 3, [255, 51, 51])
    save_frame(img)
    cv2.imshow('ok', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # if ret:
    # break

# img = cv2.resize(img, (LENGTH, HEIGHT))

cv2.destroyAllWindows()

# cap.release()