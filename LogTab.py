from tkinter import *
from tkinter import messagebox

import GuiConfig

class LogTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master
        
        self.frame = Frame(self.master)
        self.frame.pack()
        
        self.dummyFrame = Frame(self.frame)
        self.dummyFrame.pack(pady=GuiConfig.LOG_PADDINGY // 2)

        self.logFrame = Frame(self.frame)
        self.logFrame.pack(side=LEFT)

        self.searchLogFrame = Frame(self.logFrame)
        self.searchLogFrame.pack()
        self.searchLogCanvas = Canvas(self.searchLogFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_SEARCHLOG_HEIGHT, bg="red"
        )
        self.searchLogCanvas.pack()

        self.viewLogFrame = Frame(self.logFrame)
        self.viewLogFrame.pack(pady=GuiConfig.WIDGET_INTERVALY)
        self.viewLogCanvas = Canvas(self.viewLogFrame, width=GuiConfig.LOG_LOG_WIDTH,
            height=GuiConfig.LOG_VIEWLOG_HEIGHT, bg="blue"
        )
        self.viewLogCanvas.pack()

        self.viewButtonFrame = Frame(self.frame)
        self.viewButtonFrame.pack(side=LEFT, padx=GuiConfig.WIDGET_INTERVALX,
            fill=Y, expand=True
        )

        self.viewButton = Button(self.viewButtonFrame, text="View",
            width=GuiConfig.LOG_VIEW_BUTTON_WIDTH, height=5,
            command=self.click
        )
        self.viewButton.pack(pady=GuiConfig.LOG_VIEW_BUTTON_PADDINGY, side=TOP, anchor=N)


        self.buildSearchLog()
        self.buildViewLog()

    def buildSearchLog(self):
        pass

    def buildViewLog(self):
        pass

    def click(self):
        messagebox.showinfo("Log Tab", "You clicked the button in the Log Tab")