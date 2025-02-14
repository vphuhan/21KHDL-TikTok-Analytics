import os
import json
from datetime import datetime, timezone
import pandas as pd

# Define the root directory where the hashtag folders are stored
root_dir = "./data/raw/videos/"
# print(os.listdir(root_dir))

# Initialize dictionaries for unique authors, music, and lists for other data
author_dict = {}
music_dict = {}
video_data = []
hashtag_data = []
challenge_data = []
video_format_data = []
anchor_data = []

# Iterate through all hashtag folders
for hashtag_folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, hashtag_folder)
    json_file_path = os.path.join(folder_path, "videos_info.json")

    if os.path.isfile(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            video_data_json = json.load(f)  # Load JSON data

        # Extract relevant fields
        for video in video_data_json:
            # Author data
            author = video.get("author", {})
            author_stats = video.get("authorStats", {})
            author_id = author.get("id", "")
            
            if author_id and author_id not in author_dict:
                author_dict[author_id] = {
                    "Author ID": author_id,
                    "Nickname": author.get("nickname", ""),
                    "Unique ID": author.get("uniqueId", ""),
                    "Verified": author.get("verified", False),
                    "Followers": author_stats.get("followerCount", 0),
                    "Total Likes": author_stats.get("heartCount", 0),
                    "Signature": author.get("signature", ""),
                    "Profile Picture": author.get("avatarThumb", ""),
                }

            # Music data
            music = video.get("music", {})
            music_id = music.get("id", "")
            if music_id and music_id not in music_dict:
                music_dict[music_id] = {
                    "Music ID": music_id,
                    "Title": music.get("title", ""),
                    "Author": music.get("authorName", ""),
                    "Play URL": music.get("playUrl", ""),
                }

            # Video data
            stats = video.get("stats", {})
            stats_v2 = video.get("statsV2", {})
            video_row = {
                "Video ID": video.get("id", ""),
                "Author ID": author_id,
                "Description": video.get("desc", ""),
                "Posting Date": datetime.fromtimestamp(int(video.get("createTime", 0)), timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                "Play Count": stats.get("playCount", 0),
                "Likes": stats.get("diggCount", 0),
                "Comments": stats.get("commentCount", 0),
                "Shares": stats.get("shareCount", 0),
                "Saves": stats.get("collectCount", 0),
                "Reposts": stats_v2.get("repostCount", 0),
                "Duration": video.get("video", {}).get("duration", 0),
                "Video URL": video.get("video", {}).get("playAddr", ""),
                "Cover Image": video.get("video", {}).get("cover", ""),
                "Music ID": music_id,
                "Duet Enabled": video.get("duetEnabled", False),
                "Stitch Enabled": video.get("stitchEnabled", False),
            }
            video_data.append(video_row)

            # Hashtag data
            for tag in video.get("challenges", []):
                hashtag_row = {
                    "Video ID": video.get("id", ""),
                    "Hashtag ID": tag.get("id", ""),
                    "Hashtag Name": tag.get("title", ""),
                    "Hashtag View Count": tag.get("stats", {}).get("viewCount", 0)
                }
                hashtag_data.append(hashtag_row)

            # Challenge data
            for challenge in video.get("challenges", []):
                challenge_row = {
                    "Challenge ID": challenge.get("id", ""),
                    "Title": challenge.get("title", ""),
                    "Description": challenge.get("desc", ""),
                    "View Count": challenge.get("stats", {}).get("viewCount", 0),
                }
                challenge_data.append(challenge_row)

            # Video formats (bitrate and quality details)
            for format_info in video.get("video", {}).get("bitrateInfo", []):
                format_row = {
                    "Video ID": video.get("id", ""),
                    "Bitrate": format_info.get("Bitrate", 0),
                    "Codec Type": format_info.get("CodecType", ""),
                    "Quality Type": format_info.get("QualityType", ""),
                }
                video_format_data.append(format_row)

            # Anchor data (if available)
            for anchor in video.get("anchors", []):
                anchor_row = {
                    "Video ID": video.get("id", ""),
                    "Anchor Type": anchor.get("type", ""),
                    "Anchor Title": anchor.get("title", ""),
                }
                anchor_data.append(anchor_row)

# Convert dictionaries and lists to DataFrames
df_author = pd.DataFrame(author_dict.values())
df_music = pd.DataFrame(music_dict.values())
df_video = pd.DataFrame(video_data)
df_hashtag = pd.DataFrame(hashtag_data)
df_challenge = pd.DataFrame(challenge_data)
df_video_format = pd.DataFrame(video_format_data)
df_anchor = pd.DataFrame(anchor_data)

# Save to CSV
csv_author_path = "./src/preprocess/csv/tiktok_authors.csv"
df_author.to_csv(csv_author_path, index=False, encoding="utf-8")

csv_music_path = "./src/preprocess/csv/tiktok_music.csv"
df_music.to_csv(csv_music_path, index=False, encoding="utf-8")

csv_video_path = "./src/preprocess/csv/tiktok_videos.csv"
df_video.to_csv(csv_video_path, index=False, encoding="utf-8")

csv_hashtag_path = "./src/preprocess/csv/tiktok_hashtags.csv"
df_hashtag.to_csv(csv_hashtag_path, index=False, encoding="utf-8")

csv_challenge_path = "./src/preprocess/csv/tiktok_challenges.csv"
df_challenge.to_csv(csv_challenge_path, index=False, encoding="utf-8")

csv_video_format_path = "./src/preprocess/csv/tiktok_video_formats.csv"
df_video_format.to_csv(csv_video_format_path, index=False, encoding="utf-8")

csv_anchor_path = "./src/preprocess/csv/tiktok_anchors.csv"
df_anchor.to_csv(csv_anchor_path, index=False, encoding="utf-8")

print(f"Data successfully saved to multiple CSV files.")
