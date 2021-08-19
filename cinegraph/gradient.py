import cv2
import numpy as np
from typing import List, Tuple
from cinegraph.images import center_rectangle_bounding_box, place_image_in_center
from cinegraph.utils import Config


def create_cinegraph(colors: List):
    if Config.art_frame:
        return create_matting(colors)
    else:
        return create_gradient(colors, Config.resolution)


def create_matting(colors: List):
    width, height = Config.resolution
    background = np.full((height, width, 3), Config.bg_color, dtype=np.float32)
    gradient_x = round(width * 0.8)
    gradient_y = round(height / 3)
    border_dimensions = (
        round((gradient_x + Config.art_frame_margin) / 2),
        round((gradient_y + Config.art_frame_margin) / 2),
    )
    gradient = create_gradient(colors, (gradient_x, gradient_y))
    border_start, border_end = center_rectangle_bounding_box(Config.resolution, border_dimensions)
    cv2.rectangle(
        background,
        border_start,
        border_end,
        (0, 0, 0),
        Config.border_width,
    )
    result = place_image_in_center(background, gradient)
    return result


def create_gradient(colors: List, dimensions: Tuple):
    width, height = dimensions
    gradient = np.zeros((height, width, 3), np.uint8)

    x = 0
    w = width / len(colors)

    for color in colors:
        cv2.rectangle(gradient, (np.int32(x), 0), (np.int32(x + w), height), color, -1)
        x += w

    if not Config.blur_x or not Config.blur_y:
        return gradient
    return cv2.GaussianBlur(gradient, (Config.blur_x, Config.blur_y), 0, cv2.BORDER_TRANSPARENT)
