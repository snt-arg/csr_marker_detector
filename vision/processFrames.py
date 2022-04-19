import cv2 as cv
from utils.logger import logger
from vision.alignImages import alignImages
from vision.postProcessing import postProcessing
from vision.concatImages import imageConcatHorizontal

def processFrames(frameL, frameR, procParams):
    try:
        # Align images
        frameLReg = alignImages(frameL, frameR)
        # Frames Subtraction
        frame = cv.subtract(frameLReg, frameR)
        # Post-processing
        frame = postProcessing(frame, procParams)
        # Concatenate frames
        frame = imageConcatHorizontal([frameR, frameL, frame])
        # Return the frame to be shown in a window
        return frame
    except Exception as exception:
        logger(f'Running failed!\n{exception}', 'error')