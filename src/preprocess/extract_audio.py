# Description: Extract audio from mp4 files in a directory
# and save them as wav files.

import os
import multiprocessing
from moviepy.editor import VideoFileClip
from tqdm import tqdm
from typing import List


def list_file_types(directory: str, file_extension: str) -> List[str]:
    """ List all files with a specific extension in a directory.

    Args:
        directory (str): Directory path.
        file_extension (str): File extension.

    Returns:
        List[str]: List of file paths.
    """

    file_list: List[str] = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                file_list.append(os.path.join(root, file))
    return file_list


def extract_audio(mp4_file: str) -> None:
    # Split the path into a list of directories and the file name
    path_list: List[str] = mp4_file.split(os.sep)

    # Create a folder for the audio file (if it doesn't exist)
    audio_folder: str = os.path.join(os.sep.join(path_list[:3]), "audio")
    os.makedirs(audio_folder, exist_ok=True)

    # Get the file name without the extension
    file_name: str = os.path.splitext(path_list[-1])[0]

    # Create the path for the audio file
    audio_file: str = os.path.join(audio_folder, file_name + ".wav")

    # Extract the audio from the video file
    video = VideoFileClip(mp4_file)
    video.audio.write_audiofile(audio_file, verbose=False)

    # Close the video file
    video.close()


if __name__ == "__main__":
    # Example usage
    directory_path: str = "data/raw"
    mp4_files: List[str] = list_file_types(
        directory_path, file_extension=".mp4")

    # Create a pool of workers
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Use tqdm to display the progress bar
    for _ in tqdm(pool.imap_unordered(extract_audio, mp4_files),
                  total=len(mp4_files)):
        pass

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()
