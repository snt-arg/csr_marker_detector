import os
import logging
import cv2 as cv
from glob import glob
from utils.logger import logger
from utils.alignImages import alignImages
from utils.postProcessing import postProcessing
from utils.concatImages import imageConcatHorizontal
from config import cameraLeftFrames, cameraRightFrames, flipImage


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
            if flipImage:
                frameL = cv.flip(frameL, 1)
            # Align images
            frameLReg, homography = alignImages(frameL, frameR)
            # logger(f"Estimated homography for {frameId}:\n {homography}")
            frame = cv.subtract(frameLReg, frameR)
            # Post-processing
            frame = postProcessing(frame)
            # Concatenate frames
            frame = imageConcatHorizontal([frameR, frameL, frame])
            # Add some text to the frame
            cv.putText(frame, frameId, (10, 20),
                       cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 2)
            height = frame.shape[0]
            cv.putText(frame, '[Esc]: Quit', (10, height - 10),
                       cv.FONT_HERSHEY_PLAIN, 1, (0, 215, 255), 1, 2)
            # Show the frames in a window
            cv.imshow('Frames', frame)
            pressedKey = cv.waitKey(1)
            # Stop in case user presses 'Esc'
            if pressedKey == 27:
                logger('Framework stopped by user!')
                cv.destroyAllWindows()
                break
        # Create a log when finished
        logger('Framework finished!')
    except Exception as exception:
        cv.destroyAllWindows()
        logger(f'Running failed!\n{exception}', 'error')


__init__()
