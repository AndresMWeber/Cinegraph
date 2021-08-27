import pytest
from cinegraph.utils import Config, chunk_list, SIZE_UNIT, convert_unit, get_filename


class TestConfig:
    @pytest.mark.run(order=1)
    def test_defaults(self):
        assert Config.resolution == (1920, 1080)
        assert Config.output_dir == "output"
        assert Config.num_colors == 600
        assert Config.blur_x == 5 and Config.blur_y == 5
        assert Config.bg_color == 255
        assert Config.border_width == 1
        assert not Config.write_frames
        assert Config.art_frame
        assert Config.art_frame_margin == 10
        assert Config.box_size == 64
        assert Config.chunk_size == 10


class TestChunkList:
    def test_range_10(self):
        assert len(list(chunk_list(range(10), 2))) == 5

    def test_empty(self):
        assert list(chunk_list([], 2)) == []

    def test_one_overlength_chunk(self):
        assert list(chunk_list([1], 3)) == [[1]]

    def test_one_samesize_chunk(self):
        assert list(chunk_list([1], 1)) == [[1]]


class TestConvertUnit:
    def test_kb(self):
        assert pytest.approx(convert_unit(1000, SIZE_UNIT.KB), 1)

    def test_mb(self):
        assert pytest.approx(convert_unit(1000, SIZE_UNIT.MB), 0.001)

    def test_gb(self):
        assert pytest.approx(convert_unit(1000, SIZE_UNIT.GB), 0.000001)

    def test_kb(self):
        assert convert_unit(1000, 5) == 1000


class TestGetFilename:
    def test_relative(self):
        assert get_filename(r"dir1/filename.ext") == "filename"

    def test_full_windows(self):
        assert get_filename(r"C:/dir1/filename.ext") == "filename"

    def test_full_nix(self):
        assert get_filename(r"/root/dir1/filename.ext") == "filename"

    def test_no_extension(self):
        assert get_filename(r"/root/dir1/filename") == "filename"

    def test_no_filename(self):
        assert get_filename(r"/root/dir1/") == ""
