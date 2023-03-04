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
files = askdirectory(title="Files to move")
print(files)
ref = askdirectory(title="Reference folder")
print(ref)
dest = askdirectory(title="Destination folder")
print(dest)

if str(files) == '()' or str(ref) == '()' or str(dest) == '()':
    print("quit due to invalid input")
    quit()

# Get Folder to scan
file_list = os.walk(ref)

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
        except:
            pass
        i += 1

# Move files
file_list = os.walk(files)
for root, folders, files in file_list:
    for file in files:
        path = Path(os.path.join(root, file))
        path_to = Path(os.path.join(dest, file))
        try:
            fileHash = hashlib.md5(open(path, 'rb').read()).hexdigest()
            if fileHash not in unique:
                os.rename(path, path_to)
        except:
            pass
