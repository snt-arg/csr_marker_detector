import cv2 as cv
from utils.logger import logger
from vision.alignImages import alignImages
from vision.postProcessing import postProcessing
from vision.concatImages import imageConcatHorizontal

def processFrames(frameL, frameR, retL, retR, procParams):
    """
    Process the frames and return the result

    Parameters
    ----------
    frameL : numpy.ndarray
        Left camera frame
    frameR : numpy.ndarray
        Right camera frame
    retL : bool
        True if the left camera frame is valid
    retR : bool
        True if the right camera frame is valid
    procParams : dict
        Dictionary containing the parameters for the processing

    Returns
    -------
    frame: numpy.ndarray
        The processed frame
    """
    # Define a notFound image
    notFoundImage = cv.imread('notFound.png', cv.IMREAD_COLOR)
    # Retrieve camera frames (and check if they are valid)
    frameL = frameL if retL else notFoundImage
    frameR = frameR if retR else notFoundImage
    try:
        # Align images (if both are retrieved, align them, otherwise, return the notFound image)
        frameLReg = alignImages(frameL, frameR)
        frameRReg = alignImages(frameR, frameL)
        # Frames Subtraction
        frameLR = cv.subtract(frameLReg, frameR)
        frameRL = cv.subtract(frameRReg, frameL)
        # Post-processing
        frameLR = postProcessing(frameLR, procParams)
        frameRL = postProcessing(frameRL, procParams)
        # Concatenate frames
        frame = imageConcatHorizontal([frameR, frameL, frameLR, frameRL])
        # Return the frame to be shown in a window
        return frame
    except Exception as exception:
        logger(f'Running failed!\n{exception}', 'error')
        return imageConcatHorizontal([frameR, frameL, notFoundImage, notFoundImage])