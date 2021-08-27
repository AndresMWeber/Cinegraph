from pathlib import Path

here = Path(__file__).parent
SAMPLE_VIDEO_MP4 = str((here / "fixtures/sample-1s.mp4").absolute())
SAMPLE_VIDEO_AVI = str((here / "fixtures/sample-1s.avi").absolute())
SAMPLE_VIDEO_EMPTY_MP4 = str((here / "fixtures/sample-empty.mp4").absolute())
