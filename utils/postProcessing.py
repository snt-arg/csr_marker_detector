import cv2 as cv
import numpy as np


def postProcessing(frame):
    """
    Post-processing of the frame.

    Parameters:
    -----------
    frame: numpy.ndarray
        Frame obtained from the camera
    """
    # frame = cv.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
