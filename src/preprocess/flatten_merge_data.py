import os
from tqdm import tqdm
from typing import List
import json
import pandas as pd

# Show all columns
pd.set_option('display.max_columns', None)


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


def flatten_json_data(y):
    # Reference: https://stackoverflow.com/questions/51359783/how-to-flatten-multilevel-nested-json

    out = {}

    def flatten(x, name=''):
        # List of columns to ignore
        ignore_columns = [
            "challenges", "contents", "textExtra", "video.bitrateInfo.",
            "video.claInfo.captionInfos", "video.cover", "video.downloadAddr",
            "video.dynamicCover", "video.originCover", "video.shareCover",
        ]
        for col in ignore_columns:
            if name.startswith(col):
                return

        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            # For now, we dont process list
            return
            # i = 0
            # for a in x:
            #     # flatten(a, name + str(i) + '_')
            #     flatten(a, name + str(i) + '_')
            #     i += 1
        else:
            # Not store the url
            if type(x) is str and x.startswith("http"):
                return
            out[name[:-1]] = x

    flatten(y)
    return out


def load_json_files_into_df(file_list: List[str]) -> pd.DataFrame:
    """ Load JSON files to a DataFrame.

    Args:
        file_list (List[str]): List of file paths.

    Returns:
        pd.DataFrame: DataFrame.
    """

    result_list = []
    for file in tqdm(file_list):
        with open(file, "r") as f:
            video_info_list = json.load(f)
            if not (type(video_info_list) is list):
                print(f"File {file} is not a list")
                # Convert to list
                video_info_list = [video_info_list]

            # Flatten the nested information for each video
            for video_info in video_info_list:
                result_list.append(flatten_json_data(video_info))

    # Load JSON data to DataFrame
    df = pd.DataFrame(result_list)
    return df


if __name__ == "__main__":
    # Example usage

    # ********** Phase 1: Load JSON files into a DataFrame **********
    # List all JSON files in the directory
    json_files = list_file_types("data/raw", ".json")
    # Split this list to user_info and video_info
    video_json_files = [
        file for file in json_files if file.endswith("/videos_info.json")]
    user_json_files = [
        file for file in json_files if file.endswith("/user_info.json")]

    # Load JSON files into a DataFrame
    video_info_df = load_json_files_into_df(video_json_files)
    user_info_df = load_json_files_into_df(user_json_files)

    # Convert video.id to string
    video_info_df["video.id"] = video_info_df["video.id"].astype(str)

    # ********** Phase 2: Load transcript data for each video **********
    # Load transcript data for each video
    audio_text_df = pd.read_csv("data/interim/audio_text.csv")

    # Rename columns
    audio_text_df.columns = ["author_name", "video_id", "audio_to_text"]

    # Select only video_id and audio_to_text columns
    audio_text_df = audio_text_df[["video_id", "audio_to_text"]]

    # Convert video_id to string
    audio_text_df["video_id"] = audio_text_df["video_id"].astype(str)

    # ********** Phase 3: Merge video_info_df and audio_text_df **********
    # Merge "video_info_df" and "audio_text_df" on "author_name" and "video_id"
    # This action will use left join to keep all rows in "video_info_df"
    # and append column "audio_to_text" to the right of "video_info_df"
    video_info_df = pd.merge(left=video_info_df, right=audio_text_df, how="left",
                             left_on="video.id", right_on="video_id")

    # Drop "video_id" column because it is duplicated
    video_info_df = video_info_df.drop(columns=["video_id"])

    # ********** Phase 4: Save DataFrame to CSV file **********
    video_info_df.to_csv("data/interim/video_info.csv", index=False)
    user_info_df.to_csv("data/interim/user_info.csv", index=False)
    print("Done")
