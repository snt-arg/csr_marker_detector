import cv2 as cv
from config import threshold, erodeKernelSize, gaussianBlurKernelSize


def addTrackbar(windowName: str):
    """
    Adds a trackbar to the window.

    Parameters
    ----------
    windowName : str
        Name of the window.
    """
    # Define the window
    cv.namedWindow(windowName, cv.WINDOW_NORMAL)
    # Add trackbars
    cv.createTrackbar('Threshold', windowName, threshold, 100, lambda x: None)
    cv.createTrackbar('Erosion', windowName,
                      erodeKernelSize, 50, lambda x: None)
    cv.createTrackbar('G-Blur', windowName,
                      gaussianBlurKernelSize, 50, lambda x: None)
    # Get Trackbar values
    modifiedThreshold = cv.getTrackbarPos('Threshold', 'Frames')
    erosionKernel = cv.getTrackbarPos('Erosion', 'Frames')
    gaussianKernel = cv.getTrackbarPos('G-Blur', 'Frames')
    # Prevent unacceptable values
    erosionKernel = 1 if erosionKernel == 0 else erosionKernel
    gaussianKernel = 1 if gaussianKernel == 0 else gaussianKernel
    gaussianKernel = gaussianKernel - 1 if gaussianKernel % 2 != 1 else gaussianKernel
    # Return values
    return {'threshold': modifiedThreshold, 'erosionKernel': erosionKernel,
            'gaussianKernel': gaussianKernel}
