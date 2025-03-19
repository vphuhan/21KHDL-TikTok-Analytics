import asyncio
import os
import time

import utils

USER_LISTS_DIR = "data/lists"
DATA_DIR = "data/raw/final"

if __name__ == "__main__":
    # file_path = os.path.join(USER_LISTS_DIR, "missing.txt")
    usernames = utils.read_usernames_from_file(
        "data/lists/final_users_list.txt")

    start_time = time.time()
    asyncio.run(utils.get_info_users(
        usernames, months=12+4, max_retries=5, batch_size=30,  data_path=DATA_DIR, user_path=USER_LISTS_DIR))
    end_time = time.time()

    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Execution time: {int(hours)}h {int(minutes)}m {seconds:.2f}s")
