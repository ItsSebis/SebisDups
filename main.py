# created by Aadil Matloob jan
# youtube: https://www.youtube.com/channel/UCTXiHVtLmYCRr_xGoWeefqg
from tkinter.filedialog import askdirectory
from tkinter import Tk
import os, hashlib
from pathlib import Path

Tk().withdraw()
path = askdirectory(title="Select a folder")

file_list = os.walk(path)

unique = dict()
duplicates = dict()
i = 1
print('Starting to list files')
for root, folders, files in file_list:
    for file in files:
        path = Path(os.path.join(root, file))
        try:
            fileHash = hashlib.md5(open(path, 'rb').read()).hexdigest()
            print(f'Files scanned: {i}/{len(files)}', end='\r')
            if fileHash not in unique:
                unique[fileHash] = path
            else:
                duplicates[str(path)] = root
                print(f'Duplicate: {path}')
        except:
            pass
        i += 1
print(f"Finished with {duplicates} duplicate files as shown above.")
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
                os.rename(path, os.path.join(duplicates[file], "DUP_"+file))
