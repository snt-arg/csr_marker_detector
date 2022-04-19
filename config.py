cameraLeftFrames = '/home/ali/Datasets/Sample4/image_left'
cameraRightFrames = '/home/ali/Datasets/Sample4/image_right'

# Shown window
windowWidth = 1500
# Values for the left and the right camera
brightness = {'lefCam': 0, 'rightCam': 0}

# Image Alignment
flipImage = False  # Flip one of the input camera's frame
maxFeatures = 500
goodMatchPercentage = 0.4
circlularMaskCoverage = 0.8  # Value between 0 and 1

# Post-Processing initialize values
threshold = 10  # Value between 0 and 255
erodeKernelSize = 9  # Value between 1 and 50
gaussianBlurKernelSize = 5  # Only odd values
