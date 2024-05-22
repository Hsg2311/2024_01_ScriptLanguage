from tkinter import *
from tkinter import messagebox

class BookmarkTab:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.label = Label(self.frame, text="Bookmark Tab")
        self.label.pack()

        self.button = Button(self.frame, text="Click Me", command=self.click)
        self.button.pack()

    def click(self):
        messagebox.showinfo("Bookmark Tab", "You clicked the button in the Bookmark Tab")