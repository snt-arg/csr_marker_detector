import os
import cv2 as cv
import numpy as np
from config import defaultGenPath
from markers.arUcoUtils import arUcoDictionary

def markerGenerator(id=0, dictType='DICT_ARUCO_ORIGINAL', size=250, outputPath=defaultGenPath):
    """
    Generates a marker for ARUCO.

    Parameters
    ----------
    id : int
        The id of the marker (default 0).
    dictType : str
        The dictionary type of the marker (default '').
    size : int
        The size of the marker (default 250).
    outputPath : str
        The path to the output folder (default 'generated').

    Returns
    -------
    None
    """
    try:
        # Check if the dictionary type is valid
        if arUcoDictionary[dictType] is None:
            print(f'Dictionary type "{dictType}" not found. Exiting ...')
        # Otherwise, catch the dictionary type
        selectedDict = cv.aruco.Dictionary_get(arUcoDictionary[dictType])
        # Create the marker
        print(f"Creating marker #{id} of {dictType} ...")
        tag = np.zeros((size, size, 1), dtype=np.uint8)
        cv.aruco.drawMarker(selectedDict, id, size, tag, 1)
        # Save the marker to the output folder
        fileName = f'ArUco#{dictType}#{"{0:05d}".format(id)}#{size}.png'
        print(f"Saving the generated marker {fileName} ...")
        cv.imwrite(os.path.join(outputPath, fileName), tag)
        cv.imshow(fileName, tag)
        cv.waitKey(0)
    except Exception as exception:
        print(f'Error occurred when generating the arUco marker!\n{exception}', 'error')