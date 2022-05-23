import cv2 as cv

offset = 10
textColor = (255, 255, 255)
textFont = cv.FONT_HERSHEY_PLAIN

def addLabel(concatedFrame, numberOfConcatedFrames: int):
    """
    Adds a label to the concatenated frame.

    Parameters
    ----------
    concatedFrame: numpy.ndarray
        Concatenated frame.
    """
    # Claculate locations
    height, width, _ = concatedFrame.shape
    xLocation = int(width / numberOfConcatedFrames)
    yLocation = height - offset
    # Add labels
    cv.putText(concatedFrame, "CameraR", (offset, yLocation), textFont, 0.7, textColor, 1)
    cv.putText(concatedFrame, "CameraL", (xLocation + offset, yLocation), textFont, 0.7, textColor, 1)
    cv.putText(concatedFrame, "Mat. L-R", ((xLocation * 2) + offset, yLocation), textFont, 0.7, textColor, 1)
    cv.putText(concatedFrame, "Mat. R-L", ((xLocation * 3) + offset, yLocation), textFont, 0.7, textColor, 1)
    cv.putText(concatedFrame, "Merged", ((xLocation * 4) + offset, yLocation), textFont, 0.7, textColor, 1)