import cv2
import time
from domain.image_path_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar


def test_astar_on_image(image_path, blur=False):
    img = cv2.imread(image_path)
    if blur:
        img = cv2.GaussianBlur(img, (21, 21), 0)

    test_image = ImageToGridConverter(img)

    astar = Astar(test_image.grid, WIDTH, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.j, point.i), 1, [0, 0, 0])

    return test_image.image

def test_on_clear_created_image():
    start = time.time()

    # test 1
    path1 = test_astar_on_image("../../image_samples/test_table.png")

    # test 2
    path2 = test_astar_on_image("../../image_samples/test_image_2.png")

    # test3
    path3 = test_astar_on_image("../../image_samples/test_image_3.png")

    # test4
    path4 = test_astar_on_image("../../image_samples/test_image_4.png")

    # test5
    path5 = test_astar_on_image("../../image_samples/test_image_5.png")

    # test6
    path7 = test_astar_on_image("../../image_samples/test_image_7.png")

    # test7
    path8 = test_astar_on_image("../../image_samples/test_image_8.png")

    # test8
    path9 = test_astar_on_image("../../image_samples/test_image_9.png")

    end = time.time()
    print(end - start)
    print((end - start) / 8)

    cv2.imshow("path1", path1)
    cv2.imshow("path2", path2)
    cv2.imshow("path3", path3)
    cv2.imshow("path4", path4)
    cv2.imshow("path5", path5)
    cv2.imshow("path7", path7)
    cv2.imshow("path8", path8)
    cv2.imshow("path9", path9)
    cv2.waitKey(0)


def test_on_blurred_created_image():
    start = time.time()

    # test 1
    path1 = test_astar_on_image("../../image_samples/test_table.png", True)

    # test 2
    path2 = test_astar_on_image("../../image_samples/test_image_2.png", True)

    # test3
    path3 = test_astar_on_image("../../image_samples/test_image_3.png", True)

    # test4
    path4 = test_astar_on_image("../../image_samples/test_image_4.png", True)

    # test5
    path5 = test_astar_on_image("../../image_samples/test_image_5.png", True)

    # test6
    path7 = test_astar_on_image("../../image_samples/test_image_7.png", True)

    # test7
    path8 = test_astar_on_image("../../image_samples/test_image_8.png", True)

    # test8
    path9 = test_astar_on_image("../../image_samples/test_image_9.png", True)

    end = time.time()
    print(end - start)
    print((end - start) / 8)

    cv2.imshow("path1", path1)
    cv2.imshow("path2", path2)
    cv2.imshow("path3", path3)
    cv2.imshow("path4", path4)
    cv2.imshow("path5", path5)
    cv2.imshow("path7", path7)
    cv2.imshow("path8", path8)
    cv2.imshow("path9", path9)
    cv2.waitKey(0)

if __name__ == "__main__":
    # test_switch: 0 = created with no blur
    # test_switch: 1 = created with blur

    test_switch = 1

    if test_switch == 0:
        test_on_clear_created_image()
    elif test_switch == 1:
        test_on_blurred_created_image()



