from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

from xml.dom import minidom

import GuiConfig
import papery
from save import SaveCollector
import telepot

# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

class Memo:
    WIDTH = 28  # number of characters
    HEIGHT = 8  # number of lines

    def __init__(self, master, text=''):
        self.master = master
        self.text = text
        self.widget = scrolledtext.ScrolledText(self.master,
            width = Memo.WIDTH, height = Memo.HEIGHT,
            font=GuiConfig.memoFont, wrap=WORD
        )
        
        self.widget.bind("<FocusIn>", self.on_focus_in)
        self.widget.bind("<FocusOut>", self.on_focus_out)
        self.widget.insert(END, self.text)

    def update(self):
        self.text = self.widget.get("1.0", END) # read from line 1, character 0 to the end

    def grid(self, i, j):
        self.widget.grid(row=i, column=j, padx=10, pady=10)

    def owns(self, widget):
        return self.widget == widget
    
    def on_focus_in(self, event):
        self.widget.config(bg="light gray")
    
    def on_focus_out(self, event):
        self.widget.config(bg="white")

class MemoTab:
    CNT_IN_A_ROW = 3

    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.mainGUI.saveCollector.add_saver(self)
        self.master = mainGUI.master

        self.frame = Frame(self.master)
        self.frame.pack()
        self.canvas = Canvas(self.frame)
        self.canvas.place(x=10, y=10, width=640, height=580)
        self.grids = Frame(self.canvas)
        self.grids.pack(fill=BOTH, expand=True)

        self.hasScroll = False

        self.memos = []
        self.memoCnt = 0

        self.gmailIcon = PhotoImage(file="res/gmail.PNG")
        self.gmailIcon = self.gmailIcon.subsample(4, 4)
        self.telegramIcon = PhotoImage(file="res/telegram.PNG")
        self.telegramIcon = self.telegramIcon.subsample(7, 7)

        self.loadXML()

        self.addButton = Button(self.frame, text="+", command=self.addMemo)
        self.addButton.place(x=660, y=40, width=60, height=50)

        self.delButton = Button(self.frame, text="-", command=self.delMemo)
        self.delButton.place(x=660, y=90, width=60, height=50)

        self.mailButton = Button(self.frame, command=self.mail, image=self.gmailIcon)
        self.mailButton.place(x=660, y=200, width=60, height=50)

        self.sendButton = Button(self.frame, command=self.send, image=self.telegramIcon)
        self.sendButton.place(x=660, y=260, width=60, height=50)

    def loadXML(self):
        try:
            doc = minidom.parse(papery.CACHE_PREFIX + "memo.xml")
            memos = doc.getElementsByTagName("memo")
            for i, memo in enumerate(memos):
                text = memo.firstChild.nodeValue
                # remove the last newline character
                text = text[:-1]
                self.memos.append(Memo(self.grids, text))
                self.memos[-1].grid(i // MemoTab.CNT_IN_A_ROW, i % MemoTab.CNT_IN_A_ROW)
                self.memoCnt += 1

            self.adjustScrollbar()
        except:
            pass

    def save(self):
        for memo in self.memos:
            memo.update()

        saveDoc = minidom.Document()
        memosElement = saveDoc.createElement("memos")
        saveDoc.appendChild(memosElement)
        
        for i, memo in enumerate(self.memos):
            memoElement = saveDoc.createElement("memo")
            memoElement.setAttribute("id", str(i))
            memoElement.appendChild(saveDoc.createTextNode(memo.text))
            memosElement.appendChild(memoElement)

        print( saveDoc.toprettyxml(),
            file=open(papery.CACHE_PREFIX + "memo.xml", "w", encoding="utf-8")
        )

    def addMemo(self, text=''):
        self.memos.append(Memo(self.grids, text))
        self.memos[-1].grid(self.memoCnt // MemoTab.CNT_IN_A_ROW, self.memoCnt % MemoTab.CNT_IN_A_ROW)

        self.memoCnt += 1
        self.adjustScrollbar()

    def delMemo(self):
        toDelWidget = self.grids.focus_get()
        toDel = None

        for memo in self.memos:
            if memo.owns(toDelWidget):
                toDel = memo
                break

        if toDel == None:
            return

        toDelWidget.grid_forget()
        self.memoCnt -= 1
        self.memos.remove(toDel)

        # rearrange grid
        for i in range(self.memoCnt):
            self.memos[i].grid(i // MemoTab.CNT_IN_A_ROW, i % MemoTab.CNT_IN_A_ROW)

        self.adjustScrollbar()


    def adjustScrollbar(self):
        self.frame.update()

        if self.memoCnt > 4 * MemoTab.CNT_IN_A_ROW:
            if not self.hasScroll:
                self.scroll = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
                self.canvas.config(yscrollcommand=self.scroll.set)
                self.hasScroll = True
                self.scroll.place(x=680, y=10, height=580)
        else:
            if self.hasScroll:
                self.scroll.place_forget()
                self.hasScroll = False
        
        self.canvas.delete("grid")
        self.canvas.create_window((0, 0), window=self.grids, anchor="nw", tags="grid")
        self.canvas.config(scrollregion=self.grids.bbox("all"))

    def mail(self):
        toMailWidget = self.grids.focus_get()
        
        toMail = None
        for memo in self.memos:
            if memo.owns(toMailWidget):
                toMail = memo
                break

        if toMail == None:
            messagebox.showinfo("Mail", "Select a memo to mail")
            return

        toMail.update()
        MailDialog(toMail, self.master)

    def send(self):
        bot = telepot.Bot(papery.TELEGRAM_BOT_TOKEN)
        toSendWidget = self.grids.focus_get()

        toSend = None
        for memo in self.memos:
            if memo.owns(toSendWidget):
                toSend = memo
                break

        if toSend == None:
            messagebox.showinfo("Telegram", "Select a memo to send")
            return
        
        toSend.update()
        bot.sendMessage(papery.TELEGRAM_CHAT_ID, toSend.text)

        messagebox.showinfo("Telegram", "Message sent")

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
            
            if text == "Sender Password":
                entry = Entry(self.window, show="*")
            else:
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
        
        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(msgPart)
        
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