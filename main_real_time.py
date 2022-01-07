import os
import logging
import cv2 as cv
from glob import glob
from utils.logger import logger
from utils.alignImages import alignImages
from utils.postProcessing import postProcessing
from utils.concatImages import imageConcatHorizontal
from config import cameraLeftFrames, cameraRightFrames

def __init__():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Iterate over all cameraLeft frames
    capR = cv.VideoCapture(2)
    capL = cv.VideoCapture(4)
    while True:
        # Capture frame-by-frame
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        # Flip the destination frame
        frameR = cv.flip(frameR, 1) 
        # if frame is read correctly ret is True
        if not retR or not retL:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        #cv.imshow('FramesL', frameL)
        #cv.imshow('FramesR', frameR)
        #fourcc = cv.VideoWriter_fourcc(*'XVID')
        #out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


        try:
            # Align images
            frameLReg, homography = alignImages(frameL, frameR)
            # logger(f"Estimated homography for {frameId}:\n {homography}")
            frame = cv.subtract(frameLReg, frameR)
            # Post-processing
            frame = postProcessing(frame)
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

        #if cv.waitKey(1) == ord('s'):
        #    out.write(frame) 
        # When everything done, release the capture
    capL.release()
    capR.release()
    cv.destroyAllWindows()

__init__()
