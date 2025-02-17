# Description: This script converts audio files to text
# using the Google Speech-to-Text API.

import os
import speech_recognition as sr
import pandas as pd
from tqdm import tqdm
import multiprocessing
import json
from typing import List


# Define the path to the directory containing the transcript files
TRANSCRIPT_DIR = "data/interim/audio_text_list"


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


def process_audio(wav_file):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(wav_file) as source:
        # Listen for the data (load audio to memory)
        audio = recognizer.record(source)

        # Recognize the text in the audio file
        # Now, we only support the Vietnamese language
        try:
            text = recognizer.recognize_google(audio, language="vi-VN")
        # Except all errors
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")
            text = None

    # Get the file name without extension
    file_name = os.path.splitext(os.path.basename(wav_file))[0]

    # Find the last occurrence of the underscore character
    last_underscore_index = file_name.rfind("_")
    # Get the author name and video ID
    author_name = file_name[:last_underscore_index]
    video_id = file_name[last_underscore_index + 1:]

    # Create the result dictionary
    result = {
        "author_name": author_name,
        "video_id": video_id,
        "audio_to_text": text
    }

    # Save the result to a JSON file
    json_file = os.path.join(TRANSCRIPT_DIR, file_name + ".json")
    with open(json_file, "w") as f:
        json.dump(result, f)


def load_json_files_into_df(directory: str) -> pd.DataFrame:
    """ Load JSON files into a DataFrame.

    Args:
        directory (str): Directory path.

    Returns:
        pd.DataFrame: DataFrame containing the JSON data.
    """

    json_files: List[str] = list_file_types(directory, ".json")
    result_list = []
    for json_file in json_files:
        with open(json_file) as f:
            result_list.append(json.load(f))
    return pd.DataFrame(result_list)


if __name__ == "__main__":
    # Example usage
    wav_files: List[str] = list_file_types(
        directory="data/raw", file_extension=".wav")

    # Create a pool of workers
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Use tqdm to display the progress bar
    for _ in tqdm(pool.imap_unordered(process_audio, wav_files),
                  total=len(wav_files)):
        pass

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    # Create a DataFrame from the result list
    df = load_json_files_into_df(directory=TRANSCRIPT_DIR)

    # Save the DataFrame to a CSV file
    df.to_csv("data/interim/audio_text.csv", index=False)
