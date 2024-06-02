from tkinter import *
from tkinter import ttk

from SearchTab import *
from BookmarkTab import *
from MemoTab import *
from LogTab import *
from ViewTab import *

from GIFAnimation import *
import GuiConfig

class MainGUI:
    def __init__(self):
        self.master = Tk()
        self.master.title("Papery")
        self.master.geometry(str(GuiConfig.WIDTH) + "x" + str(GuiConfig.HEIGHT))
        GuiConfig.initFonts()

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack( fill=BOTH, expand=True, side=LEFT,
            padx=GuiConfig.TABS_PADDINGX, pady=GuiConfig.TABS_PADDINGY
        )

        self.searchTab = SearchTab(self)
        self.notebook.add(self.searchTab.frame, text="검색")

        self.bookmarkTab = BookmarkTab(self)
        self.notebook.add(self.bookmarkTab.frame, text="북마크")
        self.searchTab.addBookmarkTab(self.bookmarkTab)

        self.memoTab = MemoTab(self)
        self.notebook.add(self.memoTab.frame, text="메모")

        self.logTab = LogTab(self)
        self.notebook.add(self.logTab.frame, text="열람 기록")

        self.viewTab = ViewTab(self)
        self.notebook.add(self.viewTab.frame, text="보기")

        self.notebook.hide(self.viewTab.frame)

        self.gif = GIFAnimation(GuiConfig.GIF_WIDTH, GuiConfig.GIF_HEIGHT)
        self.gifLabel = Label(self.master, image=self.gif.image())
        self.gifLabel.place(
            x=GuiConfig.WIDTH - GuiConfig.GIF_PADDINGX, y=GuiConfig.GIF_PADDINGY,
            anchor=NE, width=GuiConfig.GIF_WIDTH, height=GuiConfig.GIF_HEIGHT
        )

        self.defaultbg = self.master.cget('bg')

        self.master.after(100, self.updateGIF)
        self.master.mainloop()

    def updateGIF(self):
        self.gif.advance()
        self.gifLabel.configure(image=self.gif.image())
        self.master.after(100, self.updateGIF)

if __name__ == "__main__":
    MainGUI()
        