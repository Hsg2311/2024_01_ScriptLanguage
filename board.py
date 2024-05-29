from paper import Paper

class Board:
    PAGE_CNT_IN_A_SEARCH = 10
    RECORD_CNT_IN_A_PAGE = 10
    SEARCH_UNIT = 50

    def __init__(self):
        self.papers = []
        self.pageNum = 1

    def search(self, searchStr):
        self.searchRange(searchStr, 0, Board.PAGE_CNT_IN_A_SEARCH * Board.RECORD_CNT_IN_A_PAGE - 1)

    # [start, end] is an 0-based inclusive range of indices
    # remote page referes to the XML's page
    def searchRange(self, searchStr, start, end):
        # temporary implementation
        remotePageStart = start // Board.SEARCH_UNIT + 1
        remotePageEnd = end // Board.SEARCH_UNIT + 1

        self.papers = []

        for remotePageNum in range(remotePageStart, remotePageEnd+1):
            self.papers.extend( [Paper('sample'+str(i), 'jang', '2024') for i in range(
                Board.SEARCH_UNIT * (remotePageNum-1),
                Board.SEARCH_UNIT * remotePageNum
            ) ] )

    def selectPage(self, pageNum):
        self.pageNum = pageNum

    def nextPage(self):
        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            print(len(self.papers))
            self.searchRange('sample', self.pageNum * Board.RECORD_CNT_IN_A_PAGE,
                (self.pageNum + Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE - 1
            )
            print(len(self.papers))

        self.pageNum += 1

    def prevPage(self):
        self.pageNum -= 1
        if self.pageNum < 1:
            self.pageNum = 1

        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            print(len(self.papers))
            self.searchRange('sample', (self.pageNum - Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE,
                self.pageNum * Board.RECORD_CNT_IN_A_PAGE - 1
            )
            print(len(self.papers))

    def get(self, index):
        if not (0 <= index < Board.RECORD_CNT_IN_A_PAGE):
            raise ValueError('index out of range')

        return self.papers[ ((self.pageNum-1) % Board.PAGE_CNT_IN_A_SEARCH) * Board.RECORD_CNT_IN_A_PAGE + index ]


if __name__ == '__main__':
    board = Board()
    board.search('sample')
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