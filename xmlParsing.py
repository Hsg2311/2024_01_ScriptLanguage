import papery
import xml.etree.ElementTree as ET
import requests

class xmlParsing:
    def __init__(self, key, paperDataURL, parseCnt):
        self.papers = []
        self.key = key
        self.paperDataURL = paperDataURL
        self.cnt = parseCnt

    def printPapers(self):
        for paper in self.papers:
            print('Title :', paper['Title'])

    def parse(self):
        for _ in range(1, (self.cnt // 100) + 1):
            paperDataParams = {'key' : self.key, 'apiCode' : 'articleSearch', 'title' : 1, 'displayCount' : 100}
            response = requests.get(self.paperDataURL, params=paperDataParams)
            
            # f = open('paperData.xml', 'w', encoding='utf-8')
            # f.write(response.text)
            # f.close()

            root = ET.fromstring(response.text)

            for item in root.iter('articleInfo'):
                paper = {
                    'Title' : self.getTitle(item)
                }
                self.papers.append(paper)

    def getTitle(self, item):
        # 상위 엘리먼트에서부터 찾으면서 내려와야 함.
        title_group = item.find('title-group')
        article_title = title_group.find('article-title')
        print(article_title.text)
        # title_group = item.findtext('title-group')
        # if title_group is not None:
        #     for article_title in item.findall('article-title'):
        #         if article_title.get('lang') == 'original':
        #             return article_title.text
        # return 'fuck'

parser = xmlParsing(papery.KEY, papery.paperDataUrl, 100)
parser.parse()
parser.printPapers()