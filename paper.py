class Paper:
    def __init__( self, title = None, authors = None, year = None,
        authorInsts = None, journal = None, volume = None, issue = None,
        doi = None, url = None, abstract = None, citationCnt = None,
        keywords = None, refs = None, institution = None
    ):
        self.title = title
        self.authors = authors
        self.year = year
        self.authorInsts = authorInsts
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.doi = doi
        self.url = url
        self.abstract = abstract
        self.citationCnt = citationCnt
        self.keywords = keywords
        self.refs = refs
        self.institution = institution

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
        
        return self.title == value.title and self.authors == value.authors and self.year == value.year