import cv2 as cv
import numpy as np
from config import roiCoverage


def filterROI(image, mask):
    """
    Filters a region of interest from an image based on config.py.

    Parameters:
    -----------
    image: numpy.ndarray
        Image to be filtered
    mask: numpy.ndarray
        Mask to be applied to the image

    Returns:
    --------
    filteredImage: numpy.ndarray
        Filtered image based on region of interest
    """
    # Create a blank image of the same size as the original image
    blankImage = np.zeros_like(image)
    # Obtain frame's height and width and center points
    frameHeight, frameWidth = image.shape[:2]
    centerX, centerY = frameWidth // 2, frameHeight // 2
    # Define the ROI points
    roiWidth = int(frameWidth * roiCoverage[1])
    roiHeight = int(frameHeight * roiCoverage[0])
    p1 = (centerX - roiWidth // 2, centerY - roiHeight // 2)
    p2 = (centerX + roiWidth // 2, centerY - roiHeight // 2)
    p3 = (centerX + roiWidth // 2, centerY + roiHeight // 2)
    p4 = (centerX - roiWidth // 2, centerY + roiHeight // 2)
    dimentions = np.array(
        [[p4, p1, p2, p3]], dtype=np.int32)
    roi = cv.fillPoly(blankImage, dimentions, 255)
    # Apply the ROI
    filteredImage = cv.bitwise_and(image, roi)
    # Return the result
    return filteredImage
