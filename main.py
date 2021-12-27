import os
import logging
import cv2 as cv
from glob import glob
from utils.logger import logger
from utils.alignImages import alignImages
from utils.postProcessing import postProcessing
from config import cameraLeftFrames, cameraRightFrames


def __init__():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Iterate over all cameraLeft frames
    try:
        for frameLAdd in glob(f'{cameraLeftFrames}/*.jpg')[:5]:
            frameId = os.path.basename(frameLAdd)
            frameRAdd = cameraRightFrames + '\\' + frameId
            # Load content
            frameR = cv.imread(frameRAdd, cv.IMREAD_COLOR)
            frameL = cv.imread(frameLAdd, cv.IMREAD_COLOR)
            # Flip the destination frame
            frameR = cv.flip(frameR, 1)
            # Align images
            frameLReg, homography = alignImages(frameL, frameR)
            logger(f"Estimated homography for {frameId}:\n {homography}")
            frame = cv.subtract(frameLReg, frameR)
            # frame = cv.hconcat((frameR, frameLReg))
            # Post-processing
            postProcessing(frame)
            # Add text showing the frameId
            cv.putText(frame, frameId, (10, 20),
                       cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 2)
            cv.imshow('Frames', frame)
            cv.waitKey(0)
    except KeyboardInterrupt:
        cv.destroyAllWindows()
        logger('Framework stopped!')


__init__()
