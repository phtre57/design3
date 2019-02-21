from domain.image_analysis.DetectTable import *
from domain.image_path_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar
from test.domain.pathfinding.TestPathFindingImage import test_astar_on_image
from domain.image_analysis.QR import decode
from domain.image_analysis.DetectContourPieces import *
from domain.image_analysis.DetectZoneDep import *

def pathfinding(path, x, y):
    frame = cv2.imread(path)

    test_image = ImageToGridConverter(frame, x, y)
    astar = Astar(test_image.grid, HEIGHT, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.j, point.i), 1, [0, 0, 0])

    frame = test_image.image
    cv2.imshow("main", frame)
    cv2.waitKey()

def main():
    # WAIT FOR START UI
    # socketio wait 

    pathfinding("./image_samples/real_image/globalmonde1.jpg", 240, 135)

    path = "./image_samples/real_image/qr.jpg"
    frame = cv2.imread(path)
    obj = decode(frame)

    pathfinding("./image_samples/real_image/globalmonde1QR.jpg", 235, 60)

    path = "./image_samples/real_image/pieces.jpg"
    frame = cv2.imread(path)
    shape = detect_contour_pieces(frame)
    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneDep.jpg", 25, 122)

    path = "./image_samples/real_image/zonedep.jpg"
    frame = cv2.imread(path)
    shape = detect_zone_dep(frame)
    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneBlanche.jpg", 75, 100)

main()