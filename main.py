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
        for frameLAddr in glob(f'{cameraLeftFrames}/*.jpg'):
            frameId = os.path.basename(frameLAddr)
            frameRAddr = cameraRightFrames + '\\' + frameId
            # Load content
            frameR = cv.imread(frameRAddr, cv.IMREAD_COLOR)
            frameL = cv.imread(frameLAddr, cv.IMREAD_COLOR)
            # Flip the destination frame
            frameR = cv.flip(frameR, 1)
            # Align images
            frameLReg, homography = alignImages(frameL, frameR)
            # logger(f"Estimated homography for {frameId}:\n {homography}")
            frame = cv.subtract(frameLReg, frameR)
            # frame = cv.hconcat((frameR, frameLReg))
            # Post-processing
            postProcessing(frame)
            # Bounding-box Drawer
            # Add text showing the frameId
            cv.putText(frame, frameId, (10, 20),
                       cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 2)
            # Show the frames in a window
            cv.imshow('Frames', frame)
            pressedKey = cv.waitKey(1)
            # Stop, in case user presses 'q' or 'Esc'
            if pressedKey == 27:
                break
            # Finish
            logger('Framework finished!')
    except KeyboardInterrupt:
        cv.destroyAllWindows()
        logger('Framework stopped!')


__init__()
