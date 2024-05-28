from tkinter import *
from tkinter import messagebox

class Memo:
    WIDTH = 24  # number of characters
    HEIGHT = 8  # number of lines

    def __init__(self, master, text=''):
        self.master = master
        self.text = text
        self.widget = Text(self.master, width = Memo.WIDTH, height = Memo.HEIGHT)
        self.widget.insert(END, self.text)

    def grid(self, i, j):
        self.widget.grid(row=i, column=j, padx=10, pady=10)

class MemoTab:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.grids = Frame(self.frame)
        self.grids.place(x=10, y=10, width=680, height=580)

        self.memos = [
            [Memo(self.grids, 'Memo 1'), Memo(self.grids, 'Memo 2')],
            [Memo(self.grids, 'Memo 3'), Memo(self.grids, 'Memo 4')]
        ]

        for i in range(len(self.memos)):
            for j in range(len(self.memos[i])):
                self.memos[i][j].grid(i, j)