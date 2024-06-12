from tkinter import *
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import ttk
from tkinter import simpledialog

from paper import Paper
from board import Board, Record

from Loading import Loading

import GuiConfig

import bookmark
from BookmarkRoot import root

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
            width=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.SEARCH_VIEW_BUTTON_WIDTH + GuiConfig.WIDGET_INTERVALX + 100,
            height=GuiConfig.SEARCH_RESULT_HEIGHT + GuiConfig.WIDGET_INTERVALY + GuiConfig.SEARCH_RESULT_TRAY_HEIGHT,
            anchor=NW
        )

        self.resultList = Frame(self.result, bg='white')
        self.resultList.place( x=0, y=0,
            width=GuiConfig.SEARCH_RESULT_WIDTH, height=GuiConfig.SEARCH_RESULT_HEIGHT,
            anchor=NW
        )

        self.resultListBgImg = PhotoImage(file='res/bg_image.png')
        self.labelBgImg = Label(self.resultList, image=self.resultListBgImg)
        self.labelBgImg.pack()

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

        self.sourceIdx = IntVar()
        self.sourceIdx.set(0)

        self.sourceKCI = Radiobutton(self.result, text="KCI", font=GuiConfig.cFont,
            variable=self.sourceIdx, value=0
        )
        self.sourceKCI.place( x=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=GuiConfig.SEARCH_VIEW_BUTTON_PADDINGY + GuiConfig.SEARCH_VIEW_BUTTON_HEIGHT + 100
                + GuiConfig.WIDGET_INTERVALY,
            anchor=NW
        )

        self.sourceScopus = Radiobutton(self.result, text="Scopus", font=GuiConfig.cFont,
            variable=self.sourceIdx, value=1
        )
        self.sourceScopus.place( x=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=GuiConfig.SEARCH_VIEW_BUTTON_PADDINGY + GuiConfig.SEARCH_VIEW_BUTTON_HEIGHT
                + GuiConfig.WIDGET_INTERVALY + GuiConfig.SEARCH_BUTTON_HEIGHT + 100,
            anchor=NW
        )

        self.StarImage = PhotoImage(file='노란 별.png')
        self.bmButton = Button(self.result, image=self.StarImage, command=self.bookmark)
        self.bmButton.place( x=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.WIDGET_INTERVALX, y=100, width=50, height=50 )

    def bookmark(self):
        item = self.resultList.focus_get()
        if not isinstance(item, Text):
            return
        
        for rec in self.curRecords:
            if rec.owns(item):
                self.selected_paper = rec.paper

                new_window = Toplevel(self.mainGUI.master)
                new_window.title('북마크')
                new_window.geometry('360x330')

                new_window_frame = Frame(new_window, bg='white')
                new_window_frame.pack(expand=True, fill='both')

                style = ttk.Style()
                style.configure('Treeview', font=('Helvetica', 14), rowheight=30)

                self.tree = ttk.Treeview(new_window_frame)
                self.tree.place(x=0, y=0, width=200, height=300)

                vScrollbar = ttk.Scrollbar(new_window_frame, orient='vertical', command=self.tree.yview)
                self.tree.configure(yscrollcommand=vScrollbar.set)
                vScrollbar.place(x=200, y=1, width=20, height=300)

                hScrollbar = ttk.Scrollbar(new_window_frame, orient='horizontal', command=self.tree.xview)
                self.tree.configure(xscrollcommand=hScrollbar.set)
                hScrollbar.place(x=1, y=300, width=199, height=20)

                self.updateTreeview(root)

                addButton = Button(new_window_frame, text='카테고리 추가', command=self.addCategory)
                addButton.place(x=225, y=0, width=90, height=30)
                delButton = Button(new_window_frame, text='카테고리 삭제', command=self.delCategory)
                delButton.place(x=225, y=50, width=90, height=30)
                ncButton = Button(new_window_frame, text='카테고리 이름 수정', command=self.changeItemName)
                ncButton.place(x=225, y=100, width=120, height=30)
                
                addPaperButton = Button(new_window_frame, text='+', command=self.addPaper)
                addPaperButton.place(x=225, y=150, width=50, height=30)

                expandAllItems(self.tree)

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
            if self.sourceIdx.get() == 0:
                src = Board.SEARCH_SOURCE_KCI
            else:
                src = Board.SEARCH_SOURCE_SCOPUS

            self.mainGUI.logTab.logSearch(self.searchStr.get(), logSearchMode, src)
            self.onLoading()

            if self.sourceIdx.get() == 0:
                src = Board.SEARCH_SOURCE_KCI
            else:
                src = Board.SEARCH_SOURCE_SCOPUS

            self.board.search(self.searchStr.get(), self.searchModeIdx.get(), src)
            self.trayBasePage = 1

        def onCompletion(result):
            self.labelBgImg.destroy()

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
                    if self.sourceIdx.get() == 0:
                        src = Board.SEARCH_SOURCE_KCI
                    else:
                        src = Board.SEARCH_SOURCE_SCOPUS
                    self.mainGUI.viewTab.setPaper(rec.paper, src)
                    break

            if self.searchModeIdx.get() == Board.SEARCH_MODE_TITLE:
                logSearchMode = self.mainGUI.logTab.TITLE_MODE
            elif self.searchModeIdx.get() == Board.SEARCH_MODE_AUTHOR:
                logSearchMode = self.mainGUI.logTab.AUTHOR_MODE
            elif self.searchModeIdx.get() == Board.SEARCH_MODE_JOURNAL:
                logSearchMode = self.mainGUI.logTab.JOURNAL_MODE
            elif self.searchModeIdx.get() == Board.SEARCH_MODE_INSTITUTION:
                logSearchMode = self.mainGUI.logTab.INSTITUTION_MODE
            else:
                raise ValueError("Invalid search mode")

            if self.sourceIdx.get() == 0:
                src = Board.SEARCH_SOURCE_KCI
            else:
                src = Board.SEARCH_SOURCE_SCOPUS

            self.mainGUI.logTab.logView(rec.paper.title, rec.paper.authors, rec.paper.year, rec.paper.articleID,
                self.searchStr.get(), logSearchMode, src
            )
            
        def onCompletion(result):
            self.onLoaded()
            self.mainGUI.viewTab.show(self)

        Loading(self.master, task, onCompletion)

    def insertNode(self, node, parent = None):
        global root
        if isinstance(node, bookmark.Category):
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.name, iid=node.name)
                parent.insert(bookmark.Category(node.name))
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper.title, "end", text=node.name, iid=node.name)
                parent.insert(bookmark.Category(node.name))
            else:
                self.tree.insert("", "end", text=node.name, iid=node.name)
                root.insert(bookmark.Category(node.name))
        else:
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.paper.title, iid=node.paper.title)
                parent.insert(node)
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper.title, "end", text=node.paper.title, iid=node.paper.title)
            else:
                self.tree.insert("", "end", text=node.paper.title, iid=node.paper.title)

        for child in node.children:
            self.insertNode(child, node)

    def addCategory(self):
        global root

        name = simpledialog.askstring("카테고리 이름 설정", "카테고리 이름을 입력하세요:")
        if self.findCategory(root, name):
            messagebox.showinfo('알림', '이미 존재하는 카테고리입니다.')
            return
        
        c = bookmark.Category(name)
        self.insertNode(c, root)

        self.updateSearchTab()

    def delCategory(self):
        global root

        selected_item = self.tree.selection()
        if selected_item:
            self.findCategory(root, selected_item[0]).destroy()
            self.tree.delete(selected_item)

        self.updateSearchTab()

    def changeItemName(self):
        selected_item = self.tree.selection()
        if selected_item:  # 선택된 아이템이 있는지 확인
            new_name = simpledialog.askstring("카테고리 이름 변경", "새 이름을 입력하세요:")
            if new_name:  # 사용자가 이름을 입력하고 'OK'를 누른 경우
                self.findCategory(root, selected_item[0]).name = new_name
                self.tree.item(selected_item[0], text=new_name)  # 선택된 아이템의 이름을 새로운 이름으로 변경

        self.updateSearchTab()

    def updateTreeview(self, node, parent = None):
        if isinstance(node, bookmark.Root):
            pass
        elif isinstance(node, bookmark.Category):
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.name, iid=node.name)
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper.title, "end", text=node.name, iid=node.name)
            else:
                self.tree.insert("", "end", text=node.name, iid=node.name)
        else:
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.paper.title, iid=node.paper.title)
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper.title, "end", text=node.paper.title, iid=node.paper.title)
            else:
                self.tree.insert("", "end", text=node.paper.title, iid=node.paper.title)

        for child in node.children:
            self.updateTreeview(child, node)

    def clearTreeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item) 

    def updateSearchTab(self):
        global root

        self.clearTreeview()
        self.updateTreeview(root)

    def addPaper(self):
        global root
        s = ''.join(self.tree.selection())
        c = self.findCategory(root, s)

        if c is not None:
            bi = bookmark.BookmarkItem(self.selected_paper)
            self.insertNode(bi, c)

        self.updateSearchTab()
        
    def findCategory(self, node, name):
        for child in node.children:
            if isinstance(child, bookmark.Category) and child.owns(name):
                return child
        for child in node.children:
            tmp = self.findCategory(child, name)
            if tmp is not None:
                return tmp
            
        return None
      
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

def expandAllItems(tree, item=''):
    for child in tree.get_children(item):
        tree.item(child, open=True)
        expandAllItems(tree, child)