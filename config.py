# GUI settings
fpsBoost = True
labelSize = (20,1)
inputSize = (30,1)
sliderSize = (100, 15)

# Shown window
windowWidth = 1800
# Camera ports (0 for internal webcam)
ports = {'lCam': 4, 'rCam': 2}
# Values for the left and the right camera
brightness = {'alpha': 1.0, 'beta': 0}

# Image alignment
maxFeatures = 500
goodMatchPercentage = 0.4
circlularMaskCoverage = 0.8  # Value between 0 and 1

# Post-processing initialize values
threshold = 10  # Value between 0 and 255
erodeKernelSize = 9  # Value between 1 and 50
gaussianBlurKernelSize = 5  # Only odd values

# Marker detection initialize values
markerId = 0
markerSize = 250
markerDictType = 'DICT_ARUCO_ORIGINAL'
defaultGenPath = './markers/generated/'
