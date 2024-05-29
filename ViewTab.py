from tkinter import *
import GuiConfig

class ViewTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master

        self.frame = Frame(self.master)
        self.frame.pack()

        self.paper = None
        self.returnTab = None
        self.buttons = []

    def show(self, returnTab):
        self.returnTab = returnTab
        self.mainGUI.notebook.select(self.frame)

    def goBack(self):
        self.mainGUI.notebook.select(self.returnTab.frame)
        self.mainGUI.notebook.hide(self.frame)

    def initWidgets(self):
        self.paperFrame = Frame(self.frame)
        self.paperFrame.place(
            x=GuiConfig.TABS_PADDINGX, y=GuiConfig.VIEW_PADDINGY,
            width=GuiConfig.VIEW_PAPER_WIDTH, height=GuiConfig.VIEW_PAPER_HEIGHT,
            anchor=NW
        )

        self.buttonsFrame = Frame(self.frame)
        self.buttonsFrame.place(
            x=GuiConfig.TABS_PADDINGX + GuiConfig.VIEW_PAPER_WIDTH + GuiConfig.WIDGET_INTERVALX,
            y=GuiConfig.VIEW_PADDINGY,
            width=GuiConfig.VIEW_BUTTONS_WIDTH, height=GuiConfig.VIEW_BUTTONS_HEIGHT,
            anchor=NW
        )

        # Prevent the paperFrame from resizing itself to fit its children
        self.paperFrame.grid_propagate(False)

        # Create a tag for center alignment
        def create_centered_text_widget(parent, font, content, height):
            frame = Frame(parent)
            text_widget = Text(frame, font=font, wrap=WORD, width=GuiConfig.VIEW_PAPER_WIDTH, height=height)
            text_widget.tag_configure("center", justify='center')
            text_widget.insert(END, content)
            text_widget.tag_add("center", "1.0", "end")
            text_widget.configure(state='disabled')  # Make it read-only

            # Place the text widget in the center of the frame
            text_widget.grid(row=0, column=0, sticky='nsew')
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

            return frame

        # row 0 - title
        titleStr = self.paper.title + '\n' + ' | '.join(
            [self.paper.author, self.paper.year]
        )
        tTitle = create_centered_text_widget(self.paperFrame, GuiConfig.paperTitleFont, titleStr, 2)
        tTitle.grid(row=0, column=0, sticky='nsew')

        # row 1 - abstract
        tAbstract = create_centered_text_widget(self.paperFrame, GuiConfig.cFont, self.paper.abstract, 6)
        tAbstract.grid(row=1, column=0, sticky='nsew')

        # row 2 - reference header (using Text for word wrap and center alignment)
        tReferenceHeader = create_centered_text_widget(self.paperFrame, GuiConfig.cFont, "관련 논문", 1)
        tReferenceHeader.grid(row=2, column=0, sticky='nsew')

        # row 3 - reference list
        reference_text = '현재 관련 논문 기능은 구현되어있지 않습니다.\n(참고 문헌 또는 피인용 논문 고려 구현 예정)'
        tReference = create_centered_text_widget(self.paperFrame, GuiConfig.cFont, reference_text, 3)
        tReference.grid(row=3, column=0, sticky='nsew')

        self.paperFrame.rowconfigure(0, weight=2)
        self.paperFrame.rowconfigure(1, weight=6)
        self.paperFrame.rowconfigure(2, weight=1)
        self.paperFrame.rowconfigure(3, weight=3)
        self.paperFrame.columnconfigure(0, weight=1)

        # configure buttons
        self.buttons.append( Button(self.buttonsFrame, text="돌아가기",
            font=GuiConfig.cFont, command=self.goBack
        ) )
        self.buttons[-1].grid(row=0, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY)

        for i in range(len(self.buttons)):
            self.buttonsFrame.rowconfigure(i, weight=1)
        self.buttonsFrame.columnconfigure(0, weight=1)

    def clear(self):
        self.paper = None
        self.buttons = []

        for widget in self.frame.winfo_children():
            widget.destroy()

    def setPaper(self, paper):
        self.clear()
        self.paper = paper
        self.initWidgets()