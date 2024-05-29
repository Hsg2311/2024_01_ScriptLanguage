from paper import Paper
from xmlParsing import xmlParsing
import papery

class Board:
    PAGE_CNT_IN_A_SEARCH = 10
    RECORD_CNT_IN_A_PAGE = 10
    SEARCH_UNIT = 100   # must be a multiple of 100

    def __init__(self):
        self.papers = []
        self.pageNum = 1
        self.searchStr = ''

    def search(self, searchStr):
        self.searchRange(searchStr, 0, Board.PAGE_CNT_IN_A_SEARCH * Board.RECORD_CNT_IN_A_PAGE - 1)

    # [start, end] is an 0-based inclusive range of indices
    # remote page referes to the XML's page
    def searchRange(self, searchStr, start, end):
        self.searchStr = searchStr

        remotePageStart = start // Board.SEARCH_UNIT + 1
        remotePageEnd = end // Board.SEARCH_UNIT + 1

        print('searching...')
        self.papers = []
        parser = xmlParsing(papery.KEY, searchStr, papery.paperDataUrl,
            remotePageStart, Board.SEARCH_UNIT * (remotePageEnd - remotePageStart + 1)
        )
        parser.parse()
        self.papers = parser.papers[:]

    def selectPage(self, pageNum):
        self.pageNum = pageNum

    def nextPage(self):
        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            self.searchRange(self.searchStr, self.pageNum * Board.RECORD_CNT_IN_A_PAGE,
                (self.pageNum + Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE - 1
            )

        self.pageNum += 1

    def prevPage(self):
        self.pageNum -= 1
        if self.pageNum < 1:
            self.pageNum = 1

        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            self.searchRange(self.searchStr, (self.pageNum - Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE,
                self.pageNum * Board.RECORD_CNT_IN_A_PAGE - 1
            )

    def get(self, index):
        if not (0 <= index < Board.RECORD_CNT_IN_A_PAGE):
            raise ValueError('index out of range')

        return self.papers[ ((self.pageNum-1) % Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE + index ]


if __name__ == '__main__':
    board = Board()
    board.search('컴퓨터')
    print(board.get(0)['Title'])   # sample0
    board.nextPage()
    print(board.get(0)['Title'])   # sample10
    board.nextPage()
    print(board.get(0)['Title'])   # sample20
    board.prevPage()
    print(board.get(0)['Title'])   # sample10
    board.prevPage()
    print(board.get(0)['Title'])   # sample0
    board.prevPage()
    print(board.get(0)['Title'])   # sample0
    board.selectPage(1)
    print(board.get(0)['Title'])   # sample0
    board.selectPage(2)
    print(board.get(0)['Title'])   # sample10
    board.selectPage(10)
    print(board.get(0)['Title'])   # sample90
    board.nextPage()
    print(board.get(0)['Title'])   # sample100
    board.nextPage()
    print(board.get(0)['Title'])   # sample110
    board.prevPage()
    print(board.get(0)['Title'])   # sample100
    board.prevPage()
    print(board.get(0)['Title'])   # sample90
    board.prevPage()
    print(board.get(0)['Title'])   # sample80