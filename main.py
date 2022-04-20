import logging
import cv2 as cv
import PySimpleGUI as sg
from utils.logger import logger
from vision.processFrames import processFrames
from vision.brightnessChange import brighnessChange
from config import ports, brightness, labelSize, sliderSize
from config import threshold, erodeKernelSize, gaussianBlurKernelSize
from config import maxFeatures, goodMatchPercentage, circlularMaskCoverage

# Definitions
windowTitle = 'CSR Readout Software'
tabGeneral = [[sg.Text('Frame Count:', size=labelSize), sg.Text('N/A')]]
tabAlignment = [
    [sg.Text('Max. features:', size=labelSize), sg.Slider((10, 1000), maxFeatures, 10, orientation="h", size=sliderSize, key="MaxFeat")],
    [sg.Text('Matching rate:', size=labelSize), sg.Slider((0, 1), goodMatchPercentage, .1, orientation="h", size=sliderSize, key="MatchRate")],
    [sg.Text('Circular mask:', size=labelSize), sg.Slider((0, 1), circlularMaskCoverage, .01, orientation="h", size=sliderSize, key="CircMask")]]
tabPosProcessing = [
    [sg.Text('Threshold:', size=labelSize), sg.Slider((1, 255), threshold, 1, orientation="h", size=sliderSize, key="Threshold")],
    [sg.Text('Erosion kernel:', size=labelSize), sg.Slider((1, 50), erodeKernelSize, 1, orientation="h", size=sliderSize, key="Erosion")],
    [sg.Text('Gaussian kernel:', size=labelSize), sg.Slider((1, 49), gaussianBlurKernelSize, 2, orientation="h", size=sliderSize, key="Gaussian")]]
tabGroup = [[sg.Image(filename="./logo.png",  key="LogoHolder"), sg.TabGroup([[sg.Tab('General Settings', tabGeneral), sg.Tab('Alignment Configurations', tabAlignment),
                    sg.Tab('Post-Processing', tabPosProcessing)]], tab_location='centertop', expand_x=True,
                       title_color='dark slate grey', selected_background_color='dark orange', pad=10)]]
imageViewer = [sg.Image(filename="", key="Frames")]

def main():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Framework started!')
    # Create the window
    window = sg.Window(windowTitle, [tabGroup, imageViewer], location=(800, 400))
    capL, capR = cv.VideoCapture(ports['lCam']), cv.VideoCapture(ports['rCam'])

    # Create an event loop
    while True:
        event, values = window.read(timeout=10)
        # End program if user closes window
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Retrieve frames
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        # Change brightness
        frameL = brighnessChange(frameL, brightness['lCam'])
        frameR = brighnessChange(frameR, brightness['rCam'])
        # If frame is read correctly ret is True
        if not retR or not retL:
            logger("Error while reading frames!", 'error')
            break
        # Flipping one of the frames
        frameR = cv.flip(frameR, 1)
        # Get the values from the GUI
        guiValues = {'maxFeatures': values['MaxFeat'], 'goodMatchPercentage': values['MatchRate'],
                    'circlularMaskCoverage': values['CircMask'], 'threshold': values['Threshold'], 
                    'erosionKernel': values['Erosion'], 'gaussianKernel': values['Gaussian']}
        # Process frames
        frame = processFrames(frameL, frameR, guiValues)
        # Show the frames
        frame = cv.imencode(".png", frame)[1].tobytes()
        window['Frames'].update(data=frame)
    
    capL.release()
    capR.release()
    window.close()
    logger('Framework finished!')

# Run the program
main()