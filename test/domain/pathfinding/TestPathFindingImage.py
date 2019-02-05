import cv2
from domain.image_path_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar


if __name__ == "__main__":
    img = cv2.imread("../../image_samples/test_table.png")
    test_image = ImageToGridConverter(img)

    astar = Astar(test_image.grid, WIDTH, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.y, point.x), 1, [0, 0, 0])

    cv2.imshow("path", test_image.image)
    cv2.waitKey(0)
