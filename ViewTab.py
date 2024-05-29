from tkinter import *

class ViewTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master

        self.frame = Frame(self.master)
        self.frame.pack()

        self.paper = None

    def setPaper(self, paper):
        self.paper = paper
        print(self.paper.title)