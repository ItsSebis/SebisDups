# based on code by Aadil Matloob jan
# video: Detect and Delete Duplicate files with python
# uri: https://www.youtube.com/watch?v=XrALbgIbHzc
# youtube: https://www.youtube.com/channel/UCTXiHVtLmYCRr_xGoWeefqg

import hashlib
import os
import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askdirectory

tk.Tk().withdraw()
path = askdirectory(title="Select a folder")
# Get Folder to scan

file_list = os.walk(path)

# Search for duplicate files
unique = dict()
duplicates = dict()
i = 1
print('Starting to list files')
for root, folders, files in file_list:
    for file in files:
        path = Path(os.path.join(root, file))
        try:
            # Get file content hash and check if it is a duplicate
            fileHash = hashlib.md5(open(path, 'rb').read()).hexdigest()
            print(f'Files scanned: {i}/{len(files)}', end='\r')
            if fileHash not in unique:
                # New file
                unique[fileHash] = path
            else:
                # Duplicate
                duplicates[str(path)] = root
                print(f'Duplicate: {path}')
        except:
            pass
        i += 1

# What to do with those duplicate files
print(f"Finished with {len(duplicates)} duplicate files as shown above.")
action = input("What do you want to do? (d - Delete, r - rename, n - nothing): ")
actions = ('d', 'delete', 'r', 'rename', 'n', 'nothing')
while action not in actions:
    action = input("What do you want to do? (d - Delete, r - rename, n - nothing): ")
match action:
    case 'd', 'delete':
        for file in duplicates:
            os.remove(file)
    case 'r', 'rename':
        for file in duplicates:
            if not file.startswith('DUP_'):
                os.rename(path, os.path.join(duplicates[file], "DUP_" + file))
