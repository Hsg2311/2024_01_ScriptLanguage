from tkinter import *
from tkinter import messagebox

import GuiConfig
import os
import spam

class LogTab:
    TITLE_MODE = "Title"
    AUTHOR_MODE = "Author"
    JOURNAL_MODE = "Journal"
    INSTITUTION_MODE = "Institution"

    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.mainGUI.saveCollector.add_saver(self)
        self.master = mainGUI.master
    
        self.searchLogTxts = []
        self.viewLogTxts = []

        self.__initWidgets()

        self.buildSearchLog()
        self.buildViewLog()
    
    def __initWidgets(self):
        self.frame = Frame(self.master)
        self.frame.pack()
        
        self.dummyFrame = Frame(self.frame)
        self.dummyFrame.pack(pady=GuiConfig.LOG_PADDINGY // 2)

        self.logFrame = Frame(self.frame)
        self.logFrame.pack(side=LEFT)

        searchCanvasFrame = Frame(self.logFrame)
        searchCanvasFrame.pack()
        Label(searchCanvasFrame, text="검색 기록", font=GuiConfig.cFont).pack()
        self.searchLogCanvas = Canvas(searchCanvasFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_SEARCHLOG_HEIGHT, bg="red"
        )
        self.searchLogCanvas.pack(padx=GuiConfig.WIDGET_INTERVALX)
        self.searchLogFrame = Frame(self.searchLogCanvas)
        self.searchLogFrame.pack(fill=BOTH, expand=True)

        viewCanvasFrame = Frame(self.logFrame)
        viewCanvasFrame.pack(pady=GuiConfig.WIDGET_INTERVALY)
        Label(viewCanvasFrame, text="열람 기록", font=GuiConfig.cFont).pack()
        self.viewLogCanvas = Canvas(viewCanvasFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_VIEWLOG_HEIGHT, bg="blue"
        )
        self.viewLogCanvas.pack(padx=GuiConfig.WIDGET_INTERVALX)
        self.viewLogFrame = Frame(self.viewLogCanvas)
        self.viewLogFrame.pack(fill=BOTH, expand=True)

        self.viewButtonFrame = Frame(self.frame)
        self.viewButtonFrame.pack(side=LEFT, padx=GuiConfig.WIDGET_INTERVALX,
            fill=Y, expand=True
        )

        self.viewButton = Button(self.viewButtonFrame, text="View",
            width=GuiConfig.LOG_VIEW_BUTTON_WIDTH, height=5,
            command=self.click
        )
        self.viewButton.pack(pady=GuiConfig.LOG_VIEW_BUTTON_PADDINGY, side=TOP, anchor=N)

    def logSearch(self, searchStr, searchMode):
        spam.logSearch(searchStr, searchMode)

    def logView(self, title, authors, year):
        spam.logView(title, ', '.join(authors), int(year))

    def buildSearchLog(self):
        if os.path.exists('log/search.log'):
            spam.loadSearchLog('log/search.log')

        for i in range(spam.searchLogSize()):
            response = spam.getSearchLog(i)
            s = response['timeStamp'] + '|' + response['type'] \
                + '| ' + response['keyword']
            self.searchLogTxts.append(Text(self.searchLogFrame, height=1))
            self.searchLogTxts[-1].insert(END, s)
            self.searchLogTxts[-1].pack(fill=X, expand=True)

            # it must be called to get the height of the text widget
            self.master.update_idletasks()

            height = self.master.call((self.searchLogTxts[-1], "count", "-update", "-displaylines", "1.0", "end"))
            self.searchLogTxts[-1].config(height=height)
            self.searchLogTxts[-1]['state'] = 'disabled'
            

    def buildViewLog(self):
        if os.path.exists('log/view.log'):
            spam.loadViewLog('log/view.log')

        for i in range(spam.viewLogSize()):
            response = spam.getViewLog(i)
            s = response['timeStamp'] + '| ' + response['author'] \
                + ' | ' + str(response['year']) + ' | ' + response['title']
            self.viewLogTxts.append(Text(self.viewLogFrame, height=1))
            self.viewLogTxts[-1].insert(END, s)
            self.viewLogTxts[-1].pack(fill=X, expand=True)

            # it must be called to get the height of the text widget
            self.master.update_idletasks()

            height = self.master.call((self.viewLogTxts[-1], "count", "-update", "-displaylines", "1.0", "end"))
            self.viewLogTxts[-1].config(height=height)
            self.viewLogTxts[-1]['state'] = 'disabled'

    def saveSearchLog(self):
        spam.saveSearchLog('log/search.log')

    def saveViewLog(self):
        spam.saveViewLog('log/view.log')

    def save(self):
        self.saveSearchLog()
        self.saveViewLog()

    def click(self):
        messagebox.showinfo("Log Tab", "You clicked the button in the Log Tab")