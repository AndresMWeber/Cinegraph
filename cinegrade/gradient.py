from cinegrade.utils import create_center_rectangle
from typing import List, Tuple
import numpy as np
import cv2


def create_matting(colors: List, dimensions: Tuple):
    width, height = dimensions
    background = np.full((width, height, 3), 255, dtype=np.float32)
    gradient = create_gradient(colors, (round(width / 3), round(height * 0.8)))
    border_start, border_end = create_center_rectangle(
        dimensions, (round((width * 0.40) / 2), round((height * 0.85) / 2))
    )
    cv2.rectangle(
        background,
        tuple(reversed(border_start)),
        tuple(reversed(border_end)),
        (0, 0, 0),
        2,
    )
    result = place_image_in_center(background, gradient)
    return result


def place_image_in_center(background, foreground):
    bg_h, bg_w, _ = background.shape
    fg_h, fg_w, _ = foreground.shape
    yoff = round((bg_h - fg_h) / 2)
    xoff = round((bg_w - fg_w) / 2)
    result = background.copy()
    result[yoff : yoff + fg_h, xoff : xoff + fg_w] = foreground
    return result


def create_gradient(colors: List, dimensions: Tuple):
    width, height = dimensions
    gradient = np.zeros((width, height, 3), np.uint8)

    x = 0
    w = height / len(colors)

    for color in colors:
        cv2.rectangle(gradient, (np.int32(x), 0), (np.int32(x + w), height), color, -1)
        x += w
    return cv2.GaussianBlur(gradient, (5, 1), 0, cv2.BORDER_TRANSPARENT)
