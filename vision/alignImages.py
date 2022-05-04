import cv2 as cv
import numpy as np
from utils.logger import logger
from config import maxFeatures, goodMatchPercentage


def alignImages(frame1, frame2):
    """
    Aligns two images using ORB features and descriptors.

    Parameters
    ----------
    frame1: numpy.ndarray
        Frame obtained from the left camera
    frame2: numpy.ndarray
        Frame obtained from the right camera
    """
    try:
        # Convert images to grayscale
        frame2Gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        frame1Gray = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        # Detect ORB features and compute descriptors
        orb = cv.ORB_create(maxFeatures)
        keypointsL, descriptorsL = orb.detectAndCompute(frame1Gray, None)
        keypointsR, descriptorsR = orb.detectAndCompute(frame2Gray, None)
        # Match features
        descriptorMatcher = cv.DescriptorMatcher_create(
            cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = descriptorMatcher.match(descriptorsL, descriptorsR, None)
        matches = list(matches)
        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)
        # Remove improper matches
        bestMatchesLength = int(len(matches) * goodMatchPercentage)
        matches = matches[:bestMatchesLength]
        # When there are no matches, return the original frame
        if (matches == []):
            return frame2
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
            return frame1
        height, width = frame2.shape[:2]
        # Create registered image for left camera frame
        frame1Reg = cv.warpPerspective(
            frame1, homography, (width, height))
        return frame1Reg
    except Exception as exception:
        logger(f'Error occurred in alignImages!\n{exception}', 'error')
