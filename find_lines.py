# Create a script that should find the lines by provided pattern in the provided path directory with recursion
# (it means if the directory has other directories, the script should get all the info from them as well) and threads.

import os
from concurrent.futures import ThreadPoolExecutor
import time
import re

# with os.scandir("/home/vadym/Documents/cursor/Python-Basic-Steve-Trevor/homeworks/") as scan:
#     for el in scan:
#         print(el.name)

def find_all_files(dirpath):
    all_files = []
    with os.scandir(dirpath) as scan:
        for entry in scan:
            if entry.is_dir(follow_symlinks=False) and entry.name != "venv":
                all_files.extend(find_all_files(entry.path))
            elif entry.is_file(follow_symlinks=False) and re.search("\.py$", entry.name):
                all_files.append(entry.path)
    return all_files

def find_line_in_file(filepath, pattern):
    lines_with_pattern = set()
    with open(filepath) as file:
        for line in file:
            if pattern in line:
                lines_with_pattern.add(line)
    return lines_with_pattern

def find_all_lines(path, pattern):
    lines_with_pattern = set()
    all_files = find_all_files(path)
    with ThreadPoolExecutor() as executor:                                                      #multithreading
        result = executor.map(find_line_in_file, all_files, (pattern for _ in all_files))       #
    for el in result:                                                                           #
        lines_with_pattern.update(el)                                                           #
    # for file in all_files:                                              #not multithreading
    #     lines_with_pattern.update(find_line_in_file(file, pattern))     #
    return lines_with_pattern

if __name__ == "__main__":
    start = time.time()
    lines = find_all_lines(".", "random")
    for line in lines:
        print(line.replace("\n", ""))
    print(len(lines))
    duration = time.time() - start
    print(duration)
