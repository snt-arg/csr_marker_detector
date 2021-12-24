import os
import logging
import cv2 as cv
from glob import glob
from utils.logger import logger
import matplotlib.pyplot as plt
from config import cameraLeftFrames, cameraRightFrames


def __init__():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Iterate over all cameraLeft frames
    for frameLAdd in glob(f'{cameraLeftFrames}/*.jpg'):
        frameId = os.path.basename(frameLAdd)
        frameRAdd = cameraRightFrames + '\\' + frameId
        # Load content
        frameDest = cv.imread(frameRAdd, cv.IMREAD_COLOR)
        frameSource = cv.imread(frameLAdd, cv.IMREAD_COLOR)
        frame = cv.hconcat((frameSource, frameDest))
        # Add text showing the frameId
        cv.putText(frame, frameId, (10, 10),
                   cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 2)
        cv.imshow('Frames', frame)
        cv.waitKey(0)


__init__()
