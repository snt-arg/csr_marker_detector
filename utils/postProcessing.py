import cv2 as cv
from utils.logger import logger
from utils.filterROI import applyCircularMask


def postProcessing(frame):
    """
    Post-processing of the frame.

    Parameters:
    -----------
    frame: numpy.ndarray
        Frame obtained from the camera

    Returns:
    --------
    processedMask: numpy.ndarray
        Processed frame
    """
    try:
        # Get Trackbar values
        threshold = cv.getTrackbarPos('Threshold', 'Frames')
        erosionKernel = cv.getTrackbarPos('Erosion', 'Frames')
        gaussianKernel = cv.getTrackbarPos('G-Blur', 'Frames')
        # Prevent unacceptable values
        erosionKernel = 1 if erosionKernel == 0 else erosionKernel
        gaussianKernel = 1 if gaussianKernel == 0 else gaussianKernel
        gaussianKernel = gaussianKernel - 1 if gaussianKernel % 2 != 1 else gaussianKernel
        # Convert given image to binary
        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Apply threshold
        frameGray = cv.GaussianBlur(
            frameGray, (gaussianKernel, gaussianKernel), 0)
        _, mask = cv.threshold(frameGray, threshold, 255,
                               cv.THRESH_BINARY + cv.THRESH_OTSU)
        # Apply region of interest
        mask = applyCircularMask(mask)
        # Apply morphological operations
        erodeKernel = cv.getStructuringElement(
            cv.MORPH_RECT, (erosionKernel, erosionKernel))
        mask = cv.morphologyEx(mask, cv.MORPH_ERODE, erodeKernel)
        # Create updated frame
        processedMask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        return processedMask
    except Exception as exception:
        logger(f'Error occurred in postProcessing!\n{exception}', 'error')
