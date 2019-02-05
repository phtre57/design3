import cv2
from domain.image_path_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar

def test_astar_on_image(image_path):
    img = cv2.imread(image_path)
    test_image = ImageToGridConverter(img)

    astar = Astar(test_image.grid, WIDTH, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.y, point.x), 1, [0, 0, 0])

    return test_image.image

if __name__ == "__main__":
    #test 1
    path1 = test_astar_on_image("../../image_samples/test_table.png")

    #test 2
    path2 = test_astar_on_image("../../image_samples/test_image_2.png")

    #test3
    path3 = test_astar_on_image("../../image_samples/test_image_3.png")

    cv2.imshow("path1", path1)
    cv2.imshow("path2", path2)
    cv2.imshow("path3", path3)
    cv2.waitKey(0)
