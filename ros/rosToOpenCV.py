import cv2 as cv
# CvBridge: a ROS library that provides an interface between ROS and OpenCV
from cv_bridge import CvBridge

def main():
    # Converting ROS image messages to OpenCV images
    bridge = CvBridge()
    # Possible encodings: mono8, mono16, rgb8, bgra8, and rgba8
    # cv_image = bridge.imgmsg_to_cv2(image_message, desired_encoding='passthrough')
    cap = cv.VideoCapture(0)
    print(f'Capture Status:', cap.isOpened())
    if not cap.isOpened():
        print('Cannot open camera!')
    # Main loop
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv.imshow('Frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


# Run the program
main()