import cv2
import numpy as np

def getLaneCurve(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(
        blur,
        120,
        255,
        cv2.THRESH_BINARY_INV
    )

    histogram = np.sum(thresh, axis=0)

    if np.max(histogram) < 1000:
        return 0  # no lanes detected, go straight

    midpoint = histogram.shape[0] // 2
    left   = np.argmax(histogram[:midpoint])
    right  = np.argmax(histogram[midpoint:]) + midpoint
    center = (left + right) // 2
    curve  = center - midpoint

    cv2.line(
        img,
        (center, 0),
        (center, img.shape[0]),
        (0, 255, 0),
        3
    )

    return curve
