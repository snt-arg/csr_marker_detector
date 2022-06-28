import logging
import cv2 as cv
import PySimpleGUI as sg
from utils.logger import logger
from vision.addLabel import addLabel
from vision.processFrames import processFrames
from markers.arUcoUtils import arUcoDictionary
from markers.arUcoGenerator import markerGenerator
from config import threshold, erodeKernelSize, gaussianBlurKernelSize
from config import ports, fpsBoost, brightness, labelSize, sliderSize
from config import markerId, markerSize, markerDictType, defaultGenPath
from config import maxFeatures, goodMatchPercentage, circlularMaskCoverage, flipImage, enableCircularROI

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
    [sg.Text('Circular mask:', size=labelSize), sg.Slider((0, 1), circlularMaskCoverage, .01, orientation="h", size=sliderSize, key="CircMask"),
    sg.Checkbox('Enable Circular Mask', default=enableCircularROI, key="CircMaskEnable")]]
tabPosProcessing = [
    [sg.Text('Threshold:', size=labelSize), sg.Slider((1, 255), threshold, 1, orientation="h", size=sliderSize, key="Threshold")],
    [sg.Text('Erosion kernel:', size=labelSize), sg.Slider((1, 50), erodeKernelSize, 1, orientation="h", size=sliderSize, key="Erosion")],
    [sg.Text('Gaussian kernel:', size=labelSize), sg.Slider((1, 49), gaussianBlurKernelSize, 2, orientation="h", size=sliderSize, key="Gaussian")]]
tabMarkerDetection = [
    [sg.Text('Marker Dictionary:', size=labelSize), sg.Combo(list(arUcoDictionary.keys()), default_value=str(markerDictType), key="MarkerDict")],
    [sg.Text(f'Generate Marker (will be saved in "{defaultGenPath}"):', size=(labelSize[0]*10,labelSize[1]))],
    [sg.Text('Marker-ID:', size=labelSize), sg.Slider((1, 100), markerId, 1, orientation="h", size=(sliderSize[0]/2,sliderSize[1]), key="MarkerId"),
    sg.Text('Marker Size:', size=labelSize), sg.Combo([markerSize, markerSize*2, markerSize*4], default_value=str(markerSize), key="MarkerSize"), sg.Button('Generate')]]
tabGroup = [[sg.Image(filename="./logo.png",  key="LogoHolder"), sg.TabGroup([[sg.Tab('General Settings', tabGeneral), sg.Tab('Alignment Configurations', tabAlignment),
                    sg.Tab('Post-Processing', tabPosProcessing), sg.Tab('Marker Detection', tabMarkerDetection)]], tab_location='centertop', expand_x=True,
                       title_color='dark slate grey', selected_background_color='dark orange', pad=10)]]
imageViewer = [sg.Image(filename="", key="Frames")]

def main():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Create the window
    window = sg.Window(windowTitle, [tabGroup, imageViewer], location=(800, 400))
    capL, capR = cv.VideoCapture(ports['lCam']), cv.VideoCapture(ports['rCam'])

    # Get the frame-rate of the cameras
    if fpsBoost:
        capL.set(cv.CAP_PROP_FPS, 30.0)
        capR.set(cv.CAP_PROP_FPS, 30.0)
    fpsGetter(capL.get(cv.CAP_PROP_FPS))

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