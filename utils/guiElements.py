import PySimpleGUI as sg
from markers.arUcoUtils import arUcoDictionary
from config import fpsBoost, brightness, labelSize, sliderSize
from config import threshold, erodeKernelSize, gaussianBlurKernelSize
from config import markerId, markerSize, markerDictType, defaultGenPath
from config import maxFeatures, goodMatchPercentage, circlularMaskCoverage, enableCircularROI

def guiElements():
    # Definitions of GUI elements
    windowTitle = 'CSR Readout Software'
    tabGeneral = [[sg.Text('Frame-rate:', size=labelSize), sg.Text('-' + f' fps {"(boosted)" if fpsBoost else "(normal)"}')],
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
    # Return to GUI creator
    return windowTitle, tabGroup, imageViewer