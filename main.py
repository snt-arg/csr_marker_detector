import os
import logging
import cv2 as cv
from glob import glob
from utils.logger import logger
from utils.alignImages import alignImages
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
            frameDest = cv.imread(frameRAdd, cv.IMREAD_COLOR)
            frameSource = cv.imread(frameLAdd, cv.IMREAD_COLOR)
            # Flip the destination frame
            frameDest = cv.flip(frameDest, 1)
            # Align images
            frameSourceReg, homography = alignImages(frameSource, frameDest)
            logger(f"Estimated homography for {frameId}:\n {homography}")
            frame = cv.subtract(frameSourceReg, frameDest)
            frame = cv.hconcat((frameDest, frameSourceReg))
            # Add text showing the frameId
            cv.putText(frame, frameId, (10, 10),
                       cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 2)
            cv.imshow('Frames', frame)
            cv.waitKey(0)
    except KeyboardInterrupt:
        cv.destroyAllWindows()
        logger('Framework stopped!')


__init__()
