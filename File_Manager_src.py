from os import scandir
from os.path import splitext, join, basename
from shutil import move
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json


# List of Directories.
# Replace directory addresses with one's created by you.
source_dir = ""
dest_dirs = {
    "SFX": "",
    "Music": "",
    "Vids": "",
    "Images": "",
    "Docs": "",
    "Installers": ""
}

# File extensions
# Convert lists to sets for faster lookup
file_extensions = {
    "Images": {".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"},
    "Vids": {".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
             ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"},
    "Music": {".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"},
    "Docs": {".doc", ".docx", ".odt",".pdf"}
}

# Pre-compute destination paths
dest_paths = {ext: path for category, extensions in file_extensions.items() for ext in extensions for path in dest_dirs[category]}

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.moved_files = []

    def on_modified(self, event):
        if not event.is_directory:
            file_ext = splitext(event.src_path)[1]
            if file_ext in dest_paths:
                move(event.src_path, dest_paths[file_ext])
                self.moved_files.append({
                    'original_path': event.src_path,
                    'new_path': dest_paths[file_ext],
                    'file_extension': file_ext
                })

    def write_logs_to_file(self):
        with open('moved_files_log.json', 'w') as f:
            json.dump(self.moved_files, f)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=source_dir, recursive=False)
observer.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    event_handler.write_logs_to_file()
    observer.stop()

observer.join()
