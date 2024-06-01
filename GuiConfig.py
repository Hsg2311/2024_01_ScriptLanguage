from tkinter import font

#Common
WIDTH = 800
HEIGHT = 600
GIF_WIDTH = 150
GIF_HEIGHT = 75
GIF_PADDINGX = 20
GIF_PADDINGY = 10
TABS_PADDINGX = 20
TABS_PADDINGY = 10
WIDGET_INTERVALX = 15
WIDGET_INTERVALY = 15

#SearchTab
SEARCH_BAR_PADDING_Y = 15
SEARCH_RESULT_WIDTH = 500
SEARCH_RESULT_HEIGHT = 400
SEARCH_RESULT_TRAY_WIDTH = 400
SEARCH_RESULT_TRAY_HEIGHT = 30
SEARCH_ENTRY_WIDTH = 300
SEARCH_ENTRY_HEIGHT = 25
SEARCH_BUTTON_WIDTH = 60
SEARCH_BUTTON_HEIGHT = 25
SEARCH_VIEW_BUTTON_WIDTH = 80
SEARCH_VIEW_BUTTON_HEIGHT = 60
SEARCH_VIEW_BUTTON_PADDINGY = 20

#ViewTab
VIEW_PADDINGY = 60
VIEW_PAPER_WIDTH = 600
VIEW_PAPER_HEIGHT = 400
VIEW_BUTTONS_WIDTH = 80
VIEW_BUTTONS_HEIGHT = 400

cFont = None
paperTitleFont = None
headFont = None
memoFont = None

def initFonts():
    global cFont
    cFont = font.Font(family="맑은 고딕", size=10, weight="normal", slant="roman")

    global paperTitleFont
    paperTitleFont = font.Font(family="맑은 고딕", size=12, weight="bold", slant="roman")

    global headFont
    headFont = font.Font(family="맑은 고딕", size=10, weight="bold", slant="roman")

    global memoFont
    memoFont = font.Font(family="맑은 고딕", size=8, weight="normal", slant="roman")