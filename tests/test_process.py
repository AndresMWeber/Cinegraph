from pathlib import Path
import pytest
import numpy as np
import cinegraph.process as cgp
from cinegraph.utils import Config
from .file_paths import SAMPLE_VIDEO_MP4, SAMPLE_VIDEO_AVI, SAMPLE_VIDEO_EMPTY_MP4, here


class TestProcessVideo:
    def test_file_exists_mp4(self):
        video = cgp.process_video(SAMPLE_VIDEO_MP4)
        assert video.size

    def test_file_exists_avi(self):
        video = cgp.process_video(SAMPLE_VIDEO_AVI)
        assert video.size

    def test_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            cgp.process_video("this/is/not/a/file.mp4")

    def test_file_empty(self):
        with pytest.raises(ZeroDivisionError):
            cgp.process_video(SAMPLE_VIDEO_EMPTY_MP4)


class TestWriteVideoSnap:
    original_output_dir = Config.output_dir

    def setup_class(self):
        Config.art_frame = True
        Config.output_dir = str(here.absolute())

    def teardown_class(self):
        Config.art_frame = False
        Config.output_dir = self.original_output_dir
        Path(here / "sample-black/f_10.jpg").unlink()
        Path(here / "sample-black").rmdir()

    def test_black_image(self):
        sample_black_image = np.zeros((10, 10, 1), dtype="uint8")
        cgp.write_video_snap(sample_black_image, 10, (255, 255, 255), "sample-black.mp4")
