import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from pathlib import Path

# Directories
SOURCE_DIR = "/source"
RESULT_DIR = "./YOLOX_outputs/yolox_x/"

# YOLOX command template (using CPU)
YOLOX_COMMAND = [
    "python", "tools/demo.py", "image",
    "-n", "yolox_l",
    "-c", "/workspace/YOLOX/yolox_l.pth",
    "--conf", "0.25",
    "--nms", "0.25",
    "--tsize", "640",
    "--save_result",
    "--device", "cpu"  # Use CPU instead of GPU
]


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a new file is created in the monitored directory."""
        if event.is_directory:
            print(f"Ignoring directory creation: {event.src_path}")
            return

        file_path = event.src_path
        print(f"New file detected: {file_path}")

        # Process the file with YOLOX
        try:
            yolox_command = YOLOX_COMMAND + ["--path", file_path] + ["-expn", file_path[8:13]]
            print(f"Running YOLOX command: {' '.join(yolox_command)}")
            subprocess.run(yolox_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing file {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        else:
            # Optionally, remove the original file after processing
            try:
                os.remove(file_path)
                print(f"Processed and removed: {file_path}")
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")

def monitor_directory(directory):
    """Monitor the directory for new files."""
    event_handler = NewFileHandler()
    print(f"Monitoring directory: {directory}")
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()
    observer.is_alive()

    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
        observer.stop()
    observer.join()
    print("Observer stopped.")

if __name__ == "__main__":
	# Start monitoring the source directory
	monitor_directory(SOURCE_DIR)

