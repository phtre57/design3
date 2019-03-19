import socketio
import argparse
import cv2

from domain.image_analysis.opencv_callable.DetectTable import *
from domain.image_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar
from test.domain.image_analysis.PathFindingImageTest import test_astar_on_image
from domain.image_analysis.opencv_callable.DetectQR import decode
from domain.image_analysis.opencv_callable.DetectContourPieces import *
from domain.image_analysis.opencv_callable.DetectZoneDep import *
from infrastructure.communication_pi.comm_pi import *
from infrastructure.communication_ui.comm_ui import *

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--d', dest='debug', type=bool, default=False, help='debug mode')
args = parser.parse_args()

def pathfinding(path, x, y):
    frame = cv2.imread(path)

    test_image = ImageToGridConverter(frame, x, y)
    astar = Astar(test_image.grid, HEIGHT, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.j, point.i), 1, [0, 0, 0])

    frame = test_image.image

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "optpath")

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "actualpath")

    cv2.imshow("main", frame)
    cv2.waitKey()

def main_sequence():
    pathfinding("./image_samples/real_image/globalmonde1.jpg", 240, 135)

    path = "./image_samples/real_image/qr.png"
    frame = cv2.imread(path)
    obj = decode(frame)

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "actualimg")

    comm_ui = Communication_ui()
    comm_ui.SendText(obj.data, "qrcode")

    pathfinding("./image_samples/real_image/globalmonde1QR.jpg", 235, 60)

    path = "./image_samples/real_image/pieces.jpg"
    frame = cv2.imread(path)
    shape = detect_contour_pieces(frame)

    comm_ui = Communication_ui()
    comm_ui.SendImage(shape.frame, "actualimg")

    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneDep.jpg", 25, 122)

    path = "./image_samples/real_image/zonedep.jpg"
    frame = cv2.imread(path)
    shape = detect_zone_dep(frame)

    comm_ui = Communication_ui()
    comm_ui.SendImage(shape.frame, "actualimg")

    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneBlanche.jpg", 75, 100)

    print("Sequence done")

    init_conn()

def init_conn():
    print("Waiting start signal")
    sio = socketio.Client()
    sio.connect('http://localhost:4000?token=MainRobot')

    @sio.on('validation')
    def on_validation(v):
        print('disconnect MainRobot')
        sio.disconnect()

    @sio.on('start')
    def on_start(v):
        print('Start signal')
        sio.emit("eventFromRobot", {'data': 'Started', 'type': 'text', 'dest': 'phase' })
        main_sequence()

def main():
    if (args.debug):
        print("debug")
        # connectToPi()
        # sendCoordinates('200 0\n')
    else:
        init_conn()

main()