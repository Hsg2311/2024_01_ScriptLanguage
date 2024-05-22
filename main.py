from tkinter import *
from tkinter import ttk

from SearchTab import *
from BookmarkTab import *
from MemoTab import *
from LogTab import *

class MainGUI:
    def __init__(self):
        self.master = Tk()
        self.master.title("Main GUI")
        self.master.geometry("800x600")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=BOTH, expand=True)

        self.searchTab = SearchTab(self.master)
        self.notebook.add(self.searchTab.frame, text="검색")

        self.bookmarkTab = BookmarkTab(self.master)
        self.notebook.add(self.bookmarkTab.frame, text="북마크")

        self.memoTab = MemoTab(self.master)
        self.notebook.add(self.memoTab.frame, text="메모")

        self.logTab = LogTab(self.master)
        self.notebook.add(self.logTab.frame, text="열람 기록")

        self.master.mainloop()

if __name__ == "__main__":
    MainGUI()
        