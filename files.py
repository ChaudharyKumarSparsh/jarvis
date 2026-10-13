import os
import platform
import subprocess

import config

from pathlib import Path

# HOME = Path.home()
# SEARCH_FOLDERS = [
#     HOME / "Desktop",
#     HOME / "Documents",
#     HOME / "Downloads",
#     HOME / "Pictures",                                    Removed as they are already in the config file
#     HOME / "Music",
#     HOME / "Videos",
#     HOME / "OneDrive",
#     Path("D:/"),
#     Path("E:/")
# ]
# SKIP_FOLDERS = {"node_modules", ".git", "__pycache__", ".venv", "venv", "AppData"}


def clean(name):
    return name.lower().replace("_", " ").replace("-", " ").replace(".", " ")


def score(query, filename):
    name = clean(filename)
    stem = clean(Path(filename).stem)
    if stem == query:
        return 3
    if query in name:
        return 2
    if all(word in name for word in query.split()):
        return 1
    return 0


def find_files(query, limit = 5):
    query = clean(query).strip()
    matches = []
    for folder in config.SEARCH_FOLDERS:
        if not folder.exists():
            continue
        for current_folder, subfolders, filenames in os.walk(folder):
            subfolders[:] = [f for f in subfolders
                             if f not in config.SKIP_FOLDERS and not f.startswith(".")]
            for filename in filenames:
                points = score(query, filename)
                if points > 0:
                    full_path = os.path.join(current_folder, filename)
                    matches.append((points, full_path))

    matches.sort(key = lambda match: match[0], reverse = True)
    return [path for points, path in matches[:limit]]


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])



if __name__ == '__main__':
    for path in find_files("sparsh"):
        print(path)