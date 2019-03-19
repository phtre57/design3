import os
import time
import unittest

from domain.image_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector


def test_astar_on_image(image_path, blur=False):
    img = cv2.imread(image_path)
    if blur:
        img = cv2.GaussianBlur(img, (9, 9), 0)

    robot_detector = RobotDetector(img)
    x_start, y_start = robot_detector.find_center_of_robot()

    test_image = ImageToGridConverter(img, x_start, y_start, 50, 100)

    astar = Astar(test_image.grid, HEIGHT, LENGTH)

    path = astar.find_path()

    path_smoother = PathSmoother(path)
    smooth_path = path_smoother.smooth_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.j, point.i), 1, [0, 0, 0])

    for point in smooth_path:
        cv2.circle(test_image.image, (point[0], point[1]), 1, [0, 0, 255])

    return test_image.image


def test_on_robot_discovery_and_path_finding_with_blur():
    start = time.time()

    # test 1
    path1 = test_astar_on_image("../../image_samples/path_finding/test_image_0.png", True)

    #test 2
    path2 = test_astar_on_image("../../image_samples/path_finding/test_image_1.png", True)

    #test 3
    path3 = test_astar_on_image("../../image_samples/path_finding/test_image_2.png", True)

    # test 4
    path4 = test_astar_on_image("../../image_samples/path_finding/test_image_3.png", True)

    # test 5
    path5 = test_astar_on_image("../../image_samples/path_finding/test_image_4.png", True)

    # test 6
    path6 = test_astar_on_image("../../image_samples/path_finding/test_image_5.png", True)

    end = time.time()
    print("Total time: ", end - start)
    print("Average time: ", (end - start) / 6)

    cv2.imshow("path1", path1)
    cv2.imshow("path2", path2)
    cv2.imshow("path3", path3)
    cv2.imshow("path4", path4)
    cv2.imshow("path5", path5)
    cv2.imshow("path6", path6)
    cv2.waitKey(0)

def test_on_real_image(show_images):
    start = time.time()

    path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
    path = os.path.normpath(os.path.join(path, os.pardir))
    path = os.path.normpath(os.path.join(path, os.pardir))
    path = os.path.join(path, "./image_samples/real_image/")

    # test 1
    path1 = test_astar_on_image(path+"globalmonde.jpg", False)

    path2 = test_astar_on_image(path+"globalmonde1.jpg", False)

    path3 = test_astar_on_image(path+"globalmonde2.jpg", False)

    path4 = test_astar_on_image(path+"globalmonde3.jpg", False)

    path5 = test_astar_on_image(path+"globalmonde4.jpg", False)

    #path6 = test_astar_on_image(path+"globalmonde5.jpg", False)

    #path7 = test_astar_on_image(path+"globalmonde6.jpg", False)

    path8 = test_astar_on_image(path+"globalmonde7.jpg", False)

    path9 = test_astar_on_image(path+"globalmonde8.jpg", False)

    path10 = test_astar_on_image(path+"globalmonde9.jpg", False)

    end = time.time()
    print("Total time: ", end - start)
    print("Average time: ", (end - start) / 10)

    cv2.imshow("path1", path1)
    cv2.imshow("path2", path2)
    cv2.imshow("path3", path3)
    cv2.imshow("path4", path4)
    cv2.imshow("path5", path5)
    #cv2.imshow("path6", path6)
    #cv2.imshow("path7", path7)
    cv2.imshow("path8", path8)
    cv2.imshow("path9", path9)
    cv2.imshow("path10", path10)

    if show_images:
        cv2.waitKey(0)


class PathFindingImageTest(unittest.TestCase):

    def test_pathfinding_on_real_image(self):
        test_on_real_image(False)


