import cv2
import traceback

from domain.pathfinding.Astar import Astar
from domain.pathfinding.Exceptions import *
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from sequence.DrawSequence import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from sequence.UtilSequence import find_current_center_robot
from util.Logger import Logger

logger = Logger(__name__)

DEBUG = False


class PathSequence:
    def __init__(self, pathfinding_astar_retry, actual_pathfinding_image,
                 x_end, y_end):
        self.pathfinding_astar_retry = pathfinding_astar_retry
        self.actual_pathfinding_image = actual_pathfinding_image
        self.X_END = x_end
        self.Y_END = y_end
        self.smooth_path = None
        self.actual_robot_path = []

    def create_smooth_path(self, unsecure=False):
        center_and_image = None
        while True:
            try:
                center_and_image = find_current_center_robot(
                    self.actual_pathfinding_image, self.smooth_path)
                break
            except Exception as ex:
                logger.log_error(ex)
                logger.log_critical(traceback.format_exc())

        grid_converter = ImageToGridConverter(
            center_and_image['image'], center_and_image['center'][0],
            center_and_image['center'][1], self.X_END, self.Y_END)

        astar = Astar(grid_converter.grid, HEIGHT, LENGTH)
        path = astar.find_path()

        if (path == []):
            return None

        path_smoother = PathSmoother(path)
        smooth_path = path_smoother.smooth_path()
        draw_path(smooth_path, grid_converter.image)
        self.smooth_path = smooth_path
        return self.smooth_path
