import time
import cv2
import traceback
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from infrastructure.communication_pi import __comm_pi


def take_image():
    try:
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        cap.release()

        #cv2.imshow("imageCourante", img)
        #cv2.waitKey(0)

        return img
    except Exception as ex:
        print("Camera not working")


def test():
    __comm_pi.connectToPi()
    time.sleep(5)

    __comm_pi.sendCoordinates("0,0,-10\n")
    time.sleep(5)

    print("Rotating robot phase: ")
    counter = 0

    start = time.time()

    while counter < 31:
        try:
            img = take_image()

            robot_detector = RobotDetector(img)
            robot_angle = robot_detector.find_angle_of_robot()
            print("Angle: " + str(robot_angle))
            end = time.time() - start
            print("Time: " + str(end))

            counter = counter + 1
        except Exception as ex:
            print(ex)

    final = time.time() - start
    print("Total Time: " + str(final))

    __comm_pi.sendCoordinates("0,0,0\n")


test()


