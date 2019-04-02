import cv2

from sequence.DrawSequence import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from domain.image_analysis.Cardinal import *
from util.Logger import Logger

logger = Logger(__name__)


def find_current_center_robot(img, smooth_path):

    cv2.imshow('okk', img)
    cv2.waitKey()

    img = take_image_and_draw(img, smooth_path)

    robot_detector = RobotDetector(img)
    return {'center': robot_detector.find_center_of_robot(), 'image': img}


def rotate_to_north(comm_pi, current_robot_angle):
    rotate_angle = round(90 - current_robot_angle) * -1
    comm_pi.sendAngle(rotate_angle)


def rotate_to_east(comm_pi, current_robot_angle):
    rotate_angle = round(0 - current_robot_angle) * -1
    comm_pi.sendAngle(rotate_angle)


def rotate_to_south(comm_pi, current_robot_angle):
    rotate_angle = round(-90 - current_robot_angle) * -1
    comm_pi.sendAngle(rotate_angle)


def rotate_to_west(comm_pi, current_robot_angle):
    rotate_angle = round(180 - current_robot_angle) * -1
    comm_pi.sendAngle(rotate_angle)


def rotate_robot_on_zone_plane(img, cardinal_point, comm_pi, first_it=0):
    robot_detector = RobotDetector(img)
    robot_angle = robot_detector.find_angle_of_robot()

    __decision(EAST(), rotate_to_east, robot_angle, first_it, cardinal_point,
               comm_pi, img)
    __decision(SOUTH(), rotate_to_south, robot_angle, first_it, cardinal_point,
               comm_pi, img)
    __decision(WEST(), rotate_to_west, robot_angle, first_it, cardinal_point,
               comm_pi, img)
    __decision(NORTH(), rotate_to_north, robot_angle, first_it, cardinal_point,
               comm_pi, img)


def __decision(cardinal, rotate_function, robot_angle, first_it,
               cardinal_point, comm_pi, img):
    if cardinal_point == cardinal:
        logger.log_info("Rotate to " + cardinal + "...")
        rotate_function(comm_pi, robot_angle)
        if first_it < 3:
            logger.log_info('Correction angle ' + str(first_it))
            first_it = first_it + 2
            rotate_robot_on_zone_plane(img, cardinal, comm_pi, first_it)
