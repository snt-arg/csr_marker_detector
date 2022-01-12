import cv2 as cv
import numpy as np
from utils.logger import logger
from config import maxFeatures, goodMatchPercentage


def alignImages(frameL, frameR):
    """
    Aligns two images using ORB features and descriptors.

    Parameters
    ----------
    frameL: numpy.ndarray
        Frame obtained from the left camera
    frameR: numpy.ndarray
        Frame obtained from the right camera
    """
    try:
        # Convert images to grayscale
        frameRGray = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)
        frameLGray = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)
        # Detect ORB features and compute descriptors
        orb = cv.ORB_create(maxFeatures)
        keypointsL, descriptorsL = orb.detectAndCompute(frameLGray, None)
        keypointsR, descriptorsR = orb.detectAndCompute(frameRGray, None)
        # Match features
        descriptorMatcher = cv.DescriptorMatcher_create(
            cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = descriptorMatcher.match(descriptorsL, descriptorsR, None)
        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)
        # Remove improper matches
        bestMatchesLength = int(len(matches) * goodMatchPercentage)
        matches = matches[:bestMatchesLength]
        # To avoid error when there are no matches
        # assert matches != [], 'No matches found!'
        if (matches == []):
            return frameL
        # Draw top matches
        # imMatches = cv.drawMatches(
        #     frameL, keypointsL, frameR, keypointsR, matches, None)
        # cv.imwrite("matches.jpg", imMatches)
        # Extract location of good matches
        pointsL = np.zeros((len(matches), 2), dtype=np.float32)
        pointsR = np.zeros((len(matches), 2), dtype=np.float32)
        # Iterate over matches
        for index, match in enumerate(matches):
            pointsL[index, :] = keypointsL[match.queryIdx].pt
            pointsR[index, :] = keypointsR[match.trainIdx].pt
        # Find and use homography
        homography, mask = cv.findHomography(pointsL, pointsR, cv.RANSAC)
        # To avoid error when there are no matches
        # assert homography != None, 'No homography found!'
        if (homography is None):
            return frameL
        height, width = frameR.shape[:2]
        # Create registered image for left camera frame
        frameLReg = cv.warpPerspective(
            frameL, homography, (width, height))
        return frameLReg
    except Exception as exception:
        logger(f'Error occurred in alignImages!\n{exception}', 'error')
