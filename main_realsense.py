import logging
import cv2 as cv
import numpy as np
import PySimpleGUI as sg
import pyrealsense2 as rs
from utils.logger import logger
from vision.addLabel import addLabel
from utils.guiElements import guiElements
from vision.processFrames import processFrames
from markers.arUcoGenerator import markerGenerator

def main():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started! (RealSense version)')
    # Create the window
    windowTitle, tabGroup, imageViewer = guiElements()
    window = sg.Window(windowTitle, [tabGroup, imageViewer], location=(800, 400))
    # Preparing RealSense pipeline
    realSensePoints = rs.points()
    realSenseConfig = rs.config()
    realSensePipeline = rs.pipeline()
    # Preparing profile
    realSenseConfig.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
    realSenseConfig.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)
    realSenseProfile = realSensePipeline.start(realSenseConfig)
    # Disable IR emitter
    device = realSenseProfile.get_device()
    depthSensor = device.query_sensors()[0]
    depthSensor.set_option(rs.option.emitter_enabled, 0)

    # Create an event loop
    try:
        while True:
            frames = realSensePipeline.wait_for_frames()
            # Capture infrared frames
            capL = frames.get_infrared_frame(1)
            capR = frames.get_infrared_frame(2)
            if not capL or not capR:
                continue
            event, values = window.read(timeout=10)
            # End program if user closes window
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            # Retrieve frames
            retL = np.asanyarray(capL.get_data())
            retR = np.asanyarray(capR.get_data())
            # Get the values from the GUI
            guiValues = {'maxFeatures': values['MaxFeat'], 'goodMatchPercentage': values['MatchRate'],
                        'circlularMaskCoverage': values['CircMask'], 'threshold': values['Threshold'],
                        'erosionKernel': values['Erosion'], 'gaussianKernel': values['Gaussian'],
                        'enableCircularMask': values['CircMaskEnable']
                        }
            # Check for any button presses
            if event == 'Generate':
                markerGenerator(int(values['MarkerId']), values['MarkerDict'], int(values['MarkerSize']))
            # Convert images to grayscale
            retL = cv.cvtColor(retL, cv.COLOR_GRAY2RGB)
            retR = cv.cvtColor(retR, cv.COLOR_GRAY2RGB)
            # Change brightness
            retL = cv.convertScaleAbs(retL, alpha=values['camAlpha'], beta=values['camBeta'])
            retR = cv.convertScaleAbs(retR, alpha=values['camAlpha'], beta=values['camBeta'])
            # Process frames
            frame = processFrames(retL, retR, True, True, guiValues)
            # Add text to the image
            addLabel(frame, 5)
            # Show the frames
            frame = cv.imencode(".png", frame)[1].tobytes()
            window['Frames'].update(data=frame)
    finally:
        window.close()
        realSensePipeline.stop()
        logger('Framework finished!')

# Run the program
main()