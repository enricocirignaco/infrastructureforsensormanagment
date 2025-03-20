import os
import shutil
import time
from datetime import datetime

LOG_FILE_PATH = os.path.join(os.getenv("DEFAULT_LOG_DIR"), "cleaner.log")
DIRS_TO_CLEAN = [os.getenv("DEFAULT_SOURCE_DIR"), os.getenv("DEFAULT_OUTPUT_DIR"), os.getenv("DEFAULT_LOG_DIR")]
CLEAN_INTERVAL = int(os.getenv("CLEANING_INTERVAL_HOURS", 24)) * 3600  # Convert to seconds

# Log messages to a log file situated in /logs/cleaner.log
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    try:
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(full_message + "\n")
    except Exception as e:
        print(f"Cleaner: Failed to write log: {e}", flush=True)

# Clean directories
def clean_dirs():
    try:
        for dir_path in DIRS_TO_CLEAN:
            if os.path.isdir(dir_path):
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    try:
                        if os.path.isfile(item_path) and os.path.basename(item_path) == "cleaner.log":
                            continue  # Skip log file
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                        log_message(f"Cleaner: Removed {item_path}")
                    except Exception as e:
                        log_message(f"Cleaner: Failed to remove {item_path}: {e}")
    except Exception as e:
        log_message(f"Cleaner: Failed to clean directories: {e}")

if __name__ == "__main__":
    while True:
        clean_dirs()
        time.sleep(CLEAN_INTERVAL)