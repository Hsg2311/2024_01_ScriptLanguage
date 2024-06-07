from tkinter import *
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import ttk
from tkinter import simpledialog

from paper import Paper
from board import Board, Record

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
        self.searchBar.place( x=GuiConfig.TABS_PADDINGX, y=GuiConfig.SEARCH_BAR_PADDING_Y,
            width=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.SEARCH_BUTTON_WIDTH + GuiConfig.WIDGET_INTERVALX,
            height=max(GuiConfig.SEARCH_ENTRY_HEIGHT, GuiConfig.SEARCH_BUTTON_HEIGHT) + GuiConfig.WIDGET_INTERVALY,
            anchor=NW
        )

        self.searchStr = StringVar()
        self.searchStr.set("검색어를 입력하세요")
        self.entry = Entry(self.searchBar, textvariable=self.searchStr, font=GuiConfig.cFont)
        self.entry.place( x=GuiConfig.TABS_PADDINGX, y=0,
            width=GuiConfig.SEARCH_ENTRY_WIDTH, height=GuiConfig.SEARCH_ENTRY_HEIGHT,
            anchor=NW
        )

        self.button = Button(self.searchBar, text="검색", font=GuiConfig.cFont, command=self.search)
        self.button.place( x=GuiConfig.SEARCH_ENTRY_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=0, width=GuiConfig.SEARCH_BUTTON_WIDTH, height=GuiConfig.SEARCH_BUTTON_HEIGHT,
            anchor=NW
        )

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

        self.pageTray = Frame(self.result)
        self.pageTray.place( x=(GuiConfig.SEARCH_RESULT_WIDTH - GuiConfig.SEARCH_RESULT_TRAY_WIDTH) // 2,
            y=GuiConfig.SEARCH_RESULT_HEIGHT + GuiConfig.WIDGET_INTERVALY,
            width=GuiConfig.SEARCH_RESULT_TRAY_WIDTH,
            height=GuiConfig.SEARCH_RESULT_TRAY_HEIGHT,
            anchor=NW
        )
        self.pageTrayButtons = [None] * Board.PAGE_CNT_IN_A_TRAY

        self.viewButton = Button(self.result, text="View", font=GuiConfig.cFont, command=self.view)
        self.viewButton.place( x=GuiConfig.SEARCH_RESULT_WIDTH + GuiConfig.WIDGET_INTERVALX + 100,
            y=GuiConfig.SEARCH_VIEW_BUTTON_PADDINGY,
            width=GuiConfig.SEARCH_VIEW_BUTTON_WIDTH, height=GuiConfig.SEARCH_VIEW_BUTTON_HEIGHT,
            anchor=NW                      
        )

        self.StarImage = PhotoImage(file='노란 별.png')
        self.bmButton = Button(self.result, image=self.StarImage, command=self.bookmark)
        self.bmButton.place( x=600, y=100, width=50, height=50 )

    def bookmark(self):
        item = self.resultList.focus_get()
        if not isinstance(item, Text):
            return
        
        for rec in self.curRecords:
            if rec.owns(item):
                new_window = Toplevel(self.mainGUI.master)
                new_window.title('북마크')
                new_window.geometry('330x300')

                new_window_frame = Frame(new_window, bg='white')
                new_window_frame.pack(expand=True, fill='both')

                style = ttk.Style()
                style.configure('Treeview', font=('Helvetica', 14), rowheight=30)

                self.tree = ttk.Treeview(new_window_frame)
                self.tree.place(x=0, y=0, width=200, height=300)

                self.updateTreeview(root)

                addButton = Button(new_window_frame, text='카테고리 추가', command=self.addCategory)
                addButton.place(x=205, y=0, width=90, height=30)
                delButton = Button(new_window_frame, text='카테고리 삭제', command=self.delCategory)
                delButton.place(x=205, y=50, width=90, height=30)
                ncButton = Button(new_window_frame, text='카테고리 이름 수정', command=self.changeItemName)
                ncButton.place(x=205, y=100, width=120, height=30)
                
                addPaperButton = Button(new_window_frame, text='+', command=self.addPaper)
                addPaperButton.place(x=205, y=150, width=50, height=30)

                expandAllItems(self.tree)

    def search(self):
        # self.board.search(self.searchStr.get())

        # temporary implementation
        self.board.loadCache(self.searchStr.get())

        self.update()

    def update(self):
        for widgets in self.resultList.winfo_children():
            widgets.destroy()

        for widgets in self.pageTray.winfo_children():
            widgets.destroy()

        self.curRecords = []

        for i in range(min(Board.RECORD_CNT_IN_A_PAGE, self.board.length())):
            self.curRecords.append(
                Record(self.board.get(i), self.resultList)
            )
            self.curRecords[-1].grid(i, 0)
            self.resultList.grid_rowconfigure(i, weight=1)
        self.resultList.grid_columnconfigure(0, weight=1)

        trayLen = min( self.board.length() // Board.RECORD_CNT_IN_A_PAGE,
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

        Button( self.pageTray, text=">", font=GuiConfig.cFont,
            command=self.nextPage
        ).grid(row=0, column=trayLen+1)
        self.pageTray.grid_columnconfigure(trayLen+1, weight=1)

        self.pageTrayButtons[(self.board.pageNum - 1) % Board.PAGE_CNT_IN_A_TRAY]['bg'] = 'light gray'
            
    def selectPage(self, i):
        self.board.selectPage(i)
        self.update()

    def nextPage(self):
        if self.board.pageNum % Board.PAGE_CNT_IN_A_TRAY == 0:
            self.trayBasePage += Board.PAGE_CNT_IN_A_TRAY

        self.board.nextPage()
        self.update()

    def prevPage(self):
        self.board.prevPage()

        if self.board.pageNum % Board.PAGE_CNT_IN_A_TRAY == 0:
            self.trayBasePage -= Board.PAGE_CNT_IN_A_TRAY

        self.update()

    def view(self):
        item = self.resultList.focus_get()
        if not isinstance(item, Text):
            return
        
        for rec in self.curRecords:
            if rec.owns(item):
                self.mainGUI.viewTab.setPaper(rec.paper)

        self.mainGUI.viewTab.show(self)

    def insertNode(self, node, parent = None):
        global root
        if isinstance(node, bookmark.Category):
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.name, iid=node.name)
                parent.insert(bookmark.Category(node.name))
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper, "end", text=node.name, iid=node.name)
                parent.insert(bookmark.Category(node.name))
            else:
                self.tree.insert("", "end", text=node.name, iid=node.name)
                root.insert(bookmark.Category(node.name))
        else:
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.paper, iid=node.paper)
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper, "end", text=node.paper, iid=node.paper)
            else:
                self.tree.insert("", "end", text=node.paper, iid=node.paper)

        for child in node.children:
            self.insertNode(child, node)

    def addCategory(self):
        global root
        name = simpledialog.askstring("카테고리 이름 설정", "카테고리 이름을 입력하세요:")
        c = bookmark.Category(name)
        self.insertNode(c, root)

    def delCategory(self):
        global root

        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            root.delete(selected_item)

    def changeItemName(self):
        selected_items = self.tree.selection()
        if selected_items:  # 선택된 아이템이 있는지 확인
            new_name = simpledialog.askstring("카테고리 이름 변경", "새 이름을 입력하세요:")
            if new_name:  # 사용자가 이름을 입력하고 'OK'를 누른 경우
                for item in selected_items:
                    self.tree.item(item, text=new_name)  # 선택된 아이템의 이름을 새로운 이름으로 변경

    def updateTreeview(self, node, parent = None):
        if isinstance(node, bookmark.Root):
            pass
        elif isinstance(node, bookmark.Category):
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.name, iid=node.name)
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper, "end", text=node.name, iid=node.name)
            else:
                self.tree.insert("", "end", text=node.name, iid=node.name)
        else:
            if isinstance(parent, bookmark.Category):
                self.tree.insert(parent.name, "end", text=node.paper, iid=node.paper)
            elif isinstance(parent, bookmark.BookmarkItem):
                self.tree.insert(parent.paper, "end", text=node.paper, iid=node.paper)
            else:
                self.tree.insert("", "end", text=node.paper, iid=node.paper)

        for child in node.children:
            self.updateTreeview(child, node)

    def addPaper(self):
        item = self.tree.focus_get()
        if not isinstance(item, bookmark.Category):
            return
        
        
        pass

def expandAllItems(tree, item=''):
    for child in tree.get_children(item):
        tree.item(child, open=True)
        expandAllItems(tree, child)