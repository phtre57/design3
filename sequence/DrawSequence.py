import cv2

from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector

SHOW_PATH = False


def draw_robot_on_path_image(actual_pathfinding_image, actual_robot_path,
                             center):
    img = actual_pathfinding_image
    actual_robot_path.append(center)
    if len(actual_robot_path) > 1:
        for i in range(1, len(actual_robot_path)):
            p1 = (actual_robot_path[i - 1][0] * 2,
                  actual_robot_path[i - 1][1] * 2)
            p2 = (actual_robot_path[i][0] * 2, actual_robot_path[i][1] * 2)
            cv2.line(img, p1, p2, [255, 0, 0], 6)

    cv2.circle(img, (center[0] * 2, center[1] * 2), 2, [255, 0, 0])

    comm_ui = Communication_ui()
    comm_ui.SendImage(img, PATHS_IMAGE())

    # cv2.imshow("path", img)
    # cv2.waitKey(0)

    return actual_robot_path


def draw_robot_on_image(actual_pathfinding_image,
                        world_cam_pixel_to_xy_converter, actual_robot_path):
    img = actual_pathfinding_image

    try:
        robot_detector = RobotDetector(img)
        robot_point = robot_detector.find_center_of_robot()
        actual_robot_path.append(robot_point)

        if len(actual_robot_path) > 1:
            for i in range(1, len(actual_robot_path)):
                p1 = (actual_robot_path[i - 1][0] * 2,
                      actual_robot_path[i - 1][1] * 2)
                p2 = (actual_robot_path[i][0] * 2, actual_robot_path[i][1] * 2)
                cv2.line(img, p1, p2, [255, 0, 0], 6)
                p1 = (p1[0] + 3, p1[1] + 3)
                p2 = (p2[0] + 3, p2[1] + 3)
                cv2.line(img, p1, p2, [0, 0, 255], 8)

        comm_ui = Communication_ui()
        comm_ui.SendImage(img, PATHS_IMAGE())
    except Exception:
        pass

    return actual_robot_path


def draw_path(smooth_path, img):
    for point in smooth_path:
        cv2.circle(img, (point[0], point[1]), 2, [0, 0, 255])

    if SHOW_PATH:
        cv2.imshow("path", img)
        cv2.waitKey(0)


def take_image_and_draw(img, smooth_path=None):
    img = img.copy()

    if (smooth_path is not None):
        for point in smooth_path:
            cv2.circle(img, (point[0] * 2, point[1] * 2), 4, [0, 0, 255])

        for i in range(1, len(smooth_path)):
            p1 = (smooth_path[i - 1][0] * 2, smooth_path[i - 1][1] * 2)
            p2 = (smooth_path[i][0] * 2, smooth_path[i][1] * 2)
            cv2.line(img, p1, p2, [0, 0, 255], 8)

    return img
