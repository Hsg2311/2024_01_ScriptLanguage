from tkinter import *
from tkinter import messagebox

from tkinter import ttk
from tkinter import simpledialog

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

        # self.insertNode(BookmarkRoot)
        expandAllItems(self.tree)

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

    def findCategory(self, node, name):
        for child in node.children:
            if isinstance(child, bookmark.Category) and child.owns(name):
                return child
        for child in node.children:
            tmp = self.findCategory(child, name)
            if tmp is not None:
                return tmp
            
        return None

    def addCategory(self):
        global root
        name = simpledialog.askstring("카테고리 이름 설정", "카테고리 이름을 입력하세요:")
        c = bookmark.Category(name)
        self.insertNode(c, root)

    def delCategory(self):
        global root

        selected_item = self.tree.selection()
        print(selected_item)
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

    def clearTreeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)   

def expandAllItems(tree, item=''):
    for child in tree.get_children(item):
        tree.item(child, open=True)
        expandAllItems(tree, child)