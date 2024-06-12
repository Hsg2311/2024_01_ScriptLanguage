from tkinter import *
from tkinter import messagebox

from tkinter import ttk
from tkinter import simpledialog
from tkinter import Toplevel

import bookmark

from BookmarkRoot import root

class BookmarkTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master
        
        self.frame = Frame(self.master)
        self.frame.pack()

        # show bookmark tree as treeview
        self.style = ttk.Style()
        self.style.configure('Treeview', font=('Helvetica', 14), rowheight=30)

        self.tree = ttk.Treeview(self.frame)
        self.tree.place(x=50, y=50, width=500, height=400)

        self.addButton = Button(self.frame, text='카테고리 추가', command=self.addCategory)
        self.addButton.place(x=600, y=150, width=90, height=30)
        self.delButton = Button(self.frame, text='카테고리 삭제', command=self.delCategory)
        self.delButton.place(x=600, y=210, width=90, height=30)
        self.ncButton = Button(self.frame, text='카테고리 이름 수정', command=self.changeItemName)
        self.ncButton.place(x=600, y=270, width=120, height=30)

        delPaperButton = Button(self.frame, text='논문 제거', command=self.delPaper)
        delPaperButton.place(x=600, y=330, width=65, height=30)
        viewButton = Button(self.frame, text='보기', command=self.view)
        viewButton.place(x=600, y=400, width=50, height=30)
        viewCitation = Button(self.frame, text='인용수', command=self.viewCitationCnt)
        viewCitation.place(x=600, y=470, width=50, height=30)

        # self.insertNode(BookmarkRoot)
        expandAllItems(self.tree)

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

    def findCategory(self, node, name):
        for child in node.children:
            if isinstance(child, bookmark.Category) and child.owns(name):
                return child
        for child in node.children:
            tmp = self.findCategory(child, name)
            if tmp is not None:
                return tmp
            
        return None
    
    def findBookmarkItem(self, node, title):
        for category in node.children:
            for bookmarkItem in category.children:
                if isinstance(bookmarkItem, bookmark.BookmarkItem) and bookmarkItem.owns(title):
                    return bookmarkItem
            
        return None

    def addCategory(self):
        global root
        name = simpledialog.askstring("카테고리 이름 설정", "카테고리 이름을 입력하세요:")
        c = bookmark.Category(name)
        self.insertNode(c, root)

    def delCategory(self):
        global root

        selected_item = self.tree.selection()
        if selected_item:
            self.findCategory(root, selected_item[0]).destroy()
            self.tree.delete(selected_item)
            

    def changeItemName(self):
        selected_item = self.tree.selection()
        if selected_item:  # 선택된 아이템이 있는지 확인
            new_name = simpledialog.askstring("카테고리 이름 변경", "새 이름을 입력하세요:")
            if new_name:  # 사용자가 이름을 입력하고 'OK'를 누른 경우
                self.findCategory(root, selected_item[0]).name = new_name
                self.tree.item(selected_item[0], text=new_name)  # 선택된 아이템의 이름을 새로운 이름으로 변경

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

    def delPaper(self):
        global root

        selected_item = self.tree.selection()
        if selected_item:
            self.findBookmarkItem(root, selected_item[0]).destroy()
            self.tree.delete(selected_item[0])

    def view(self):
        global root
        
        paperTitle = self.tree.selection()

        paper = self.findBookmarkItem(root, paperTitle[0])
        self.mainGUI.viewTab.setPaper(paper.paper)
        self.mainGUI.viewTab.show(self)

    def viewCitationCnt(self):
        global root

        selected_item = self.tree.selection()
        category = self.findCategory(root, selected_item[0])

        if category:
            new_window = Toplevel(self.mainGUI.master)
            new_window.title('인용수 보기')
            new_window.geometry('800x600+100+100')

            listbox = Listbox(new_window)
            citations = []
            
            for i in range(len(category.children)-1, -1, -1):
                listbox.insert(0, str(i+1)+'. '+category.children[i].paper.title)
            for i in range(len(category.children)):
                if category.children[i].paper.citationCnt == None:
                    citations.append(0)
                    continue
                citations.append(int(category.children[i].paper.citationCnt))
            for i in citations:
                print(type(i), ' ', i)

            listbox.place(x=0, y=0, width=200, height=200)
            
            vScrollbar = ttk.Scrollbar(new_window, orient='vertical', command=listbox.yview)
            listbox.configure(yscrollcommand=vScrollbar.set)
            vScrollbar.place(x=200, y=0, width=20, height=200)

            hScrollbar = ttk.Scrollbar(new_window, orient='horizontal', command=listbox.xview)
            listbox.configure(xscrollcommand=hScrollbar.set)
            hScrollbar.place(x=0, y=200, width=200, height=20)

            canvas = Canvas(new_window, bg='white', width=600, height= 500)
            canvas.place(x=220, y=0, width=580, height=500)
            hCanvasScrollbar = ttk.Scrollbar(new_window, orient='horizontal', command=canvas.xview)
            canvas.configure(xscrollcommand=hCanvasScrollbar.set)
            hCanvasScrollbar.place(x=220, y=500, width=580, height=20)
            
            barWidth = (580-20)/20
            height = 500
            maxCitation = max(citations)
            step = 50
            for i in range(len(category.children)):
                canvas.create_rectangle(20+(i*step)+i*barWidth, height-(height-200)*citations[i]/maxCitation,
                                        20+(i*step)+(i+1)*barWidth, height-40)
                canvas.create_text(35+(i*step)+i*barWidth, height-20, text=str(i+1)+'번\n논문')
                canvas.create_text(35+(i*step)+i*barWidth, height-(height-200)*citations[i]/maxCitation-10, text=str(citations[i]))

            self.frame.update()
            canvas.configure(scrollregion=canvas.bbox('all'))

def expandAllItems(tree, item=''):
    for child in tree.get_children(item):
        tree.item(child, open=True)
        expandAllItems(tree, child)