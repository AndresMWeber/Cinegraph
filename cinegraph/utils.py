import enum
import os
from typing import Tuple, cast


class Config:
    output_dir = "output"
    resolution = (1920, 1080)
    num_colors = 600
    blur_x = 5
    blur_y = 5
    bg_color = 255
    border_width = 1
    write_frames = False
    art_frame = True
    art_frame_margin = 10
    box_size = 64
    chunk_size = 10


def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_filesize(size_in_bytes, unit):
    """Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def get_filename(file_path):
    filename, _ = os.path.splitext(os.path.basename(file_path))
    return filename


class PrintSize:
    """ https://pixelcalculator.com/en
    ISO A Series Poster Sizes
    2A0	1189 x 1682 mm	46.8 x 66.2 in
    A0	841 x 1189 mm	33.1 x 46.8 in
    A1	594 x 841 mm	23.4 x 33.1 in
    A2	420 x 594 mm	16.5 x 23.4 in
    A3	297 x 420 mm	11.7 x 16.5 in
    A4	210 x 297 mm	8.3 x 11.7 in

    Poster Sizes
    Letter	215.9 x 279.4 mm	8.5 x 11 in
    Small	279.4 x 431.8 mm	11 x 17 in
    Medium	457.2 x 609.6 mm	18 x 24 in
    Large	609.6 x 914.4 mm	24 x 36 in
    """

    sizes = {
        "A0": (841, 1188),
        "A1": (594, 841),
        "A2": (420, 594),
        "A3": (297, 420),
        "A4": (210, 297),
        "A5": (148, 210),
        "A6": (105, 148),
        "A7": (74, 105),
        "A8": (52, 74),
        "LETTER": (215.9, 279.4),
        "SMALL": (279.4, 431.8),
        "MEDIUM": (457.2, 609.6),
        "LARGE": (609.6, 914.4),
    }  # in mm

    def __init__(self, resolution: tuple) -> None:
        assert len(resolution) == 2
        shape = cast(Tuple[int, int], resolution)
        self.x, self.y = shape

    @property
    def resolution(self):
        return (self.x, self.y)

    @staticmethod
    def pixels_to_dpi(pixel: int, dimension: float) -> float:
        # dpi = pixel * 25.4 mm (1 in) / dimension (in mm)
        return pixel * 25.4 / dimension

    @staticmethod
    def dpi_to_pixels(dpi: int, dimension: float) -> int:
        # pixel = dpi * dimension (in mm) / 25.4 mm (1 in)
        return round(dpi * dimension / 25.4)

    @staticmethod
    def size_from_dpi_pixels(dpi: int, pixel: int) -> int:
        # length (in mm) = pixel * 25.4mm (1 in) / dpi
        return pixel * 25.4 / dpi

    @classmethod
    def from_string(cls, preset: str) -> tuple:
        return cls(cls.sizes.get(preset.upper(), (0, 0)))

    def to_print_resolution(self, dpi: int) -> tuple:
        return (self.dpi_to_pixels(self.x, dpi), self.dpi_to_pixels(self.y, dpi))
