# Simple Stereo Image Alignment

This repository provides a simple tool that requires some basic configurations to ensure perfect image alignment on the images taken by a color stereo-vision camera. The main goal is to keep only the frame differences and remove other matched sections. In this regard, the frames acquired by one of the cameras are horizontally flipped (if needed), and then keypoints and descriptors are extracted using the [Oriented FAST and Rotated BRIEF (ORB)](https://docs.opencv.org/4.x/d1/d89/tutorial_py_orb.html "Oriented FAST and Rotated BRIEF (ORB)") algorithm. A [homography matrix](https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html "homography matrix") is found using the matching data, and the registered version of the input image is created to match the other image perfectly.

### ⚙️ Conditions

- Images obtained from two cameras are the same size.
- Illumination conditions are not severe.
- The vertical and horizontal displacements are fixed.

### 🚀 Env. and Libraries

You will need below libraries to be installed before running the application:

- Python > 3.7
- OpenCV > 3.4
- Numpy > 1.19

You can simply run the below command in the root directory:

```python
pip install -r requirements.txt
```

### 🗹 TODOs

- Improve image denoising
- Provide B&W output
- Adding a ROI to clear unused parts
- [Optional] Enable processing videos as input
- [Optional] Draw bounding-boxes on the detected item
