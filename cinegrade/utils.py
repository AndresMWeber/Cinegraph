import enum
import os


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


def convert_unit(size_in_bytes, unit):
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
