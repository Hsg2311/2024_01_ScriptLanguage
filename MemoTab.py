from tkinter import *
from tkinter import messagebox

class Memo:
    WIDTH = 28  # number of characters
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
            [Memo(self.grids, 'Memo 1'), Memo(self.grids, 'Memo 2'), Memo(self.grids, 'Memo 3')],
            [Memo(self.grids, 'Memo 6'), Memo(self.grids, 'Memo 7')]
        ]

        for i in range(len(self.memos)):
            for j in range(len(self.memos[i])):
                self.memos[i][j].grid(i, j)

        self.addButton = Button(self.frame, text="+", command=self.addMemo)
        self.addButton.place(x=700, y=40, width=60, height=50)

        self.delButton = Button(self.frame, text="-", command=self.delMemo)
        self.delButton.place(x=700, y=90, width=60, height=50)

        self.mailButton = Button(self.frame, text="Mail", command=self.mail)
        self.mailButton.place(x=700, y=200, width=60, height=50)

        self.sendButton = Button(self.frame, text="Send", command=self.send)
        self.sendButton.place(x=700, y=260, width=60, height=50)

    def addMemo(self):
        pass

    def delMemo(self):
        pass

    def mail(self):
        pass

    def send(self):
        pass