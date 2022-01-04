import cv2 as cv
from config import windowWidth


def frameResize(image, width=200):
    """
    Resizes an image to a given width, while maintaining the aspect ratio.

    Parameters
    ----------
    image: numpy.ndarray
        Image to resize.
    width: int
        Width to resize the image to.

    Returns
    -------
    scaledImage: numpy.ndarray
        Resized image.
    """
    # Calculating frame dimensions
    frameHeight, frameWidth = image.shape[:2]
    aspectRatio = frameWidth / frameHeight
    # Scale the frame's width, while keeping its aspect ratio
    scaledImage = cv.resize(
        image, (width, int(width / aspectRatio)), interpolation=cv.INTER_AREA)
    return scaledImage


def imageConcatHorizontal(imageList):
    """
    Concatenates a list of images horizontally.

    Parameters
    ----------
    imageList: list
        List of images to concatenate.
    """
    numberOfImages = len(imageList)

    # Resizing the images
    resizedImageList = [frameResize(
        img, int(windowWidth / numberOfImages)) for img in imageList]

    # Returning the final image
    return cv.hconcat(resizedImageList)
