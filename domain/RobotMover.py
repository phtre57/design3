from domain.image_analysis.Cardinal import *

OFFSET_Y_CAM_EMBARKED = 150
OFFSET_X_CAM_EMBARKED = -25


class RobotMover:

    def __init__(self, world_converter, embarked_converter):
        self.world_converter = world_converter
        self.embarked_converter = embarked_converter

    def move_robot_from_embarked_referential(self, x, y, cardinal_string, image_width, image_height):
        x_from_center_of_image = round(x - (
            (image_width / 2) + OFFSET_X_CAM_EMBARKED))
        y_from_center_of_image = round(y - (
            (image_height / 2) + OFFSET_Y_CAM_EMBARKED))

        real_x, real_y = self.robot_cam_pixel_to_xy_converter \
            .convert_pixel_to_xy_point_given_angle((x_from_center_of_image, y_from_center_of_image),
                                                   self.__cardinal_to_angle(cardinal_string))

        return real_x, real_y

    def __cardinal_to_angle(self, cardinal_str):

        if cardinal_str == EAST():
            return 0
        elif cardinal_str == NORTH():
            return 90
        elif cardinal_str == WEST():
            return 180
        elif cardinal_str == SOUTH():
            return -90
        else:
            return None