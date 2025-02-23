import subprocess
import sys
import time
import os
<<<<<<< HEAD

def get_python_executable():
    """Get the correct Python executable path"""
    if sys.platform == "win32":
        # Use the same Python interpreter that's running this script
        return sys.executable
    return "python"
=======
from yt_dlp import YoutubeDL
>>>>>>> origin/vmphat

def run_crawler(keyword, limit):
    """
    Run the crawler script with given keyword and limit
    Returns True if successful, False otherwise
    """
    try:
        print(f"\nStarting crawler for keyword: {keyword}")
        
        # Set environment variable for UTF-8 encoding
        my_env = os.environ.copy()
        my_env["PYTHONIOENCODING"] = "utf-8"
        
        # On Windows, force the console to use UTF-8
        if sys.platform == "win32":
            my_env["PYTHONUTF8"] = "1"
        
        # Get the absolute path to crawler.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        crawler_path = os.path.join(current_dir, "crawler.py")
        
        # Use the correct Python executable
        python_exe = get_python_executable()
        
        process = subprocess.run(
            [python_exe, crawler_path, keyword, str(limit)],
            check=True,
            text=True,
            capture_output=True,
            env=my_env,
            encoding='utf-8'
        )
        print(f"Successfully completed crawler for {keyword}")
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running crawler for {keyword}: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error for {keyword}: {e}")
        print(f"Command tried to run: {python_exe} {crawler_path} {keyword} {limit}")
        return False


def main():
    # List of tasks to run sequentially
    tasks = [
        # ********** Tin tuc - Giai tri **********
        ("nhactamtrang", 50),
        ("phongthuy", 50),
        ("drama", 50),
        ("tintuc", 50),
        ("nhacchill", 50),

        # ********** Du lich **********
        ("festival", 50),
        ("dulich", 50),
        ("amthuc", 50),
        ("paradise", 50),
        ("homestay", 50),
    
    ]
    # Set console to UTF-8 mode on Windows
    if sys.platform == "win32":
        os.system("chcp 65001")

    total_tasks = len(tasks)
    completed_tasks = 0

    for keyword, limit in tasks:
        completed_tasks += 1
        print(f"\n[{completed_tasks}/{total_tasks}] Running task for: {keyword}")

        if run_crawler(keyword, limit):
            print(f"Completed {completed_tasks} of {total_tasks} tasks")
        else:
            print(f"Task failed for {keyword}. Continuing with next task...")

        # Add a small delay between tasks to prevent any potential issues
        if completed_tasks < total_tasks:
            time.sleep(2)


if __name__ == "__main__":
    print("Starting sequential crawler execution...")
    main()
    print("\nAll tasks completed!")
