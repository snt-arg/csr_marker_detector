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
