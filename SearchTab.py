from tkinter import *
from tkinter import messagebox

import GuiConfig

class SearchTab:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.searchBar = Frame(self.frame)
        self.searchBar.place( x=GuiConfig.TABS_PADDINGX, y=GuiConfig.SEARCH_BAR_PADDING_Y,
            width=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.SEARCH_BUTTON_WIDTH + GuiConfig.WIDGET_INTERVALX,
            height=max(GuiConfig.SEARCH_ENTRY_HEIGHT, GuiConfig.SEARCH_BUTTON_HEIGHT) + GuiConfig.WIDGET_INTERVALY,
            anchor=NW
        )

        self.searchStr = StringVar()
        self.searchStr.set("검색어를 입력하세요")
        self.entry = Entry(self.searchBar, textvariable=self.searchStr, font=GuiConfig.cFont)
        self.entry.place( x=GuiConfig.TABS_PADDINGX, y=0,
            width=GuiConfig.SEARCH_ENTRY_WIDTH, height=GuiConfig.SEARCH_ENTRY_HEIGHT,
            anchor=NW
        )

        self.button = Button(self.searchBar, text="검색", font=GuiConfig.cFont, command=self.search)
        self.button.place( x=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=0, width=GuiConfig.SEARCH_BUTTON_WIDTH, height=GuiConfig.SEARCH_BUTTON_HEIGHT,
            anchor=NW
        )

        self.result = Frame(self.frame, height=GuiConfig.SEARCH_RESULT_HEIGHT)
        self.result.place( x=GuiConfig.TABS_PADDINGX,
            y=max(GuiConfig.SEARCH_ENTRY_HEIGHT, GuiConfig.SEARCH_BUTTON_HEIGHT)
                + GuiConfig.WIDGET_INTERVALY + GuiConfig.SEARCH_BAR_PADDING_Y,
            width=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.VIEW_BUTTON_WIDTH + GuiConfig.WIDGET_INTERVALX,
            height=GuiConfig.SEARCH_RESULT_HEIGHT,
            anchor=NW
        )

        self.resultList = Listbox(self.result, font=GuiConfig.cFont)
        self.resultList.place( x=0, y=0,
            width=GuiConfig.SEARCH_RESULT_WIDTH, height=GuiConfig.SEARCH_RESULT_HEIGHT,
            anchor=NW
        )

        self.viewButton = Button(self.result, text="View", font=GuiConfig.cFont, command=self.view)
        self.viewButton.place( x=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=GuiConfig.VIEW_BUTTON_PADDINGY,
            width=GuiConfig.VIEW_BUTTON_WIDTH, height=GuiConfig.VIEW_BUTTON_HEIGHT,
            anchor=NW                      
        )

    def search(self):
        pass

    def view(self):
        pass