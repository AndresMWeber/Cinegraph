import cv2
import os
from cinegrade.gradient import create_matting
from cinegrade.utils import (
    create_center_rectangle,
    get_dominant_color,
    write_img_to_dir,
)


class Video:
    def __init__(self, file_path, number_of_frames):
        self.vidcap = cv2.VideoCapture(file_path)
        self.set_desired_frames(number_of_frames)

    def set_desired_frames(self, number_of_frames):
        self.frame_step = int(len(self) / number_of_frames) + 1

    def get_frame(self, frame):
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        return image if success else []

    def __len__(self):
        return int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))


def draw_center_box(image, color, size):
    height, width, _ = image.shape
    inner_start, inner_end = create_center_rectangle((width, height), (size, size))
    cv2.rectangle(
        image,
        inner_start,
        inner_end,
        color,
        thickness=-1,
    )


def write_video_snap(image, frame_number, dominant_color):
    draw_center_box(image, dominant_color, 64)
    write_img_to_dir(image, "output", f"frame_{frame_number}.jpg")


def process_video(video_file_path, number_of_colors=100):
    video = Video(video_file_path, number_of_colors)

    colors = []
    for frame_number in range(0, len(video), video.frame_step):
        image = video.get_frame(frame_number)
        if len(image):
            dominant_color = get_dominant_color(image)
            colors.append(dominant_color)
            # write_video_snap(image, frame_number, dominant_color)

    gradient = create_matting(colors, (1080, 1920))
    write_img_to_dir(
        gradient,
        "gradient",
        f"{os.path.basename(video_file_path).split('.')[0]}_gradient.jpg",
    )
