from tkinter import *
from tkinter import ttk

from SearchTab import *
from BookmarkTab import *
from MemoTab import *
from LogTab import *

from GIFAnimation import *

class MainGUI:
    GIF_WIDTH = 150
    GIF_HEIGHT = 100
    GIF_PADDINGX = 20
    GIF_PADDINGY = 10
    TABS_PADDINGX = 20
    TABS_PADDINGY = 20

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        self.master = Tk()
        self.master.title("Main GUI")
        self.master.geometry(str(MainGUI.WIDTH) + "x" + str(MainGUI.HEIGHT))

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack( fill=BOTH, expand=True, side=LEFT,
            padx=MainGUI.TABS_PADDINGX, pady=MainGUI.TABS_PADDINGY
        )

        self.searchTab = SearchTab(self.master)
        self.notebook.add(self.searchTab.frame, text="검색")

        self.bookmarkTab = BookmarkTab(self.master)
        self.notebook.add(self.bookmarkTab.frame, text="북마크")

        self.memoTab = MemoTab(self.master)
        self.notebook.add(self.memoTab.frame, text="메모")

        self.logTab = LogTab(self.master)
        self.notebook.add(self.logTab.frame, text="열람 기록")

        self.gif = GIFAnimation(MainGUI.GIF_WIDTH, MainGUI.GIF_HEIGHT)
        self.gifLabel = Label(self.master, image=self.gif.image())
        self.gifLabel.place(
            x=MainGUI.WIDTH - MainGUI.GIF_PADDINGX, y=MainGUI.GIF_PADDINGY,
            anchor=NE, width=MainGUI.GIF_WIDTH, height=MainGUI.GIF_HEIGHT
        )

        self.master.after(100, self.updateGIF)
        self.master.mainloop()

    def updateGIF(self):
        self.gif.advance()
        self.gifLabel.configure(image=self.gif.image())
        self.master.after(100, self.updateGIF)

if __name__ == "__main__":
    MainGUI()
        