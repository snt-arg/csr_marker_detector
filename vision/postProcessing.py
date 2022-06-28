import cv2 as cv
from utils.logger import logger
from vision.filterROI import applyCircularMask


def postProcessing(frame, procParams):
    """
    Post-processing of the frame.

    Parameters:
    -----------
    frame: numpy.ndarray
        Frame obtained from the camera
    procParams: dict
        Dictionary with the parameters for the post-processing

    Returns:
    --------
    processedMask: numpy.ndarray
        Processed frame
    """
    try:
        # Convert image to grayscale
        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Apply threshold
        frameGray = cv.GaussianBlur(
            frameGray, (int(procParams['gaussianKernel']), int(procParams['gaussianKernel'])), 0)
        _, mask = cv.threshold(frameGray, procParams['threshold'], 255,
                               cv.THRESH_BINARY + cv.THRESH_OTSU)
        # Apply region of interest
        mask = applyCircularMask(mask, procParams['circlularMaskCoverage'])
        # Apply morphological operations
        erodeKernel = cv.getStructuringElement(
            cv.MORPH_RECT, (int(procParams['erosionKernel']), int(procParams['erosionKernel'])))
        mask = cv.morphologyEx(mask, cv.MORPH_ERODE, erodeKernel)
        # Create updated frame
        processedMask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        return processedMask
    except Exception as exception:
        logger(f'Error occurred in postProcessing!\n{exception}', 'error')
