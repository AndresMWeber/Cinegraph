import fire
import pytest
from cinegraph.cli import generate, create_filename
from .file_paths import SAMPLE_VIDEO_MP4


@pytest.mark.run(order=2)
class TestCli:
    def test_generate(self, capsys):
        fire.Fire(generate, [SAMPLE_VIDEO_MP4])
        captured = capsys.readouterr()
        result = captured.out
        assert "Processing file" in result

    def test_generate_no_files(self, capsys):
        fire.Fire(generate, [])
        captured = capsys.readouterr()
        result = captured.out
        assert "No files" in result


def test_create_filename():
    assert create_filename(SAMPLE_VIDEO_MP4) == "sample-1s_c600_b5_r1920x1080_f0_fm50.jpg"
