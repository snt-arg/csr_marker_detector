import logging
import cv2 as cv
import numpy as np
import PySimpleGUI as sg
import pyrealsense2 as rs
from utils.logger import logger
from vision.addLabel import addLabel
from vision.processFrames import processFrames
from config import ports, fpsBoost, brightness, labelSize, sliderSize
from config import threshold, erodeKernelSize, gaussianBlurKernelSize
from config import maxFeatures, goodMatchPercentage, circlularMaskCoverage

def fpsGetter(newFps):
    return newFps

# Definitions
fps = fpsGetter(0)
windowTitle = 'CSR Readout Software'
tabGeneral = [[sg.Text('Frame-rate:', size=labelSize), sg.Text(str(fps) + f' fps {"(boosted)" if fpsBoost else "(normal)"}')],
    [sg.Text("Camera brightness/contrast:", size=labelSize), sg.Slider((1.0, 3.0), brightness['alpha'], .1, orientation="h", size=(50, 15), key="camAlpha"),
    sg.Slider((0, 50), brightness['beta'], 1, orientation="h", size=(50, 15), key="camBeta")]]
tabAlignment = [
    [sg.Text('Max. features:', size=labelSize), sg.Slider((10, 1000), maxFeatures, 10, orientation="h", size=sliderSize, key="MaxFeat")],
    [sg.Text('Matching rate:', size=labelSize), sg.Slider((0, 1), goodMatchPercentage, .1, orientation="h", size=sliderSize, key="MatchRate")],
    [sg.Text('Circular mask:', size=labelSize), sg.Slider((0, 1), circlularMaskCoverage, .01, orientation="h", size=sliderSize, key="CircMask")]]
tabPosProcessing = [
    [sg.Text('Threshold:', size=labelSize), sg.Slider((1, 255), threshold, 1, orientation="h", size=sliderSize, key="Threshold")],
    [sg.Text('Erosion kernel:', size=labelSize), sg.Slider((1, 50), erodeKernelSize, 1, orientation="h", size=sliderSize, key="Erosion")],
    [sg.Text('Gaussian kernel:', size=labelSize), sg.Slider((1, 49), gaussianBlurKernelSize, 2, orientation="h", size=sliderSize, key="Gaussian")]]
tabMarkerDetection = [
    [sg.Text('Threshold:', size=labelSize), sg.Slider((1, 255), threshold, 1, orientation="h", size=sliderSize, key="Threshold")],
    [sg.Text('Erosion kernel:', size=labelSize), sg.Slider((1, 50), erodeKernelSize, 1, orientation="h", size=sliderSize, key="Erosion")],
    [sg.Text('Gaussian kernel:', size=labelSize), sg.Slider((1, 49), gaussianBlurKernelSize, 2, orientation="h", size=sliderSize, key="Gaussian")]]
tabGroup = [[sg.Image(filename="./logo.png",  key="LogoHolder"), sg.TabGroup([[sg.Tab('General Settings', tabGeneral), sg.Tab('Alignment Configurations', tabAlignment),
                    sg.Tab('Post-Processing', tabPosProcessing), sg.Tab('Marker Detection', tabMarkerDetection)]], tab_location='centertop', expand_x=True,
                       title_color='dark slate grey', selected_background_color='dark orange', pad=10)]]
imageViewer = [sg.Image(filename="", key="Frames")]

def main():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started! (RealSense version)')
    # Create the window
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
                        'erosionKernel': values['Erosion'], 'gaussianKernel': values['Gaussian']}
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