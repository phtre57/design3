import traceback

from domain.image_analysis.opencv_callable.DetectStartZone import detect_start_zone
from domain.image_analysis.opencv_callable.DetectZoneDepWorld import detect_zone_dep_world
from domain.image_analysis.opencv_callable.DetectPickupZone import detect_pickup_zone
from util.Logger import Logger

logger = Logger(__name__)


class InitSequence():
    def __init__(self, x_end_start_zone, y_end_start_zone, image_taker):
        self.X_END_START_ZONE = x_end_start_zone
        self.Y_END_START_ZONE = y_end_start_zone
        self.image_taker = image_taker
        self.zone_start_point = None
        self.zone_dep_cardinal = None
        self.zone_dep_point = None
        self.zone_pickup_cardinal = None
        self.zone_pickup_point = None

    def init(self):
        self.__detect_start_zone()
        self.__detect_zone_dep()
        self.__detect_pickup_zone()

        return (self.zone_start_point, self.zone_dep_cardinal,
                self.zone_dep_point, self.zone_pickup_cardinal,
                self.zone_pickup_point)

    def take_image(self):
        logger.log_info("Capture d'image de la camera monde en cours...")

        while True:
            ret, img = self.image_taker.read()
            if ret:
                break

        return img

    def __detect_start_zone(self):
        i = 0
        while True:
            try:
                img = self.take_image()
                i = i + 1
                if (i > 20):
                    logger.log_critical(
                        'START ZONE NOT DETECTED, FALL BACK TO HARDCODED')
                    logger.log_debug(traceback.format_exc())
                    self.zone_start_point = (self.X_END_START_ZONE,
                                             self.Y_END_START_ZONE)
                    break

                (x, y) = detect_start_zone(img)
                self.zone_start_point = (round(x / 2), round(y / 2))
                break
            except Exception:
                logger.log_debug('START ZONE NOT DETECTED RETRYING' + str(i))

    def __detect_zone_dep(self):
        i = 0
        while True:
            try:
                img = self.take_image()
                i = i + 1
                res = detect_zone_dep_world(img)
                (x, y) = res['point']
                self.zone_dep_point = (round(x / 2), round(y / 2))
                self.zone_dep_cardinal = res['cardinal']
                break
            except Exception:
                logger.log_debug('ZONE DEP WORLD NOT DETECTED RETRYING' +
                                 str(i))
                if (i > 20):
                    logger.log_critical(
                        'ZONE DEP WORLD NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )
                    logger.log_debug(traceback.format_exc())
                    raise Exception(
                        'ZONE DEP WORLD NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )

    def __detect_pickup_zone(self):

        i = 0
        while True:
            try:
                img = self.take_image()
                i = i + 1
                res = detect_pickup_zone(img)
                (x, y) = res['point']
                self.zone_pickup_point = (round(x / 2), round(y / 2))
                self.zone_pickup_cardinal = res['cardinal']
                break
            except Exception:
                logger.log_debug('PICKUP ZONE NOT DETECTED RETRYING' + str(i))
                if (i > 20):
                    logger.log_critical(
                        'PICKUP ZONE NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )
                    logger.log_debug(traceback.format_exc())
                    raise Exception(
                        'PICKUP ZONE NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )
