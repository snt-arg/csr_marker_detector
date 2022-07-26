import logging
import cv2 as cv
import PySimpleGUI as sg
from utils.logger import logger
from vision.addLabel import addLabel
from utils.guiElements import guiElements
from config import ports, fpsBoost, flipImage
from vision.processFrames import processFrames
from markers.arUcoGenerator import markerGenerator

def main():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Create the window
    windowTitle, tabGroup, imageViewer = guiElements()
    window = sg.Window(windowTitle, [tabGroup, imageViewer], location=(800, 400))
    capL, capR = cv.VideoCapture(ports['lCam']), cv.VideoCapture(ports['rCam'])

    # Get the frame-rate of the cameras
    if fpsBoost:
        capL.set(cv.CAP_PROP_FPS, 30.0)
        capR.set(cv.CAP_PROP_FPS, 30.0)

    # Create an event loop
    while True:
        event, values = window.read(timeout=10)
        # End program if user closes window
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Retrieve frames
        # Note: if each of the cameras not working, retX will be False
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        # Get the values from the GUI
        guiValues = {'maxFeatures': values['MaxFeat'], 'goodMatchPercentage': values['MatchRate'],
                    'circlularMaskCoverage': values['CircMask'], 'threshold': values['Threshold'],
                    'erosionKernel': values['Erosion'], 'gaussianKernel': values['Gaussian'],
                    'enableCircularMask': values['CircMaskEnable'],
                    }
        # Check for any button presses
        if event == 'Generate':
            markerGenerator(int(values['MarkerId']), values['MarkerDict'], int(values['MarkerSize']))
        # Change brightness
        frameL = cv.convertScaleAbs(frameL, alpha=values['camAlpha'], beta=values['camBeta'])
        frameR = cv.convertScaleAbs(frameR, alpha=values['camAlpha'], beta=values['camBeta'])
        # Flip the right frame
        if (flipImage):
            frameR = cv.flip(frameR, 1)
        # Process frames
        frame = processFrames(frameL, frameR, retL, retR, guiValues)
        # Add text to the image
        addLabel(frame, 5)
        # Show the frames
        frame = cv.imencode(".png", frame)[1].tobytes()
        window['Frames'].update(data=frame)
    
    capL.release()
    capR.release()
    window.close()
    logger('Framework finished!')

# Run the program
main()