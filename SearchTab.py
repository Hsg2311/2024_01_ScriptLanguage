from tkinter import *
from tkinter import messagebox

from paper import Paper
from board import Board, Record

from Loading import Loading

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
        self.searchBar.place( x=GuiConfig.TABS_PADDINGX * 2, y=GuiConfig.SEARCH_BAR_PADDING_Y,
            width=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.SEARCH_BUTTON_WIDTH + GuiConfig.WIDGET_INTERVALX * 2 + GuiConfig.SEARCH_MODE_TRAY_WIDTH,
            height=max(GuiConfig.SEARCH_ENTRY_HEIGHT, GuiConfig.SEARCH_BUTTON_HEIGHT) + GuiConfig.WIDGET_INTERVALY,
            anchor=NW
        )

        self.searchStr = StringVar()
        self.searchStr.set("검색어를 입력하세요")
        self.entry = Entry(self.searchBar, textvariable=self.searchStr, font=GuiConfig.cFont)
        self.entry.place( x=0, y=0, width=GuiConfig.SEARCH_ENTRY_WIDTH,
            height=GuiConfig.SEARCH_ENTRY_HEIGHT, anchor=NW
        )

        self.searchButton = Button(self.searchBar, text="검색", font=GuiConfig.cFont, command=self.search)
        self.searchButton.place( x=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.WIDGET_INTERVALX * 2 + GuiConfig.SEARCH_MODE_TRAY_WIDTH,
            y=0, width=GuiConfig.SEARCH_BUTTON_WIDTH, height=GuiConfig.SEARCH_BUTTON_HEIGHT,
            anchor=NW
        )

        self.searchModeTray = Frame(self.searchBar)
        self.searchModeTray.place( x=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=0, width=GuiConfig.SEARCH_MODE_TRAY_WIDTH, height=GuiConfig.SEARCH_ENTRY_HEIGHT,
            anchor=NW
        )

        self.searchModeIdx = IntVar()

        self.smTitle = Radiobutton(self.searchModeTray, text="제목", font=GuiConfig.searchModeFont,
            variable=self.searchModeIdx, value=Board.SEARCH_MODE_TITLE
        )
        self.smTitle.pack(side=LEFT)

        self.smAuthor = Radiobutton(self.searchModeTray, text="저자", font=GuiConfig.searchModeFont,
            variable=self.searchModeIdx, value=Board.SEARCH_MODE_AUTHOR
        )
        self.smAuthor.pack(side=LEFT)

        self.smJournal = Radiobutton(self.searchModeTray, text="학술지", font=GuiConfig.searchModeFont,
            variable=self.searchModeIdx, value=Board.SEARCH_MODE_JOURNAL
        )
        self.smJournal.pack(side=LEFT)

        self.smInstitution = Radiobutton(self.searchModeTray, text="기관", font=GuiConfig.searchModeFont,
            variable=self.searchModeIdx, value=Board.SEARCH_MODE_INSTITUTION
        )
        self.smInstitution.pack(side=LEFT)

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
            y=GuiConfig.SEARCH_RESULT_HEIGHT + GuiConfig.SEARCH_RESULT_TRAY_PADDINGY,
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
        if self.searchModeIdx.get() == Board.SEARCH_MODE_TITLE:
            logSearchMode = self.mainGUI.logTab.TITLE_MODE
        elif self.searchModeIdx.get() == Board.SEARCH_MODE_AUTHOR:
            logSearchMode = self.mainGUI.logTab.AUTHOR_MODE
        elif self.searchModeIdx.get() == Board.SEARCH_MODE_JOURNAL:
            logSearchMode = self.mainGUI.logTab.JOURNAL_MODE
        elif self.searchModeIdx.get() == Board.SEARCH_MODE_INSTITUTION:
            logSearchMode = self.mainGUI.logTab.INSTITUTION_MODE

        def task():
            self.mainGUI.logTab.logSearch(self.searchStr.get(), logSearchMode)
            self.onLoading()
            self.board.search(self.searchStr.get(), self.searchModeIdx.get())
            self.trayBasePage = 1

        def onCompletion(result):
            self.onLoaded()
            self.update()

        Loading(self.master, task, onCompletion)

    def update(self):
        for widgets in self.resultList.winfo_children():
            widgets.destroy()

        for widgets in self.pageTray.winfo_children():
            widgets.destroy()

        self.curRecords = []

        for i in range( min( Board.RECORD_CNT_IN_A_PAGE,
            self.board.length() - (self.board.curPage() - 1) * Board.RECORD_CNT_IN_A_PAGE
        ) ):
            self.curRecords.append(
                Record(self.board.get(i), self.resultList)
            )
            self.curRecords[-1].grid(i, 0)
            self.resultList.grid_rowconfigure(i, weight=1)
        self.resultList.grid_columnconfigure(0, weight=1)

        trayLen = min( self.board.length() // Board.RECORD_CNT_IN_A_PAGE + 1,
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

        for i in range(trayLen, Board.PAGE_CNT_IN_A_TRAY):
            self.pageTrayButtons[i] = None

        Button( self.pageTray, text=">", font=GuiConfig.cFont,
            command=self.nextPage
        ).grid(row=0, column=trayLen+1)
        self.pageTray.grid_columnconfigure(trayLen+1, weight=1)

        idx = (self.board.pageNum - 1) % Board.PAGE_CNT_IN_A_TRAY
        
        if self.pageTrayButtons[idx] is not None:
            self.pageTrayButtons[idx]['bg'] = 'light gray'
            
    def selectPage(self, i):
        self.board.selectPage(i)
        self.update()

    def nextPage(self):
        def task():
            self.onLoading()
            return self.board.nextPage()

        def onCompletion(result):
            self.onLoaded()

            if not result:
                return

            if (self.board.pageNum - 1) % Board.PAGE_CNT_IN_A_TRAY == 0:
                self.trayBasePage += Board.PAGE_CNT_IN_A_TRAY
            self.update()

        Loading(self.master, task, onCompletion)

    def prevPage(self):
        self.board.prevPage()

        if self.board.pageNum % Board.PAGE_CNT_IN_A_TRAY == 0:
            self.trayBasePage -= Board.PAGE_CNT_IN_A_TRAY

        self.update()

    def view(self):
        def task():
            self.onLoading()
        
            item = self.resultList.focus_get()
            if not isinstance(item, Text):
                return
            
            for rec in self.curRecords:
                if rec.owns(item):
                    self.mainGUI.viewTab.setPaper(rec.paper)

            self.mainGUI.logTab.logView(rec.paper.title, rec.paper.authors, rec.paper.year)

        def onCompletion(result):
            self.onLoaded()
            self.mainGUI.viewTab.show(self)

        Loading(self.master, task, onCompletion)

    def onLoading(self):
        # disable all buttons
        self.searchButton['state'] = 'disabled'
        self.viewButton['state'] = 'disabled'

        for button in self.pageTrayButtons:
            if button is not None:
                button['state'] = 'disabled'

    
    def onLoaded(self):
        # enable all buttons
        self.searchButton['state'] = 'normal'
        self.viewButton['state'] = 'normal'
        for button in self.pageTrayButtons:
            if button is not None:
                button['state'] = 'normal'