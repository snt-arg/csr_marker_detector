import cv2 as cv
from utils.arUcoUtils import arUcoDictionary

def arUcoMarkerDetector(imageAddress, dictType='DICT_ARUCO_ORIGINAL'):
    try:
        # Read the image
        image = cv.imread(imageAddress)
        cv.imshow('fileName', image)
        # Selecting the dictionary type
        selectedDict = cv.aruco.Dictionary_get(arUcoDictionary[dictType])
        arucoParams = cv.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv.aruco.detectMarkers(image, selectedDict,	parameters=arucoParams)
        # Return the detected markers
        # print(corners, ids, rejected)
        return (corners, ids, rejected)
        # draw the bounding box of the ArUCo detection
		# cv.line(image, topLeft, topRight, (0, 255, 0), 2)
		# cv.line(image, topRight, bottomRight, (0, 255, 0), 2)
		# cv.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
		# cv.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
		# # compute and draw the center (x, y)-coordinates of the ArUco
		# # marker
		# cX = int((topLeft[0] + bottomRight[0]) / 2.0)
		# cY = int((topLeft[1] + bottomRight[1]) / 2.0)
		# cv.circle(image, (cX, cY), 4, (0, 0, 255), -1)
		# # draw the ArUco marker ID on the image
		# cv.putText(image, str(markerID),
		# 	(topLeft[0], topLeft[1] - 15), cv.FONT_HERSHEY_SIMPLEX,
		# 	0.5, (0, 255, 0), 2)
		# print("[INFO] ArUco marker ID: {}".format(markerID))
		# # show the output image
		# cv.imshow("Image", image)
		# cv.waitKey(0)
    except Exception as exception:
        print(f'Error occurred when detecting the arUco marker!\n{exception}', 'error')

arUcoMarkerDetector('ArUco#DICT_ARUCO_ORIGINAL#00010.png', 'DICT_ARUCO_ORIGINAL')

# https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/