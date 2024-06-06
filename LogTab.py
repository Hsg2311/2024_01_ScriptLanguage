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
        
        self.frame = Frame(self.master)
        self.frame.pack()
        
        self.dummyFrame = Frame(self.frame)
        self.dummyFrame.pack(pady=GuiConfig.LOG_PADDINGY // 2)

        self.logFrame = Frame(self.frame)
        self.logFrame.pack(side=LEFT)

        self.searchLogFrame = Frame(self.logFrame)
        self.searchLogFrame.pack()
        Label(self.searchLogFrame, text="검색 기록", font=GuiConfig.cFont).pack()
        self.searchLogCanvas = Canvas(self.searchLogFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_SEARCHLOG_HEIGHT, bg="red"
        )
        self.searchLogCanvas.pack(padx=GuiConfig.WIDGET_INTERVALX)

        self.viewLogFrame = Frame(self.logFrame)
        self.viewLogFrame.pack(pady=GuiConfig.WIDGET_INTERVALY)
        Label(self.viewLogFrame, text="열람 기록", font=GuiConfig.cFont).pack()
        self.viewLogCanvas = Canvas(self.viewLogFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_VIEWLOG_HEIGHT, bg="blue"
        )
        self.viewLogCanvas.pack(padx=GuiConfig.WIDGET_INTERVALX)

        self.viewButtonFrame = Frame(self.frame)
        self.viewButtonFrame.pack(side=LEFT, padx=GuiConfig.WIDGET_INTERVALX,
            fill=Y, expand=True
        )

        self.viewButton = Button(self.viewButtonFrame, text="View",
            width=GuiConfig.LOG_VIEW_BUTTON_WIDTH, height=5,
            command=self.click
        )
        self.viewButton.pack(pady=GuiConfig.LOG_VIEW_BUTTON_PADDINGY, side=TOP, anchor=N)

        self.buildSearchLog()
        self.buildViewLog()
    
    def logSearch(self, searchStr, searchMode):
        spam.logSearch(searchStr, searchMode)

    def logView(self, title, authors, year):
        spam.logView(title, ', '.join(authors), int(year))

    def buildSearchLog(self):
        if os.path.exists('log/search.log'):
            spam.loadSearchLog('log/search.log')

    def buildViewLog(self):
        if os.path.exists('log/view.log'):
            spam.loadViewLog('log/view.log')

    def saveSearchLog(self):
        spam.saveSearchLog('log/search.log')

    def saveViewLog(self):
        spam.saveViewLog('log/view.log')

    def save(self):
        self.saveSearchLog()
        self.saveViewLog()

    def click(self):
        messagebox.showinfo("Log Tab", "You clicked the button in the Log Tab")