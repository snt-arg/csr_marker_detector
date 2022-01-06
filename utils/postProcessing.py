import cv2 as cv
from utils.logger import logger
from config import threshold, gaussianBlurKernelSize, erodeKernelSize


def postProcessing(frame):
    """
    Post-processing of the frame.

    Parameters:
    -----------
    frame: numpy.ndarray
        Frame obtained from the camera
    """
    try:
        # Convert given image to binary
        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Apply threshold
        frameGray = cv.GaussianBlur(frameGray, gaussianBlurKernelSize, 0)
        _, mask = cv.threshold(frameGray, threshold, 255,
                               cv.THRESH_BINARY + cv.THRESH_OTSU)
        # Apply morphological operations
        erodeKernel = cv.getStructuringElement(cv.MORPH_RECT, erodeKernelSize)
        mask = cv.morphologyEx(mask, cv.MORPH_ERODE, erodeKernel)
        # Create updated frame
        result = cv.bitwise_and(frame, frame, mask=mask)
        return result
    except Exception as exception:
        logger(f'Error occurred in postProcessing!\n{exception}', 'error')
