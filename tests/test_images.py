import numpy as np
from pathlib import Path
from .file_paths import SAMPLE_VIDEO_MP4
from cinegraph.images import (
    Video,
    write_img_to_dir,
    place_image_in_center,
    center_rectangle_bounding_box,
    draw_center_box,
    get_dominant_color,
)

here = Path(__file__).parent


class TestClassVideo:
    def test_init(self):
        Video(SAMPLE_VIDEO_MP4)

    def test_set_desired_frames(self):
        assert Video(SAMPLE_VIDEO_MP4).set_desired_frames(5).frame_step == 5

    def test_get_frame(self):
        assert len(Video(SAMPLE_VIDEO_MP4).get_frame(10))

    def test_release(self):
        vid = Video(SAMPLE_VIDEO_MP4)
        vid.release()
        assert not vid.vidcap.isOpened()

    def test_len(self):
        assert len(Video(SAMPLE_VIDEO_MP4)) == 23


class TestWriteImgToDir:
    def test_placeholder(self):
        write_img_to_dir


class TestPlaceImageInCenter:
    def test_placeholder(self):
        place_image_in_center


class TestCenterRectangleBoundingBox:
    def test_placeholder(self):
        center_rectangle_bounding_box


class TestDrawCenterBox:
    def test_placeholder(self):
        draw_center_box


class TestGetDominantColor:
    def test_placeholder(self):
        get_dominant_color
