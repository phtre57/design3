import unittest
from domain.RobotMover import *


class RobotMoverTest(unittest.TestCase):

    def setUp(self):
        self.mover = RobotMover()

    def test_given_angle_90_whenToCardinality_thenNorthReturned(self):
        cardinal = self.mover.angle_to_cardinal(90)

        self.assertEqual(cardinal, "NORTH")

    def test_given_angle_0_whenToCardinality_thenEastReturned(self):
        cardinal = self.mover.angle_to_cardinal(0)

        self.assertEqual(cardinal, "EAST")

    def test_given_angle_minus90_whenToCardinality_thenSouthReturned(self):
        cardinal = self.mover.angle_to_cardinal(-90)

        self.assertEqual(cardinal, "SOUTH")

    def test_given_angle_180_whenToCardinality_thenWESTReturned(self):
        cardinal = self.mover.angle_to_cardinal(180)

        self.assertEqual(cardinal, "WEST")

    def test_given_angle_minus_180_whenToCardinality_thenWESTReturned(self):
        cardinal = self.mover.angle_to_cardinal(-180)

        self.assertEqual(cardinal, "WEST")

    def test_given_robot_east_and_obstacle_at_its_left_when_getting_out_of_object_move_returned_isminus50_0(self):
        obstacle_array = [(4, 2)]
        robot_angle = 0
        robot_point = (1, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (-50, 0))

    def test_given_robot_east_and_obstacle_at_its_right_when_getting_out_of_object_move_returned_is50_0(self):
        obstacle_array = [(1, 2)]
        robot_angle = 0
        robot_point = (4, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (50, 0))

    def test_given_robot_east_and_obstacle_at_its_bottom_when_getting_out_of_object_move_returned_is0_50(self):
        obstacle_array = [(1, 5)]
        robot_angle = 0
        robot_point = (1, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (0, 50))

    def test_given_robot_east_and_obstacle_at_its_up_when_getting_out_of_object_move_returned_is0_minus50(self):
        obstacle_array = [(1, 1)]
        robot_angle = 0
        robot_point = (1, 5)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (0, -50))

    def test_given_robot_north_and_obstacle_at_its_left_when_getting_out_of_object_move_returned_is0_minus50(self):
        obstacle_array = [(1, 1)]
        robot_angle = 90
        robot_point = (5, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (0, -50))

    def test_given_robot_north_and_obstacle_at_its_right_when_getting_out_of_object_move_returned_is0_50(self):
        obstacle_array = [(5, 1)]
        robot_angle = 90
        robot_point = (1, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (0, 50))

    def test_given_robot_north_and_obstacle_at_its_bottom_when_getting_out_of_object_move_returned_is50_0(self):
        obstacle_array = [(1, 5)]
        robot_angle = 90
        robot_point = (1, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (50, 0))

    def test_given_robot_north_and_obstacle_at_its_up_when_getting_out_of_object_move_returned_isminus50_0(self):
        obstacle_array = [(1, 1)]
        robot_angle = 90
        robot_point = (1, 5)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (-50, 0))

    def test_given_robot_south_and_obstacle_at_its_left_when_getting_out_of_object_move_returned_is0_50(self):
        obstacle_array = [(1, 1)]
        robot_angle = -90
        robot_point = (5, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (0, 50))

    def test_given_robot_south_and_obstacle_at_its_right_when_getting_out_of_object_move_returned_is0_minus50(self):
        obstacle_array = [(5, 1)]
        robot_angle = -90
        robot_point = (1, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (0, -50))

    def test_given_robot_south_and_obstacle_at_its_bottom_when_getting_out_of_object_move_returned_isminus50_0(self):
        obstacle_array = [(1, 5)]
        robot_angle = -90
        robot_point = (1, 1)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (-50, 0))

    def test_given_robot_south_and_obstacle_at_its_up_when_getting_out_of_object_move_returned_i50_0(self):
        obstacle_array = [(1, 1)]
        robot_angle = -90
        robot_point = (1, 5)

        move = self.mover.get_out_of_object(robot_angle, robot_point, obstacle_array)

        self.assertEqual(move, (50, 0))