import math
from domain.image_analysis.Cardinal import *

OFFSET_Y_CAM_EMBARKED = 140
OFFSET_X_CAM_EMBARKED = -30


class RobotMover:
    def __init__(self, world_converter, embarked_converter):
        self.world_converter = world_converter
        self.embarked_converter = embarked_converter

    def move_robot_from_embarked_referential(self, x, y, cardinal_string,
                                             image_width, image_height):
        x_from_center_of_image = round(x - (
            (image_width / 2) + OFFSET_X_CAM_EMBARKED))
        y_from_center_of_image = round(y - (
            (image_height / 2) + OFFSET_Y_CAM_EMBARKED))

        real_x, real_y = self.embarked_converter \
            .convert_pixel_to_xy_point_given_angle((x_from_center_of_image, y_from_center_of_image),
                                                   self.__cardinal_to_angle(cardinal_string))

        return real_x, real_y

    def fallback_from_cardinality(self, cardinal_str):
        fallback_move = -70

        if cardinal_str == EAST():
            return fallback_move, 0
        elif cardinal_str == NORTH():
            return fallback_move, 0
        elif cardinal_str == WEST():
            return fallback_move, 0
        elif cardinal_str == SOUTH():
            return fallback_move * 2, 0
        else:
            return None

    def get_out_of_object(self, cardinal_str, obstacle_point_array, robot_point):

        closest_point = self.__find_closest_obstacle_from_robot(robot_point, obstacle_point_array)

        if robot_point[0] < closest_point[0]:
            move = (-50, 0)

            move = self.__change_referential(move, cardinal_str)
            return move

        if robot_point[1] < closest_point[1]:
            move = (0, 50)

            move = self.__change_referential(move, cardinal_str)
            return move

        if robot_point[0] > closest_point[0]:
            if robot_point[0] < closest_point[0]:
                move = (50, 0)

                move = self.__change_referential(move, cardinal_str)
                return move

        if robot_point[1] > closest_point[1]:
            move = (0, -50)

            move = self.__change_referential(move, cardinal_str)
            return move


    def move_closer_on_plane(self, cardinal_str):
        move = -15

        if cardinal_str == EAST():
            return 0, move
        elif cardinal_str == NORTH():
            return 0, move
        elif cardinal_str == WEST():
            return 0, move
        elif cardinal_str == SOUTH():
            return 0, move
        else:
            return None

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

    def __change_referential(self, point, cardinal_str):
        if cardinal_str == EAST():
            return (point[0],
                    point[1])

        if cardinal_str == NORTH():
            return (point[1],
                    point[0] * -1)

        if cardinal_str == WEST():
            return (point[0] * -1,
                    point[1] * -1)

        if cardinal_str == SOUTH():
            return (point[1],
                    point[0] * -1)

    def __find_closest_obstacle_from_robot(self, robot_point, obstacle_array):
        min_distance = 10000000000
        closest_pt = ()

        for point in obstacle_array:
            distance = math.sqrt((robot_point[0] - point[0])**2 + (robot_point[1] - point[1]**2))

            if distance < min_distance:
                closest_pt = point

        return closest_pt