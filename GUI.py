import hashlib
import os
import tkinter as tk
import tkinter.font as tkFont
from threading import Thread
from queue import Queue
from pathlib import Path
from tkinter import ttk
from tkinter.filedialog import askdirectory


def countFiles(dir_path):
    count = 0
    for root_dir, cur_dir, files in os.walk(dir_path):
        count += len(files)
    return count


class GUI:
    def __init__(self):
        self.actions = None
        self.filecount = None
        self.statWin = None
        self.prog = None
        self.duplicates = None
        self.file_list = None
        self.bg = '#333'
        self.fg = '#eef'

        self.path = None
        self.start = tk.Tk()
        self.start.geometry('600x300')
        self.start.title("Sebi`s Duplicate Scanner")
        self.start.config(bg=self.bg)

        self.label = tk.Label(self.start, text="Scan file duplicates", font=('Arial', 18), fg=self.fg, bg=self.bg)
        font = tkFont.Font(self.label, self.label.cget('font'))
        font.configure(underline=True)
        self.label.configure(font=font)
        self.label.pack(padx=20, pady=30)

        self.selDirBut = tk.Button(self.start, text="Select directory", font=('Arial', 16), fg=self.fg, bg=self.bg,
                                   command=self.selScanDir)
        self.selDirBut.pack()

        self.scanBtn = tk.Button(self.start, text="Scan", font=('Arial', 18), fg=self.fg, bg=self.bg, state='disabled',
                                 command=self.scanWin)
        self.scanBtn.pack(pady=50)

        self.start.mainloop()

    def selScanDir(self):
        prePath = self.path
        self.path = askdirectory(title="Select a folder")
        if str(self.path) != "()" and str(self.path) != "":
            self.selDirBut["text"] = str(self.path)
            self.scanBtn["state"] = 'normal'
        else:
            self.path = prePath
        print(self.path)

    def scanWin(self):
        self.start.destroy()
        self.statWin = tk.Tk()
        self.statWin.geometry('500x200')
        self.statWin.title("Scanning")
        self.statWin.config(bg=self.bg)

        self.file_list = os.walk(self.path)
        self.filecount = countFiles(self.path)

        progLab = tk.Label(self.statWin, text="0/" + str(self.filecount), font=('Arial', 16), fg=self.fg, bg=self.bg)
        progLab.pack(pady=50)

        self.prog = ttk.Progressbar(self.statWin, orient='horizontal', mode='determinate', length=300)
        self.prog.place(y=120, x=100)

        thread = Thread(target=self.scan, daemon=True)
        thread.start()
        self.statWin.mainloop()
        self.postProgressing()

    def scan(self):

        # Search for duplicate files
        unique = dict()
        self.duplicates = dict()
        i = 1
        for root, folders, files in self.file_list:
            for file in files:
                path = Path(os.path.join(root, file))
                try:
                    # Get file content hash and check if it is a duplicate
                    fileHash = hashlib.md5(open(path, 'rb').read()).hexdigest()
                    progress = ((i / self.filecount) * 100)
                    self.prog['value'] = progress
                    print(progress)
                    if fileHash not in unique:
                        # New file
                        unique[fileHash] = path
                    else:
                        # Duplicate
                        self.duplicates[str(path)] = root
                except:
                    pass
                i += 1
        self.statWin.destroy()

    def postProgressing(self):
        print("post progressing now")
        self.actions = tk.Tk()
        self.actions.geometry('800x1000')
        self.actions.title("Actions for duplicates")
        self.actions.config(bg=self.bg)

        frame = tk.Frame(self.actions, bg=self.bg)
        frame.columnconfigure(0, weight=1)

        i = 0
        for dup in self.duplicates:
            path = tk.Label(self.actions, text=dup, font=('Arial', 12), bg=self.bg, fg=self.fg, bd=1,
                            width=int(self.actions.winfo_width()))
            if i % 2 == 0:
                path.config(bg='#444')
            path.pack(pady=3, fill="x")
            i += 1

        frame.pack(fill="x")

        self.actions.mainloop()
        print("finished")


GUI()
