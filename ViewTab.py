from tkinter import *

class ViewTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master

        self.frame = Frame(self.master)
        self.frame.pack(fill=BOTH, expand=True)

        self.label = Label(self.frame, text="View Tab")
        self.label.pack(padx=20, pady=20)
        
        self.button = Button(self.frame, text="Click Me", command=self.buttonClick)
        self.button.pack(padx=20, pady=20)

    def buttonClick(self):
        self.label.config(text="Button Clicked")