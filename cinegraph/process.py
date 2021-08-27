import os
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager, cpu_count
from cinegraph.images import Video, draw_center_box, get_dominant_color, write_img_to_dir
from cinegraph.gradient import create_cinegraph
from cinegraph.utils import Config, chunk_list, get_filename


def write_video_snap(image, frame_number, dominant_color, video_file_path):
    draw_center_box(image, dominant_color, Config.box_size)
    filename = get_filename(video_file_path)
    write_img_to_dir(image, os.path.join(Config.output_dir, filename), f"f_{frame_number}.jpg")


def process_chunk(video_file_path, frame_numbers, colors):
    video = Video(video_file_path)
    for frame_number in frame_numbers:
        process_frame(video, frame_number, colors, video_file_path)
    video.release()


def process_frame(video, frame_number, colors, video_file_path):
    image = video.get_frame(frame_number)
    if len(image):
        dominant_color = get_dominant_color(image)
        colors.append(dominant_color)
        if Config.write_frames:
            write_video_snap(image, frame_number, dominant_color, video_file_path)


def process_video(video_file_path):
    if not (Path(video_file_path).is_file()):
        raise FileNotFoundError(f"Could not find associated video file {video_file_path}")

    video = Video(video_file_path, Config.num_colors)
    colors = []
    frame_numbers = range(0, len(video), video.frame_step)
    video.release()
    chunks = list(chunk_list(frame_numbers, Config.chunk_size))

    with tqdm(total=len(chunks)) as pbar:
        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            with Manager() as manager:
                colors = manager.list()
                futures = [
                    executor.submit(process_chunk, video_file_path, chunk_frames, colors) for chunk_frames in chunks
                ]

                for _ in as_completed(futures):
                    pbar.update(1)
                pbar.close()
                gradient = create_cinegraph(colors)
                return gradient
