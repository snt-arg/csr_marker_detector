import cv2 as cv
import numpy as np
from config import maxFeatures, goodMatchPercentage


def alignImages(frameSource, frameDest):
    """
    Aligns two images using ORB features and descriptors.

    Parameters
    ----------
    frameSource: numpy.ndarray
        Frame obtained from the left camera
    frameDest: numpy.ndarray
        Frame obtained from the right camera
    """
    # Convert images to grayscale
    frameDestGray = cv.cvtColor(frameSource, cv.COLOR_BGR2GRAY)
    frameSourceGray = cv.cvtColor(frameDest, cv.COLOR_BGR2GRAY)
    # Detect ORB features and compute descriptors
    orb = cv.ORB_create(maxFeatures)
    keypointsS, descriptorsS = orb.detectAndCompute(frameSourceGray, None)
    keypointsD, descriptorsD = orb.detectAndCompute(frameDestGray, None)
    # Match features
    descriptorMatcher = cv.DescriptorMatcher_create(
        cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = descriptorMatcher.match(descriptorsS, descriptorsD, None)
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
    # Remove improper matches
    bestMatchesLength = int(len(matches) * goodMatchPercentage)
    matches = matches[:bestMatchesLength]
    # Draw top matches
    # imMatches = cv.drawMatches(
    #     frameSource, keypointsS, frameDest, keypointsD, matches, None)
    # cv.imwrite("matches.jpg", imMatches)
    # Extract location of good matches
    pointsS = np.zeros((len(matches), 2), dtype=np.float32)
    pointsD = np.zeros((len(matches), 2), dtype=np.float32)
    for index, match in enumerate(matches):
        pointsS[index, :] = keypointsS[match.queryIdx].pt
        pointsD[index, :] = keypointsD[match.trainIdx].pt
    # Find and use homography
    h, mask = cv.findHomography(pointsS, pointsD, cv.RANSAC)
    height, width, channels = frameDest.shape
    # Create registered image for L
    frameSourceReg = cv.warpPerspective(frameSource, h, (width, height))
    return frameSourceReg, h
