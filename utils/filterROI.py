import cv2 as cv
import numpy as np
from config import circlularMaskCoverage


def applyCircularMask(image):
    """
    Filters a region of interest from an image based on config.py.

    Parameters:
    -----------
    image: numpy.ndarray
        Image to be filtered

    Returns:
    --------
    filteredImage: numpy.ndarray
        Filtered image based on region of interest
    """
    # Obtain frame's height and width and center points
    frameHeight, frameWidth = image.shape[:2]
    centerX, centerY = frameWidth // 2, frameHeight // 2
    # Define the circle
    radius = int(centerY * circlularMaskCoverage) if frameHeight < frameWidth else int(
        centerX * circlularMaskCoverage)
    # Create a blank image of the same size as the original image
    mask = np.zeros_like(image)
    mask = cv.circle(mask, (centerX, centerY), radius, (255, 255, 255), -1)
    # Subtraction
    mask = cv.bitwise_and(mask, image)
    # Return the result
    return mask
