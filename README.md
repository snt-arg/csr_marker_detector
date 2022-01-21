# CSR-FM Detector

This repository provides a simple tool to detect fiducial markers in a stereo-vision camera. It requires some configurations to ensure perfect image alignment applied to the images taken by the camera. The main goal is to keep only the frame differences and remove other matched sections. In this regard, the frames acquired by one of the cameras are horizontally flipped (if needed). Then keypoints and descriptors are extracted using the [Oriented FAST and Rotated BRIEF (ORB)](https://docs.opencv.org/4.x/d1/d89/tutorial_py_orb.html "Oriented FAST and Rotated BRIEF (ORB)") algorithm. A [homography matrix](https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html "homography matrix") is found using the matching data, and the registered version of the input image is created to match the other image perfectly. The following step is to apply some post-processing stuff to ensure the output contains only the unmatched section of the frames.

### ⚙️ Conditions

- Images obtained from two cameras have the same size.
- Illumination conditions are not severe.
- The vertical and horizontal displacements are fixed.

### 🚀 Libraries

You will need below libraries to be installed before running the application:

- Python > 3.7
- OpenCV > 3.4
- Numpy > 1.19

You can also run the command below in the root directory to get all of them installed:

```python
pip install -r requirements.txt
```

### 🗹 TODOs

- Improve image alignment in case no matches are found
- Improve post-processing module
- Resolve the intense changes issue when there is no keypoints
- [Optional] Draw bounding-boxes on the detected item
