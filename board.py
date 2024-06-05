from paper import Paper
from xmlParsing import PageParser
import papery

from tkinter import *
from tkinter import messagebox
import GuiConfig

class Board:
    PAGE_CNT_IN_A_TRAY = 10
    PAGE_CNT_IN_A_SEARCH = 30
    RECORD_CNT_IN_A_PAGE = 10
    SEARCH_UNIT = 100   # must be a multiple of 100
    SEARCH_MODE_TITLE = 0
    SEARCH_MODE_AUTHOR = 1
    SEARCH_MODE_JOURNAL = 2
    SEARCH_MODE_INSTITUTION = 3

    def __init__(self):
        self.papers = []
        self.pageNum = 1
        self.searchStr = ''

    def search(self, searchStr, searchMode=SEARCH_MODE_TITLE):
        self.searchRange(searchStr, searchMode, 0,
            Board.PAGE_CNT_IN_A_SEARCH * Board.RECORD_CNT_IN_A_PAGE - 1
        )

    def length(self):
        return len(self.papers)

    # [start, end] is an 0-based inclusive range of indices
    # remote page referes to the XML's page
    def searchRange(self, searchStr, searchMode, start, end):
        self.searchStr = searchStr

        remotePageStart = start // Board.SEARCH_UNIT + 1
        remotePageEnd = end // Board.SEARCH_UNIT + 1

        if searchMode == Board.SEARCH_MODE_TITLE:
            searchMode = PageParser.TITLE_MODE
        elif searchMode == Board.SEARCH_MODE_AUTHOR:
            searchMode = PageParser.AUTHOR_MODE
        elif searchMode == Board.SEARCH_MODE_JOURNAL:
            searchMode = PageParser.JOURNAL_MODE
        elif searchMode == Board.SEARCH_MODE_INSTITUTION:
            searchMode = PageParser.INSTITUTION_MODE
        else:
            raise ValueError('invalid search mode')

        parseResults = PageParser( searchStr, searchMode, remotePageStart,
            Board.SEARCH_UNIT * (remotePageEnd - remotePageStart + 1)
        ).searchAndParse()

        for parseResult in parseResults:
            self.papers.append( Paper() )
            parseResult.reflect(self.papers[-1])

    def selectPage(self, pageNum):
        self.pageNum = pageNum

    def nextPage(self):
        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            self.searchRange(self.searchStr, self.pageNum * Board.RECORD_CNT_IN_A_PAGE,
                (self.pageNum + Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE - 1
            )

        if self.length() <= self.pageNum * Board.RECORD_CNT_IN_A_PAGE:
            messagebox.showinfo('알림', '마지막 페이지입니다.')
            return

        self.pageNum += 1

    def prevPage(self):
        self.pageNum -= 1
        if self.pageNum < 1:
            self.pageNum = 1

    def get(self, index):
        if not (0 <= index < Board.RECORD_CNT_IN_A_PAGE):
            raise ValueError('index out of range')

        return self.papers[ (self.pageNum-1) * Board.RECORD_CNT_IN_A_PAGE + index ]

class Record:
    def __init__(self, paper, master):
        self.paper = paper
        self.master = master
        self.widget = Text(self.master, font = GuiConfig.cFont, wrap=WORD)

        recordStr = ' | '.join(
            [paper.title, ', '.join(paper.authors), paper.year]
        )
        self.widget.insert(END, recordStr)

        self.widget.bind("<FocusIn>", self.on_focus_in)
        self.widget.bind("<FocusOut>", self.on_focus_out)

        self.widget.config(state='disabled')

    def grid(self, i, j):
        self.widget.grid(row=i, column=j, sticky='ew')

    def on_focus_in(self, event):
        self.widget.config(bg="light blue", fg='white')

    def on_focus_out(self, event):
        self.widget.config(bg="white", fg='black')

    def owns(self, widget):
        return self.widget == widget

if __name__ == '__main__':
    board = Board()
    board.search('컴퓨터')
    print(board.get(0).title)   # sample0
    board.nextPage()
    print(board.get(0).title)   # sample10
    board.nextPage()
    print(board.get(0).title)   # sample20
    board.prevPage()
    print(board.get(0).title)   # sample10
    board.prevPage()
    print(board.get(0).title)   # sample0
    board.prevPage()
    print(board.get(0).title)   # sample0
    board.selectPage(1)
    print(board.get(0).title)   # sample0
    board.selectPage(2)
    print(board.get(0).title)   # sample10
    board.selectPage(10)
    print(board.get(0).title)   # sample90
    board.nextPage()
    print(board.get(0).title)   # sample100
    board.nextPage()
    print(board.get(0).title)   # sample110
    board.prevPage()
    print(board.get(0).title)   # sample100
    board.prevPage()
    print(board.get(0).title)   # sample90
    board.prevPage()
    print(board.get(0).title)   # sample80