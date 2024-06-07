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
        self.searchLogCanvas.pack(side=LEFT, padx=GuiConfig.WIDGET_INTERVALX)
        self.searchLogFrame = Frame(self.searchLogCanvas)
        self.searchLogFrame.pack(fill=BOTH, expand=True)
        self.searchLogCanvas.create_window((0, 0), window=self.searchLogFrame, anchor=NW)

        self.searchScroll = Scrollbar(searchCanvasFrame, orient=VERTICAL, command=self.searchLogCanvas.yview)
        self.searchLogCanvas.config(yscrollcommand=self.searchScroll.set)
        self.searchScroll.pack(side=LEFT, fill=Y, expand=True)

        viewCanvasFrame = Frame(self.logFrame)
        viewCanvasFrame.pack(pady=GuiConfig.WIDGET_INTERVALY)
        Label(viewCanvasFrame, text="열람 기록", font=GuiConfig.cFont).pack()
        self.viewLogCanvas = Canvas(viewCanvasFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_VIEWLOG_HEIGHT, bg="blue"
        )
        self.viewLogCanvas.pack(side=LEFT, padx=GuiConfig.WIDGET_INTERVALX)
        self.viewLogFrame = Frame(self.viewLogCanvas)
        self.viewLogFrame.pack(fill=BOTH, expand=True)
        self.viewLogCanvas.create_window((0, 0), window=self.viewLogFrame, anchor=NW)

        self.viewScroll = Scrollbar(viewCanvasFrame, orient=VERTICAL, command=self.viewLogCanvas.yview)
        self.viewLogCanvas.config(yscrollcommand=self.viewScroll.set)
        self.viewScroll.pack(side=LEFT, fill=Y, expand=True)

        self.viewButtonFrame = Frame(self.frame)
        self.viewButtonFrame.pack(side=LEFT, padx=GuiConfig.WIDGET_INTERVALX,
            fill=Y, expand=True
        )

        self.viewButton = Button(self.viewButtonFrame, text="View",
            width=GuiConfig.LOG_VIEW_BUTTON_WIDTH, height=5,
            command=self.click
        )
        self.viewButton.pack(pady=GuiConfig.LOG_VIEW_BUTTON_PADDINGY, side=TOP, anchor=N)

    def __searchLogToStr(self, log):
        return log['timeStamp'] + '|' + log['type'] + '| ' + log['keyword']
    
    def __viewLogToStr(self, log):
        return log['timeStamp'] + '| ' + log['author'] + ' | ' + str(log['year']) + ' | ' + log['title']
    
    def __appendSearchLogStr(self, s):
        self.searchLogTxts.append(Text(self.searchLogFrame, height=1,
            wrap=WORD, width=GuiConfig.LOG_LOG_TEXT_WIDTH
        ))
        self.searchLogTxts[-1].insert(END, s)
        self.searchLogTxts[-1].pack(fill=X, expand=True)

        # it must be called to get the height of the text widget
        self.master.update_idletasks()

        height = self.master.call((self.searchLogTxts[-1], "count", "-update", "-displaylines", "1.0", "end"))
        self.searchLogTxts[-1].config(height=height)
        self.searchLogTxts[-1]['state'] = 'disabled'

    def __appendViewLogStr(self, s):
        self.viewLogTxts.append(Text(self.viewLogFrame, height=1,
            wrap=WORD, width=GuiConfig.LOG_LOG_TEXT_WIDTH
        ))
        self.viewLogTxts[-1].insert(END, s)
        self.viewLogTxts[-1].pack(fill=X, expand=True)

        # it must be called to get the height of the text widget
        self.master.update_idletasks()

        height = self.master.call((self.viewLogTxts[-1], "count", "-update", "-displaylines", "1.0", "end"))
        self.viewLogTxts[-1].config(height=height)
        self.viewLogTxts[-1]['state'] = 'disabled'

    def logSearch(self, searchStr, searchMode):
        spam.logSearch(searchStr, searchMode)
        self.__appendSearchLogStr( self.__searchLogToStr(
            spam.getSearchLog(spam.searchLogSize() - 1)
        ) )
        self.adjustScrollbar()

    def logView(self, title, authors, year):
        spam.logView(title, ', '.join(authors), int(year))
        self.__appendViewLogStr( self.__viewLogToStr(
            spam.getViewLog(spam.viewLogSize() - 1)
        ) )
        self.adjustScrollbar()

    def buildSearchLog(self):
        if os.path.exists('log/search.log'):
            spam.loadSearchLog('log/search.log')

        for i in range(spam.searchLogSize()):
            self.__appendSearchLogStr(
                self.__searchLogToStr( spam.getSearchLog(i) )
            )
        self.adjustScrollbar()
            

    def buildViewLog(self):
        if os.path.exists('log/view.log'):
            spam.loadViewLog('log/view.log')

        for i in range(spam.viewLogSize()):
            self.__appendViewLogStr(
                self.__viewLogToStr( spam.getViewLog(i) )
            )
        self.adjustScrollbar()

    def saveSearchLog(self):
        spam.saveSearchLog('log/search.log')

    def saveViewLog(self):
        spam.saveViewLog('log/view.log')

    def save(self):
        self.saveSearchLog()
        self.saveViewLog()

    def adjustScrollbar(self):
        self.searchLogFrame.update()
        self.searchLogCanvas.delete('searchLogFrame')
        self.searchLogCanvas.create_window((0, 0), window=self.searchLogFrame, anchor=NW, tags='searchLogFrame')
        self.searchLogCanvas.config(scrollregion=self.searchLogCanvas.bbox('all'))

        self.viewLogFrame.update()
        self.viewLogCanvas.delete('viewLogFrame')
        self.viewLogCanvas.create_window((0, 0), window=self.viewLogFrame, anchor=NW, tags='viewLogFrame')
        self.viewLogCanvas.config(scrollregion=self.viewLogCanvas.bbox('all'))


    def click(self):
        messagebox.showinfo("Log Tab", "You clicked the button in the Log Tab")