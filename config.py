cameraLeftFrames = 'E:\Datasets\Dataset 23 - CSR\Sample1\image_left'
cameraRightFrames = 'E:\Datasets\Dataset 23 - CSR\Sample1\image_right'

# Shown window
windowWidth = 1500

# Image Alignment
flipImage = True  # Flip one of the input camera's frame
maxFeatures = 500
goodMatchPercentage = 0.4
roiCoverage = (0.5, 1)  # Percentage of the frame to be used as ROI (h, w)

# Post-Processing
threshold = 10  # Value between 0 and 255
erodeKernelSize = (9, 9)
gaussianBlurKernelSize = (5, 5)
