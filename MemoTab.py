from tkinter import *
from tkinter import messagebox

# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

class Memo:
    WIDTH = 28  # number of characters
    HEIGHT = 8  # number of lines

    def __init__(self, master, text=''):
        self.master = master
        self.text = text
        self.widget = Text(self.master, width = Memo.WIDTH, height = Memo.HEIGHT)
        self.widget.insert(END, self.text)

    def update(self):
        self.text = self.widget.get("1.0", END) # read from line 1, character 0 to the end

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

        if toDel == None or not isinstance(toDel, Text):
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
        toMail = self.grids.focus_get()
        print(toMail)
        if toMail == None or not isinstance(toMail, Text):
            messagebox.showinfo("Mail", "Select a memo to mail")
            return
        
        for memo in self.memos:
            if memo.owns(toMail):
                memo.update()
                MailDialog(memo, self.master)

    def send(self):
        pass

import mysmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailDialog:
    def __init__(self, memo, master):
        self.memo = memo
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
        senderAddr, recipientAddr, title, passwd = values[:4]
        
        #Message container를 생성합니다.
        msg = MIMEMultipart('alternative')

        #set message
        msg['Subject'] = title
        msg['From'] = senderAddr
        msg['To'] = recipientAddr
        
        msgPart = MIMEText(self.memo.text, 'plain')
        print(self.memo.text)
        
        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(msgPart)
        
        print ("connect smtp server ... ")
        s = mysmtplib.MySMTP(host,port)
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(senderAddr, passwd)    # 로긴을 합니다. 
        s.sendmail(senderAddr , [recipientAddr], msg.as_string())
        s.close()

        messagebox.showinfo("Mail", "Mail sending complete.")
        self.window.destroy()