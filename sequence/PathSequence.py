import cv2
import traceback

from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from sequence.DrawSequence import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from sequence.UtilSequence import find_current_center_robot
from util.Logger import Logger

logger = Logger(__name__)


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

        grid_converter = None
        try:
            if unsecure:
                self.pathfinding_astar_retry = self.pathfinding_astar_retry + 1
                print(self.pathfinding_astar_retry)
                print(OBSTACLE_BORDER - 5 * self.pathfinding_astar_retry)
                grid_converter = ImageToGridConverter(
                    center_and_image['image'], center_and_image['center'][0],
                    center_and_image['center'][1], self.X_END, self.Y_END,
                    OBSTACLE_BORDER - 5 * self.pathfinding_astar_retry,
                    LEFT_OBSTACLE_BORDER - 5 * self.pathfinding_astar_retry)
                logger.log_critical(
                    "Unsecure pathfinding with new grid converter with new value for obstacle border: "
                    + str(grid_converter.get_obstacle_border()))
            else:
                grid_converter = ImageToGridConverter(
                    center_and_image['image'], center_and_image['center'][0],
                    center_and_image['center'][1], self.X_END, self.Y_END)
                # grid_converter = ImageToGridConverter(
                #     center_and_image['image'], center_and_image['center'][0],
                #     center_and_image['center'][1], self.X_END, self.Y_END, 0,
                #     0, CIRCLE_OBSTACLE_RADIUS, True)

            astar = Astar(grid_converter.grid, HEIGHT, LENGTH)
            path = astar.find_path()

            if (path == []):
                return None

            path_smoother = PathSmoother(path)
            smooth_path = path_smoother.smooth_path()
            draw_path(smooth_path, grid_converter.image)
            self.smooth_path = smooth_path
            return self.smooth_path
        except Exception as ex:
            if (isinstance(ex, NoBeginingPointException)):
                logger.log_debug('NoBeginingPointException have been raised')
                logger.log_debug(ex)
                logger.log_debug(traceback.format_exc())
                self.create_smooth_path(True)
                pass
            else:
                logger.log_debug(ex)
                logger.log_debug(traceback.format_exc())
                if (DEBUG):
                    frame = self.actual_pathfinding_image
                    cv2.circle(frame, (self.X_END * 2, self.Y_END * 2), 1,
                               [0, 0, 255])
                    cv2.imshow('OBSTACLE PATH', frame)
                    cv2.waitKey()
                raise ex