from tkinter import *
from tkinter import messagebox

class MemoTab:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.grids = Frame(self.frame)
        self.grids.place(x=10, y=10, width=680, height=540)

        self.memos = []

        for i in range(5):
            for j in range(5):
                tmp = Text(self.grids)
                tmp.grid(row=i, column=j, padx=10, pady=10)
                self.memos.append(tmp)

        for i in range(5):
            self.grids.grid_rowconfigure(i, weight=1)
            self.grids.grid_columnconfigure(i, weight=1)