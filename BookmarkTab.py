from tkinter import *
from tkinter import messagebox

from tkinter import ttk

import bookmark

testBookmarkRoot = bookmark.Category("Root")

c1 = bookmark.Category("Category1")
c2 = bookmark.Category("Category2")
c3 = bookmark.Category("Category3")

b1 = bookmark.BookmarkItem("Paper1")
b2 = bookmark.BookmarkItem("Paper2")
b3 = bookmark.BookmarkItem("Paper3")
b4 = bookmark.BookmarkItem("Paper4")
b5 = bookmark.BookmarkItem("Paper5")
b6 = bookmark.BookmarkItem("Paper6")

testBookmarkRoot.insert(c1)
testBookmarkRoot.insert(c2)
testBookmarkRoot.insert(c3)

c1.insert(b1)
c1.insert(b2)

c2.insert(b3)
c2.insert(b4)

c3.insert(b5)
c3.insert(b6)

class BookmarkTab:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        global testBookmarkRoot
        # show bookmark tree as treeview
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack()

        self.insertNode(testBookmarkRoot)

    def insertNode(self, node, parent = None):
        if isinstance(node, bookmark.Category):
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
            self.insertNode(child, node)