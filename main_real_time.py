import logging
import cv2 as cv
from config import brightness
from utils.logger import logger
from utils.alignImages import alignImages
from utils.addTrackbar import addTrackbar
from utils.postProcessing import postProcessing
from utils.brightnessChange import brighnessChange
from utils.concatImages import imageConcatHorizontal


def __init__():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Define video capture
    capR = cv.VideoCapture(2)
    capL = cv.VideoCapture(1)
    # Add trackbar
    procParams = addTrackbar('Frames')
    # Iterate over all camera frames
    while True:
        # Capture frame-by-frame
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        # Change brightness
        frameL = brighnessChange(frameL, brightness['lefCam'])
        frameR = brighnessChange(frameR, brightness['rightCam'])
        # Flip the destination frame
        frameR = cv.flip(frameR, 1)
        # if frame is read correctly ret is True
        if not retR or not retL:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        try:
            # Align images
            frameLReg = alignImages(frameL, frameR)
            # Frames Subtraction
            frame = cv.subtract(frameLReg, frameR)
            # Post-processing
            frame = postProcessing(frame, procParams)
            # Concatenate frames
            frame = imageConcatHorizontal([frameR, frameL, frame])
            # Show the frames in a window
            cv.imshow('Marker Detection', frame)
            #logger('Framework finished!')
        except Exception as exception:
            cv.destroyAllWindows()
            logger(f'Running failed!\n{exception}', 'error')

        if cv.waitKey(1) == ord('q'):
            break

    capL.release()
    capR.release()
    cv.destroyAllWindows()


__init__()
