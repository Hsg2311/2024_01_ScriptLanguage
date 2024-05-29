from tkinter import *
from tkinter import messagebox
import GuiConfig
import webbrowser
from summary import Summarizer

class ViewTab:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI
        self.master = mainGUI.master

        self.frame = Frame(self.master)
        self.frame.pack()

        self.paper = None
        self.returnTab = None
        self.buttons = []
        self.summarizer = Summarizer()

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
        def create_centered_text_widget(parent, font, content, height, bg='white'):
            frame = Frame(parent)
            text_widget = Text(frame, font=font, wrap=WORD,
                width=GuiConfig.VIEW_PAPER_WIDTH, height=height, bg=bg
            )
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
        tTitle = create_centered_text_widget(
            self.paperFrame, GuiConfig.paperTitleFont, titleStr, 2
        )
        tTitle.grid(row=0, column=0, sticky='nsew')

        # row 1 - abstract
        tAbstract = create_centered_text_widget(
            self.paperFrame, GuiConfig.cFont, self.paper.abstract, 6
        )
        tAbstract.grid(row=1, column=0, sticky='nsew')

        # row 2 - reference header (using Text for word wrap and center alignment)
        tReferenceHeader = create_centered_text_widget(
            self.paperFrame, GuiConfig.headFont, "관련 논문", 1, '#dbdfdf'
        )
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

        # row 0 - return button
        self.buttons.append( Button(self.buttonsFrame, text="돌아가기",
            font=GuiConfig.cFont, command=self.goBack
        ) )
        self.buttons[-1].grid(row=0, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY)

        # row 1 - doi(url) button
        self.buttons.append( Button(self.buttonsFrame, text="DOI",
            font=GuiConfig.cFont, command=self.openDOI
        ) )
        self.buttons[-1].grid(row=1, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY)

        # row 2 - translation button
        self.buttons.append( Button(self.buttonsFrame, text="번역",
            font=GuiConfig.cFont, command=self.translate
        ) )
        self.buttons[-1].grid(row=2, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY)

        # row 3 - memo button
        self.buttons.append( Button(self.buttonsFrame, text="메모",
            font=GuiConfig.cFont, command=self.memo
        ) )
        self.buttons[-1].grid(row=3, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY)

        # row 4 - summarize button
        self.buttons.append( Button(self.buttonsFrame, text="요약",
            font=GuiConfig.cFont, command=self.summarize
        ) )
        self.buttons[-1].grid(row=4, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY)

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

    def openDOI(self):
        if self.paper is None:
            messagebox.showinfo("DOI", "DOI를 열 논문이 없습니다.")
            return

        if self.paper.doi is not None:
            webbrowser.open(self.paper.doi)
        elif self.paper.url is not None:
            webbrowser.open(self.paper.url)
        else:
            messagebox.showinfo("DOI", "DOI 혹은 URL 정보가 제공되지 않았습니다.")

    def translate(self):
        pass

    def memo(self):
        if self.paper is None:
            messagebox.showinfo("메모", "메모할 논문이 없습니다.")
            return

        memoStr='\n\n[Paper] ' + ' | '.join(
            [self.paper.title, self.paper.author, self.paper.year]
        )

        self.mainGUI.memoTab.addMemo(memoStr)
        self.mainGUI.notebook.select(self.mainGUI.memoTab.frame)
        self.mainGUI.notebook.hide(self.frame)

    def summarize(self):
        if self.paper is None:
            messagebox.showinfo("요약", "요약할 논문이 없습니다.")
            return
        
        messagebox.showinfo("요약", self.summarizer.summarize(self.paper.title, self.paper.abstract))