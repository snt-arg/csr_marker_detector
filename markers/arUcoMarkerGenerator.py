import sys
import cv2 as cv
import numpy as np
from utils.arUcoUtils import arUcoDictionary

defaultGeneratedMarkersPath = './generatedMarkers'

def arUcoMarkerGenerator(id = 0, dictType = arUcoDictionary['DICT_ARUCO_ORIGINAL'], outputPath = defaultGeneratedMarkersPath):
    """
    Generates a marker for ARUCO.

    Parameters
    ----------
    id : int
        The id of the marker (default 0).
    dictType : str
        The dictionary type of the marker (default '').
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
        # Otherwise, generate the marker
        selectedDict = cv.aruco.Dictionary_get(arUcoDictionary[dictType])
        print(selectedDict)
    except Exception as exception:
        print(f'Error occurred when generating the arUco marker!\n{exception}', 'error')

arUcoMarkerGenerator(0, 'DICT_ARUCO_ORIGINAL', defaultGeneratedMarkersPath)

# https://pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/