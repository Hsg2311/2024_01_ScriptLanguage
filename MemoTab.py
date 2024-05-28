from tkinter import *

class Memo:
    WIDTH = 28  # number of characters
    HEIGHT = 8  # number of lines

    def __init__(self, master, text=''):
        self.master = master
        self.text = text
        self.widget = Text(self.master, width = Memo.WIDTH, height = Memo.HEIGHT)
        self.widget.insert(END, self.text)

    def grid(self, i, j):
        self.widget.grid(row=i, column=j, padx=10, pady=10)

    def owns(self, widget):
        return self.widget == widget

class MemoTab:
    CNT_IN_A_ROW = 3

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.grids = Frame(self.frame)
        self.grids.place(x=10, y=10, width=680, height=580)

        self.memos = []
        self.memoCnt = 0
    

        for i in range(len(self.memos)):
            self.memos[i].grid(i // MemoTab.CNT_IN_A_ROW, i % MemoTab.CNT_IN_A_ROW)

        self.addButton = Button(self.frame, text="+", command=self.addMemo)
        self.addButton.place(x=700, y=40, width=60, height=50)

        self.delButton = Button(self.frame, text="-", command=self.delMemo)
        self.delButton.place(x=700, y=90, width=60, height=50)

        self.mailButton = Button(self.frame, text="Mail", command=self.mail)
        self.mailButton.place(x=700, y=200, width=60, height=50)

        self.sendButton = Button(self.frame, text="Send", command=self.send)
        self.sendButton.place(x=700, y=260, width=60, height=50)

    def addMemo(self):
        self.memos.append(Memo(self.grids))
        self.memos[-1].grid(self.memoCnt // MemoTab.CNT_IN_A_ROW, self.memoCnt % MemoTab.CNT_IN_A_ROW)

        self.memoCnt += 1

    def delMemo(self):
        toDel = self.grids.focus_get()

        if toDel == None:
            return

        toDel.grid_forget()
        self.memoCnt -= 1

        # remove memo
        for i in range(self.memoCnt):
            if self.memos[i].owns(toDel):
                del self.memos[i]
                break

        # rearrange grid
        for i in range(self.memoCnt):
            self.memos[i].grid(i // MemoTab.CNT_IN_A_ROW, i % MemoTab.CNT_IN_A_ROW)
        

    def mail(self):
        MailDialog(self.master)

    def send(self):
        pass

class MailDialog:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(self.master)
        self.window.title("Mail")
        
        self.entries = []

        labels_texts = ["Sender Address", "Recipient Address", "Title", "Sender Password"]
        for i, text in enumerate(labels_texts):
            label = Label(self.window, text=text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            entry = Entry(self.window)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)

        submit_button = Button(self.window, text="Submit", command=self.submit)
        submit_button.grid(row=len(labels_texts), columnspan=2, pady=10)

    def submit(self):
        values = [entry.get() for entry in self.entries]
        print(values)