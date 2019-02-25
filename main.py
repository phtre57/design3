import socketio
import argparse

from domain.image_analysis.DetectTable import *
from domain.image_path_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar
from test.domain.pathfinding.TestPathFindingImage import test_astar_on_image
from domain.image_analysis.QR import decode
from domain.image_analysis.DetectContourPieces import *
from domain.image_analysis.DetectZoneDep import *
from infrastructure.communication_pi.comm_pi import *
from infrastructure.communication.comm import SendImage, SendText

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
    SendImage(frame, "optpath")
    SendImage(frame, "actualpath")
    cv2.imshow("main", frame)
    cv2.waitKey()

def main_sequence():
    pathfinding("./image_samples/real_image/globalmonde1.jpg", 240, 135)

    path = "./image_samples/real_image/qr.png"
    frame = cv2.imread(path)
    obj = decode(frame)

    SendImage(frame, "actualimg")
    SendText(obj.data, "qrcode")

    pathfinding("./image_samples/real_image/globalmonde1QR.jpg", 235, 60)

    path = "./image_samples/real_image/pieces.jpg"
    frame = cv2.imread(path)
    shape = detect_contour_pieces(frame)

    SendImage(shape.frame, "actualimg")

    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneDep.jpg", 25, 122)

    path = "./image_samples/real_image/zonedep.jpg"
    frame = cv2.imread(path)
    shape = detect_zone_dep(frame)

    SendImage(shape.frame, "actualimg")

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
        sio.disconnect()

    @sio.on('start')
    def on_start(v):
        print('Start signal')
        sio.emit("eventFromRobot", {'data': 'Started', 'type': 'text', 'dest': 'phase' })
        main_sequence()

def main():
    if (args.debug):
        # connectToPi()
        # sendCoordinates('200 0\n')
    else:
        init_conn()



main()