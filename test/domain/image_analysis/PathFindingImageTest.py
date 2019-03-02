import cv2
import time
from domain.image_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar


def test_astar_on_image(image_path, blur=False):
    img = cv2.imread(image_path)
    if blur:
        img = cv2.GaussianBlur(img, (9, 9), 0)

    test_image = ImageToGridConverter(img, LENGTH - 1, HEIGHT - 1)

    astar = Astar(test_image.grid, HEIGHT, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.j, point.i), 1, [0, 0, 0])

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

def test_on_real_image():
    start = time.time()

    # test 1
    path1 = test_astar_on_image("../../image_samples/real_image/globalmonde.jpg", False)

    path2 = test_astar_on_image("../../image_samples/real_image/globalmonde1.jpg", False)

    path3 = test_astar_on_image("../../image_samples/real_image/globalmonde2.jpg", False)

    path4 = test_astar_on_image("../../image_samples/real_image/globalmonde3.jpg", False)

    path5 = test_astar_on_image("../../image_samples/real_image/globalmonde4.jpg", False)

    path6 = test_astar_on_image("../../image_samples/real_image/globalmonde5.jpg", False)

    path7 = test_astar_on_image("../../image_samples/real_image/globalmonde6.jpg", False)

    path8 = test_astar_on_image("../../image_samples/real_image/globalmonde7.jpg", False)

    path9 = test_astar_on_image("../../image_samples/real_image/globalmonde8.jpg", False)

    path10 = test_astar_on_image("../../image_samples/real_image/globalmonde9.jpg", False)

    end = time.time()
    print("Total time: ", end - start)
    print("Average time: ", (end - start) / 10)

    cv2.imshow("path1", path1)
    cv2.imshow("path2", path2)
    cv2.imshow("path3", path3)
    cv2.imshow("path4", path4)
    cv2.imshow("path5", path5)
    cv2.imshow("path6", path6)
    cv2.imshow("path7", path7)
    cv2.imshow("path8", path8)
    cv2.imshow("path9", path9)
    cv2.imshow("path10", path10)
    cv2.waitKey(0)

if __name__ == "__main__":
    # test_switch: 0 = created with no blur two circles starting point
    # test_switch: 1 = on real image

    test_switch = 1

    if test_switch == 0:
        test_on_robot_discovery_and_path_finding_with_blur()
    elif test_switch == 1:
        test_on_real_image()




