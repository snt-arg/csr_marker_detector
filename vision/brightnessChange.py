import cv2 as cv


def brighnessChange(image, value=40):
    """
    Change the brightness of the given image.

    Parameters:
    -----------
    image: numpy.ndarray
        Image to be changed
    value: int
        Value to be added to the brightness

    Returns:
    --------
    processedImage: numpy.ndarray
        Image with changed brightness
    """
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    processedImage = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)

    return processedImage
