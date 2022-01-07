cameraLeftFrames = 'E:\Datasets\Dataset 23 - CSR\Sample2\image_left'
cameraRightFrames = 'E:\Datasets\Dataset 23 - CSR\Sample2\image_right'

# Shown window
windowWidth = 1500

# Image Alignment
flipImage = False  # Flip one of the input camera's frame
maxFeatures = 500
goodMatchPercentage = 0.4
circlularMaskCoverage = 0.8  # Value between 0 and 1

# Post-Processing
threshold = 10  # Value between 0 and 255
erodeKernelSize = (9, 9)
gaussianBlurKernelSize = (5, 5)
