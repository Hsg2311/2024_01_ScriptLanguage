from paper import Paper

class Board:
    PAGE_CNT_IN_A_SEARCH = 10
    RECORD_CNT_IN_A_PAGE = 10
    SEARCH_UNIT = 100

    def __init__(self):
        self.papers = []
        self.pageNum = 1

    def search(self, searchStr):
        self.searchRemotePage(searchStr, 1)

    # remote page referes to the XML's page
    def searchRemotePage(self, searchStr, remotePageNum):
        # temporary implementation
        self.papers=[Paper('sample'+str(i), 'jang', '2024') for i in range(
            ( Board.PAGE_CNT_IN_A_SEARCH*Board.RECORD_CNT_IN_A_PAGE ) * remotePageNum
        )]

    def selectPage(self, pageNum):
        self.pageNum = pageNum

    def nextPage(self):
        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            self.searchRemotePage('sample',
                self.pageNum * Board.RECORD_CNT_IN_A_PAGE // Board.SEARCH_UNIT + 1                      
            )

        self.pageNum += 1

    def prevPage(self):
        self.pageNum = max(self.pageNum - 1, 1)

        if self.pageNum % Board.PAGE_CNT_IN_A_SEARCH == 0:
            self.searchRemotePage('sample',
                self.pageNum * Board.RECORD_CNT_IN_A_PAGE // Board.SEARCH_UNIT + 1
            )

    def get(self, index):
        if not (0 <= index < Board.RECORD_CNT_IN_A_PAGE):
            raise ValueError('index out of range')

        return self.papers[ (self.pageNum-1)*Board.RECORD_CNT_IN_A_PAGE + index ]


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