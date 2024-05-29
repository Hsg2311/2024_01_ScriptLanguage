from tkinter import *
from tkinter import messagebox

from paper import Paper
from board import Board, Record

import GuiConfig

class SearchTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master

        self.frame = Frame(self.master)
        self.frame.pack()

        self.initWidgets()
        self.board=Board()
        self.curRecords = []
        self.trayBasePage = 1

    def initWidgets(self):
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
            width=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.SEARCH_VIEW_BUTTON_WIDTH + GuiConfig.WIDGET_INTERVALX,
            height=GuiConfig.SEARCH_RESULT_HEIGHT + GuiConfig.WIDGET_INTERVALY + GuiConfig.SEARCH_RESULT_TRAY_HEIGHT,
            anchor=NW
        )

        self.resultList = Frame(self.result, bg='white')
        self.resultList.place( x=0, y=0,
            width=GuiConfig.SEARCH_RESULT_WIDTH, height=GuiConfig.SEARCH_RESULT_HEIGHT,
            anchor=NW
        )

        self.pageTray = Frame(self.result)
        self.pageTray.place( x=(GuiConfig.SEARCH_RESULT_WIDTH - GuiConfig.SEARCH_RESULT_TRAY_WIDTH) // 2,
            y=GuiConfig.SEARCH_RESULT_HEIGHT + GuiConfig.WIDGET_INTERVALY,
            width=GuiConfig.SEARCH_RESULT_TRAY_WIDTH,
            height=GuiConfig.SEARCH_RESULT_TRAY_HEIGHT,
            anchor=NW
        )
        self.pageTrayButtons = [None] * Board.PAGE_CNT_IN_A_TRAY

        self.viewButton = Button(self.result, text="View", font=GuiConfig.cFont, command=self.view)
        self.viewButton.place( x=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=GuiConfig.SEARCH_VIEW_BUTTON_PADDINGY,
            width=GuiConfig.SEARCH_VIEW_BUTTON_WIDTH, height=GuiConfig.SEARCH_VIEW_BUTTON_HEIGHT,
            anchor=NW                      
        )

    def search(self):
        # self.board.search(self.searchStr.get())

        # temporary implementation
        self.board.loadCache(self.searchStr.get())

        self.update()

    def update(self):
        for widgets in self.resultList.winfo_children():
            widgets.destroy()

        for widgets in self.pageTray.winfo_children():
            widgets.destroy()

        self.curRecords = []

        for i in range(min(Board.RECORD_CNT_IN_A_PAGE, self.board.length())):
            self.curRecords.append(
                Record(self.board.get(i), self.resultList)
            )
            self.curRecords[-1].grid(i, 0)
            self.resultList.grid_rowconfigure(i, weight=1)
        self.resultList.grid_columnconfigure(0, weight=1)

        trayLen = min( self.board.length() // Board.RECORD_CNT_IN_A_PAGE,
            Board.PAGE_CNT_IN_A_TRAY
        )

        Button( self.pageTray, text="<", font=GuiConfig.cFont,
            command=self.prevPage
        ).grid(row=0, column=0)
        self.pageTray.grid_columnconfigure(0, weight=1)

        for i in range(trayLen):
            self.pageTrayButtons[i] = Button(
                self.pageTray, text=str(self.trayBasePage + i), font=GuiConfig.cFont,
                command=lambda i=self.trayBasePage + i: self.selectPage(i)
            )
            self.pageTrayButtons[i].grid(row=0, column=i+1)
            self.pageTray.grid_columnconfigure(i+1, weight=1)
        self.pageTray.grid_rowconfigure(0, weight=1)

        Button( self.pageTray, text=">", font=GuiConfig.cFont,
            command=self.nextPage
        ).grid(row=0, column=trayLen+1)
        self.pageTray.grid_columnconfigure(trayLen+1, weight=1)

        self.pageTrayButtons[(self.board.pageNum - 1) % Board.PAGE_CNT_IN_A_TRAY]['bg'] = 'light gray'
            
    def selectPage(self, i):
        self.board.selectPage(i)
        self.update()

    def nextPage(self):
        if self.board.pageNum % Board.PAGE_CNT_IN_A_TRAY == 0:
            self.trayBasePage += Board.PAGE_CNT_IN_A_TRAY

        self.board.nextPage()
        self.update()

    def prevPage(self):
        self.board.prevPage()

        if self.board.pageNum % Board.PAGE_CNT_IN_A_TRAY == 0:
            self.trayBasePage -= Board.PAGE_CNT_IN_A_TRAY

        self.update()

    def view(self):
        item = self.resultList.focus_get()
        if not isinstance(item, Text):
            return
        
        for rec in self.curRecords:
            if rec.owns(item):
                self.mainGUI.viewTab.setPaper(rec.paper)

        self.mainGUI.viewTab.show(self)