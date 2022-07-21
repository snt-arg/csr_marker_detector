import rospy
import cv2 as cv
from sensor_msgs.msg import Image
# CvBridge: a ROS library that provides an interface between ROS and OpenCV
from cv_bridge import CvBridge, CvBridgeError

# Parameters
cameraPort = 0
topicName = '/webcam'

def main():
    # Converting ROS image messages to OpenCV images
    bridge = CvBridge()
    cap = cv.VideoCapture(cameraPort)
    print(f'Capture Status:', cap.isOpened())
    if not cap.isOpened():
        print('Cannot open camera!')
    # Main loop
    try:
        # Topic
        publisher = rospy.Publisher(topicName, Image, queue_size=1)
        # Node
        rospy.init_node('imageAlex', anonymous=False)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            ret, frame = cap.read()
            if not ret:
                break
            # Possible encodings: mono8, mono16, rgb8, bgra8, and rgba8
            # message = bridge.imgmsg_to_cv2(frame, desired_encoding='passthrough')
            message = bridge.cv2_to_imgmsg(frame, 'bgr8')
            publisher.publish(message)
            # 
            if cv.waitKey(1) == ord('q'):
                break
            if rospy.is_shutdown():
                cap.release()
    except rospy.ROSInterruptException:
        print(f'Error in ROS')
        pass

# Run the program
main()