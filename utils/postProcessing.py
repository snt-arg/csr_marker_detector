import cv2 as cv
from config import threshold, gaussianBlurKernel


def postProcessing(frame):
    """
    Post-processing of the frame.

    Parameters:
    -----------
    frame: numpy.ndarray
        Frame obtained from the camera
    """
    # Convert given image to binary
    frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Apply threshold
    frameGray = cv.GaussianBlur(frameGray, gaussianBlurKernel, 0)
    _, mask = cv.threshold(frameGray, threshold, 255,
                           cv.THRESH_BINARY + cv.THRESH_OTSU)
    # Create updated frame
    result = cv.bitwise_and(frame, frame, mask=mask)
    return result
