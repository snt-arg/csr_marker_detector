cameraLeftFrames = 'E:\Datasets\Dataset 23 - CSR\Sample6\image_left'
cameraRightFrames = 'E:\Datasets\Dataset 23 - CSR\Sample6\image_right'

# Shown window
windowWidth = 1500
# Values for the left and the right camera
brightness = {'lefCam': 0, 'rightCam': 0}

# Image Alignment
flipImage = False  # Flip one of the input camera's frame
maxFeatures = 500
goodMatchPercentage = 0.4
circlularMaskCoverage = 0.8  # Value between 0 and 1

# Post-Processing
threshold = 10  # Value between 0 and 255
erodeKernelSize = (9, 9)
gaussianBlurKernelSize = (5, 5)
