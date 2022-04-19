import PySimpleGUI as sg
from config import threshold, erodeKernelSize, gaussianBlurKernelSize
from config import maxFeatures, goodMatchPercentage, circlularMaskCoverage

# Definitions
windowTitle = 'CSR Readout'
tabGeneral = [[sg.Text('Frame Count:', size=(20,1)), sg.Text('N/A')]]
tabAlignment = [
    [sg.Text('Flip image?', size=(20,1)),
        sg.Radio('Already flipped.', "RadFlip", default=True, key="FlipYes"),
        sg.Radio('Needs flipping', "RadFlip", default=False, key="FlipNo")],
    [sg.Text('Max. features:', size=(20,1)), sg.Slider((10, 1000), maxFeatures, 10, orientation="h", size=(35, 15), key="MaxFeat")],
    [sg.Text('Matching rate:', size=(20,1)), sg.Slider((0, 1), goodMatchPercentage, .1, orientation="h", size=(35, 15), key="MatchRate")],
    [sg.Text('Circular mask:', size=(20,1)), sg.Slider((0, 1), circlularMaskCoverage, .01, orientation="h", size=(35, 15), key="CircMask")]]
tabPosProcessing = [
    [sg.Text('Threshold:', size=(20,1)), sg.Slider((1, 255), threshold, 1, orientation="h", size=(35, 15), key="Threshold")],
    [sg.Text('Erosion kernel:', size=(20,1)), sg.Slider((1, 50), erodeKernelSize, 1, orientation="h", size=(35, 15), key="Erosion")],
    [sg.Text('Gaussian kernel:', size=(20,1)), sg.Slider((1, 49), gaussianBlurKernelSize, 2, orientation="h", size=(35, 15), key="Gaussian")]]
tabgrp = [[sg.TabGroup([[sg.Tab('General Settings', tabGeneral), sg.Tab('Alignment Configurations', tabAlignment),
                    sg.Tab('Post-Processing', tabPosProcessing)]], tab_location='centertop',
                       title_color='dark slate grey', selected_background_color='dark orange', border_width=5)]]
layout = [tabgrp]

def gui():
    # Create the window
    window = sg.Window(windowTitle, layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

    window.close()