from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ShapeDetector import *
from domain.image_analysis.opencv_callable.Canny import *

DEBUG = True


class SequencePiece:

    def __init__(self, pixel_to_mm_converter):
        self.pixel_to_mm_converter = pixel_to_mm_converter

    def __calculate_xy_from_center_of_image(self, x, y, height, width):
        return x - width/2, y - height/2

    def find_position_of_wanted_piece_in_image(self, og_frame, p_shape):
        image = og_frame.copy()
        img = image.copy()
        height, width, channels = img.shape

        frame = canny(img, dilate_mask)
        shapeDetector = ShapeDetector(True, False, False)
        shapeDetector.set_peri_limiter(400, 2000)
        shape = shapeDetector.detect(frame, og_frame.copy())
        shape = shapeDetector.detect(shape.frameCnts, og_frame.copy())
        x, y = shapeDetector.get_center_of_wanted_shape(shape.frameCnts, p_shape)
        x_from_center, y_from_center = self.__calculate_xy_from_center_of_image(x, y, height, width)
        x_mm, y_mm = self.pixel_to_mm_converter.convert_to_xy_point_without_scalling((x_from_center, y_from_center))

        if DEBUG:
            print(x_from_center, y_from_center)

            cv2.circle(shape.frameCnts, (x, y), 5, [0, 0, 0])
            cv2.imshow(p_shape, shape.frameCnts)
            cv2.waitKey()

        return x_mm, y_mm
