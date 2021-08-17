import os
import cv2
import numpy as np


def mkdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def create_center_rectangle(dimensions, size):
    width, height = dimensions
    x, y = size
    return [
        (int((width / 2) - x), int((height / 2) - y)),
        (int((width / 2) + x), int((height / 2) + y)),
    ]


def get_dominant_color(image):
    data = np.reshape(image, (-1, 3))
    data = np.float32(data)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, _, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)
    dominant_color = centers[0].astype(np.int32)
    return tuple([int(c) for c in dominant_color])


def write_img_to_dir(image, dirname, filename):
    mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, filename), image)
