class Node:
    def __init__(self):
        self.parent = None
        self.children = []

    def insert(self, node):
        self.children.append(node)
        node.parent = self

    def delete(self, node):
        if node not in self.children:
            return
        self.children.remove(node)
        node.parent = None

    def destroy(self):
        for child in self.children:
            child.parent = None
        if self.parent is not None:
            self.parent.delete(self)

class Category(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

class BookmarkItem(Node):
    def __init__(self, paper):
        super().__init__()
        self.paper = paper

def traverse(node, indentLevel=0):
    print("    " * indentLevel, end="")
    if isinstance(node, Category):
        print(node.name)
    else:
        print(node.paper)

    for child in node.children:
        traverse(child, indentLevel + 1)


if __name__ == "__main__":
    r = Category("Root")
    c1 = Category("Category1")
    c2 = Category("Category2")
    c3 = Category("Category3")

    r.insert(c1)
    r.insert(c2)
    r.insert(c3)

    b1 = BookmarkItem("Paper1")
    b2 = BookmarkItem("Paper2")

    c1.insert(b1)
    c1.insert(b2)

    b3 = BookmarkItem("Paper3")
    b4 = BookmarkItem("Paper4")
    b5 = BookmarkItem("Paper5")

    c2.insert(b3)
    c2.insert(b4)
    c2.insert(b5)

    b6 = BookmarkItem("Paper6")

    c3.insert(b6)

    traverse(r)

    #test delete
    c1.delete(b1)
    r.delete(c2)

    traverse(r)

    #test destroy
    c3.destroy()
    b2.destroy()

    traverse(r)