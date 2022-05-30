import cv2 as cv
import numpy as np
from utils.arUcoUtils import arUcoDictionary

defaultGenPath = './generated-markers'

def arUcoMarkerGenerator(id=0, dictType='DICT_ARUCO_ORIGINAL', size=250, outputPath=defaultGenPath):
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
        The path to the output folder (default './generatedMarkers').

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
        fileName = f'ArUco_{dictType}#{"{0:05d}".format(id)}.png'
        cv.imwrite(f'{outputPath}/{fileName}', tag)
        cv.imshow(fileName, tag)
        cv.waitKey(0)
    except Exception as exception:
        print(f'Error occurred when generating the arUco marker!\n{exception}', 'error')

arUcoMarkerGenerator(10, 'DICT_ARUCO_ORIGINAL')