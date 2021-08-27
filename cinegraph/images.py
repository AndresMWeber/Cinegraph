import os
from pathlib import Path
import numpy as np
import cv2
from cinegraph.utils import Config


class Video:
    def __init__(self, file_path, number_of_frames=Config.num_colors):
        self.vidcap = cv2.VideoCapture(file_path)
        self.set_desired_frames(number_of_frames)

    def set_desired_frames(self, number_of_frames):
        self.frame_step = int(len(self) / number_of_frames) + 1
        return self

    def get_frame(self, frame):
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        return image if success else []

    def release(self):
        self.vidcap.release()

    def __len__(self):
        return int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))


def write_img_to_dir(image, dirname, filename):
    Path(dirname).mkdir(parents=True, exist_ok=True)
    path = os.path.normpath(os.path.join(dirname, filename))
    cv2.imwrite(path, image)
    return path


def place_image_in_center(background, foreground):
    bg_h, bg_w, _ = background.shape
    fg_h, fg_w, _ = foreground.shape
    yoff = round((bg_h - fg_h) / 2)
    xoff = round((bg_w - fg_w) / 2)
    result = background.copy()
    result[yoff : yoff + fg_h, xoff : xoff + fg_w] = foreground
    return result


def center_rectangle_bounding_box(dimensions, size):
    width, height = dimensions
    x, y = size
    return [
        (int((width / 2) - x), int((height / 2) - y)),
        (int((width / 2) + x), int((height / 2) + y)),
    ]


def draw_center_box(image, color, size):
    height, width, _ = image.shape
    inner_start, inner_end = center_rectangle_bounding_box((width, height), (size, size))
    cv2.rectangle(
        image,
        inner_start,
        inner_end,
        color,
        thickness=-1,
    )


def get_dominant_color(image):
    data = np.reshape(image, (-1, 3))
    data = np.float32(data)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, _, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)
    dominant_color = centers[0].astype(np.int32)
    return tuple([int(c) for c in dominant_color])
