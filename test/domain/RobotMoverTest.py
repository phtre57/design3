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