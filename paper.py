class Paper:
    def __init__(self, title, author, year, school=None, doi=None, url=None, abstract=None, citationCnt=None):
        self.title = title
        self.author = author
        self.year = year
        self.school = school
        self.doi = doi
        self.url = url
        self.abstract = abstract
        self.citationCnt = citationCnt

        self.hasBookmark = False
        self.hasMemo = False

    def updateWithMemos(self, memos):
        for memo in memos:
            if memo.paper == self:
                self.setHasMemo()
                break

    def updateWithBookmarks(self, bookmarks):
        for bookmark in bookmarks:
            if bookmark.paper == self:
                self.setHasBookmark()
                break

    def setHasBookmark(self):
        self.hasBookmark = True

    def setHasMemo(self):
        self.hasMemo = True

    def __eq__(self, value) -> bool:
        if self.doi is not None and value.doi is not None:
            return self.doi == value.doi
        
        return self.title == value.title and self.author == value.author and self.year == value.year