import os

path = os.getcwd()

files = []
for root, _, files_in_dir in os.walk(path):
    for file in files_in_dir:
        if ".html" in file:
            files.append(os.path.join(root, file))

file_count = 0
for f in files:
    try:
        with open(f, "r") as f:
            file_count += 1
    except:
        print("failed")

print("file count:", file_count)
