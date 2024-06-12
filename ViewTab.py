from tkinter import *
from tkinter import messagebox
import GuiConfig
import webbrowser
from summary import Summarizer
from xmlParsing import DetailParser
from tkintermapview import TkinterMapView
import requests
from Loading import Loading
from translate import translate_text
import papery

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
            text_widget = Text(parent, font=font, wrap=WORD,
                width=GuiConfig.VIEW_PAPER_WIDTH, height=height, bg=bg
            )
            text_widget.tag_configure("center", justify='center')
            text_widget.insert(END, content)
            text_widget.tag_add("center", "1.0", "end")
            text_widget.configure(state='disabled')  # Make it read-only

            return text_widget
        
        def create_text_widget(parent, font, content, height, bg='white'):
            text_widget = Text(parent, font=font, wrap=WORD,
                width=GuiConfig.VIEW_PAPER_WIDTH, height=height, bg=bg
            )
            text_widget.insert(END, content)
            text_widget.configure(state='disabled')

            return text_widget

        # row 0 - title
        titleStr = self.paper.title + '\n' + ' | '.join(
            [', '.join( self.paper.authors ), self.paper.year]
        )
        tTitle = create_centered_text_widget(
            self.paperFrame, GuiConfig.paperTitleFont, titleStr, 2
        )
        tTitle.grid(row=0, column=0, sticky='nsew')

        # row 1 - abstract
        if self.paper.abstract is None:
            self.paper.abstract = '논문 초록 정보가 제공되지 않습니다.'

        self.tAbstract = create_text_widget(
            self.paperFrame, GuiConfig.cFont, self.paper.abstract, 6
        )
        self.tAbstract.grid(row=1, column=0, sticky='nsew')

        abstractScroll = Scrollbar(self.paperFrame, command=self.tAbstract.yview, orient=VERTICAL)
        abstractScroll.grid(row=1, column=1, sticky='ns')
        self.tAbstract.config(yscrollcommand=abstractScroll.set)

        # row 2 - reference header (using Text for word wrap and center alignment)
        tReferenceHeader = create_centered_text_widget(
            self.paperFrame, GuiConfig.headFont, "참조 논문", 1, '#dbdfdf'
        )
        tReferenceHeader.grid(row=2, column=0, sticky='nsew')

        # row 3 - reference list
        reference_text = '\n'.join(self.paper.refs) if self.paper.refs is not None \
            else '참조 논문 정보가 제공되지 않습니다.'
        tReference = create_text_widget(self.paperFrame, GuiConfig.refFont, reference_text, 3)
        tReference.grid(row=3, column=0, sticky='nsew')

        referenceScroll = Scrollbar(self.paperFrame, command=tReference.yview, orient=VERTICAL)
        referenceScroll.grid(row=3, column=1, sticky='ns')
        tReference.config(yscrollcommand=referenceScroll.set)

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
        self.buttons[-1].grid(row=0, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 1 - doi(url) button
        self.buttons.append( Button(self.buttonsFrame, text="DOI",
            font=GuiConfig.cFont, command=self.openDOI
        ) )
        self.buttons[-1].grid(row=1, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 2 - translation button
        self.buttons.append( Button(self.buttonsFrame, text="번역",
            font=GuiConfig.cFont, command=self.translate
        ) )
        self.buttons[-1].grid(row=2, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 3 - memo button
        self.buttons.append( Button(self.buttonsFrame, text="메모",
            font=GuiConfig.cFont, command=self.memo
        ) )
        self.buttons[-1].grid(row=3, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 4 - summarize button
        self.buttons.append( Button(self.buttonsFrame, text="요약",
            font=GuiConfig.cFont, command=self.summarize
        ) )
        self.buttons[-1].grid(row=4, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 5 - citation button
        self.buttons.append( Button(self.buttonsFrame, text="인용",
            font=GuiConfig.cFont, command=self.cite
        ) )
        self.buttons[-1].grid(row=5, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 6 - bookmark button
        self.buttons.append( Button(self.buttonsFrame, text="북마크",
            font=GuiConfig.cFont, command=self.bookmark
        ) )
        self.buttons[-1].grid(row=6, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        # row 7 - map button
        self.buttons.append( Button(self.buttonsFrame, text="지도",
            font=GuiConfig.cFont, command=self.map
        ) )
        self.buttons[-1].grid(row=7, column=0, sticky='nsew', pady=GuiConfig.WIDGET_INTERVALY // 2)

        for i in range(len(self.buttons)):
            self.buttonsFrame.rowconfigure(i, weight=1)
        self.buttonsFrame.columnconfigure(0, weight=1)

    def clear(self):
        self.paper = None
        self.buttons = []

        for widget in self.frame.winfo_children():
            widget.destroy()

    def setPaper(self, paper, source):
        self.clear()
        self.paper = paper
        if self.paper.articleID is not None:
            DetailParser(self.paper.articleID, source).searchAndParse().reflect(self.paper)
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
        self.tAbstract['state'] = 'normal'

        self.tAbstract.delete('1.0', END)
        self.tAbstract.insert(END, translate_text(self.paper.abstract, 'ko'))

        self.tAbstract['state'] = 'disabled'

    def memo(self):
        if self.paper is None:
            messagebox.showinfo("메모", "메모할 논문이 없습니다.")
            return

        self.paper.setHasMemo()

        memoStr='\n\n[Paper] ' + ' | '.join(
            [self.paper.title, self.paper.author, self.paper.year]
        )

        self.mainGUI.memoTab.addMemo(memoStr)
        self.mainGUI.notebook.select(self.mainGUI.memoTab.frame)

    def summarize(self):
        if self.paper is None:
            messagebox.showinfo("요약", "요약할 논문이 없습니다.")
            return
        
        messagebox.showinfo("요약", self.summarizer.summarize(self.paper.title, self.paper.abstract))

    def cite(self):
        if self.paper is None:
            messagebox.showinfo("인용", "인용할 논문이 없습니다.")
            return

        CiteDialog(self.paper, self.master)

    def bookmark(self):
        pass

    def map(self):
        if self.paper is None:
            messagebox.showinfo("지도", "지도에 표시할 논문이 없습니다.")
            return

        def task():
            MapWindow(self.master, self.paper)

        def onCompletion(result):
            pass

        Loading(self.master, task, onCompletion)

import clipboard

class CiteDialog:
    def __init__(self, paper, master):
        self.paper = paper
        self.master = master

        self.frame = Toplevel(master)
        self.frame.title("인용")
        self.frame.geometry("300x200")

        # select which format to cite
        # by choosing the format with a radio button
        self.radioFrame = Frame(self.frame)
        self.radioFrame.pack()

        self.format = StringVar()
        self.format.set("APA")

        self.radioAPA = Radiobutton(self.radioFrame, text="APA", variable=self.format, value="APA")
        self.radioAPA.pack(side=LEFT)

        self.radioMLA = Radiobutton(self.radioFrame, text="MLA", variable=self.format, value="MLA")
        self.radioMLA.pack(side=LEFT)

        self.radioChicago = Radiobutton(self.radioFrame, text="Chicago", variable=self.format, value="Chicago")
        self.radioChicago.pack(side=LEFT)

        self.submitButton = Button(self.frame, text="인용하기", command=self.submit)
        self.submitButton.pack()

    def submit(self):
        citation = None
        if self.format.get() == "APA":
            citation = self.makeAPACitation()
        elif self.format.get() == "MLA":
            citation = self.makeMLACitation()
        elif self.format.get() == "Chicago":
            citation = self.makeChicagoCitation()

        clipboard.copy(citation)
        self.frame.destroy()

    def makeAPACitation(self):
        return self.paper.author + ' (' + self.paper.year + '). ' + self.paper.title
        # return self.paper.author + ' (' + self.paper.year + '). ' + self.paper.title + '. ' + self.paper.journal + ', ' + self.paper.volume + '(' + self.paper.issue + '), ' + self.paper.pages + '.'

    def makeMLACitation(self):
        return self.paper.author + '. "' + self.paper.title + '." (' + self.paper.year + ')'
        # return self.paper.author + '. "' + self.paper.title + '." ' + self.paper.journal + ' ' + self.paper.volume + '.' + self.paper.issue + ' (' + self.paper.year + '): ' + self.paper.pages + '.'

    def makeChicagoCitation(self):
        return self.paper.author + '. "' + self.paper.title + '." (' + self.paper.year + ')'
        # return self.paper.author + '. "' + self.paper.title + '." ' + self.paper.journal + ' ' + self.paper.volume + ', no. ' + self.paper.issue + ' (' + self.paper.year + '): ' + self.paper.pages + '.'

class MapWindow:
    def __init__(self, master, paper):
        self.master = master
        self.paper = paper

        self.frame = Toplevel(master)
        self.frame.title("지도")
        self.frame.geometry("600x400")
        self.frame.resizable(False, False)

        self.gmap_widget = TkinterMapView(self.frame, width=600, height=400)
        self.gmap_widget.pack(fill=BOTH)

        self.gmap_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=kr&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )

        insti = self.paper.authors[0][self.paper.authors[0].find('('):]
        if insti == self.paper.authors[0][-1]:
            insti = None
        else:
            insti = insti[1:-1]

        if insti is None:
            self.marker = self.gmap_widget.set_position(0, 0, marker=True)
            self.marker.set_text("기관 정보가 제공되지 않습니다.")
        else:
            self.marker = self.gmap_widget.set_address(insti, marker=True)
            if self.marker is not False:
                self.marker.set_text(insti)
            else:
                lat, lng = self.get_lat_lng(insti, papery.KAKAO_MAP_API_KEY)
                if lat is not None and lng is not None:
                    self.marker = self.gmap_widget.set_position(lat, lng, marker=True)
                    self.marker.set_text(insti)
                else:
                    self.marker = self.gmap_widget.set_position(0, 0, marker=True)
                    self.marker.set_text("위치 정보를 찾을 수 없습니다.")

        self.gmap_widget.set_zoom(16)

    def get_lat_lng(self, address, api_key):
        url = 'https://dapi.kakao.com/v2/local/search/address.json'
        headers = {
            'Authorization': f'KakaoAK {api_key}'
        }
        params = {
            'query': address
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            result = response.json()
            if result['documents']:
                address_info = result['documents'][0]
                lat = address_info['y']
                lng = address_info['x']
                return lat, lng
            else:
                return None, None
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")