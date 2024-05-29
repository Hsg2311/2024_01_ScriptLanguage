import papery
from paper import Paper
import xml.etree.ElementTree as ET
import requests

class xmlParsing:
    def __init__(self, apiKey, searchStr, paperDataURL, basePage, parseCnt):
        self.papers = []
        self.searchStr = searchStr
        self.key = apiKey
        self.paperDataURL = paperDataURL
        self.basePage = basePage
        self.cnt = parseCnt
        self.roots = []

    def printPapers(self, file=None):
        for paper in self.papers:
            print('Year :', paper.year, file=file)
            print('Title :', paper.title, file=file)
            print('Author :', paper.author, file=file)
            print('Abstract :', paper.abstract, file=file)
            print('DOI :', paper.doi if paper.doi is not None else 'DOI 정보가 없습니다.', file=file)
            print('URL :', paper.url if paper.url is not None else 'URL 정보가 없습니다.', file=file)
            print('Citation Count :', paper.citationCnt, file=file)
            print(file=file)

    def parseFromXMLFile(self, xmlFile):
        self.parseFromXMLStr(open(xmlFile, 'r', encoding='utf-8').read())

    def parseFromXMLStr(self, xmlStr, buildNewRoot=True):
        root = ET.fromstring(xmlStr)
        if buildNewRoot:
            self.roots.clear()
        self.roots.append(root)

        for item in root.iter('record'):
            jour = item.find('journalInfo')
            arti = item.find('articleInfo')

            self.papers.append( Paper(
                title=self.getTitle(arti),
                author=', '.join( self.getAuthor(arti) ),
                year=self.getPubYear(jour),
                school='',
                doi=self.getDOI(arti),
                url=self.getURL(arti),
                abstract=self.getAbstract(arti),
                citationCnt=self.getCitationCount(arti)
            ) )

    def parse(self):
        for i in range(0, self.cnt // 100):
            paperDataParams = {'key' : self.key, 'apiCode' : 'articleSearch',
                'title' : self.searchStr, 'page' : i + self.basePage,
                'displayCount' : 100
            }
            response = requests.get(self.paperDataURL, params=paperDataParams)
            self.parseFromXMLStr( response.text, False )

    def printAsXML(self, file=None):
        for root in self.roots:
            print( ET.tostring(root, encoding='utf8').decode('utf8'),
                file=open(file, 'w', encoding='utf-8') if file is not None else None
            )

    def getPubYear(self, item):
        year = item.find('pub-year')
        return year.text

    def getTitle(self, item):
        # 상위 엘리먼트에서부터 찾으면서 내려와야 함.
        title_group = item.find('title-group')
        article_title = title_group.find('article-title')
        return article_title.text
    
    def getAuthor(self, item):
        result = []
        author_group = item.find('author-group')
        for author in author_group.findall('author'):
            result.append(author.text)
        return result
    
    def getAbstract(self, item):
        abst_group = item.find('abstract-group')
        abst = abst_group.find('abstract')

        if abst.text is None:
            return '논문 초록이 제공되지 않습니다.'
        else:
            return abst.text

    def getDOI(self, item):
        doi = item.find('doi')

        if doi.text is None:
            return None
        else:
            return doi.text

    def getURL(self, item):
        url = item.find('url')

        if url.text is None:
            return None
        else:
            return url.text

    def getCitationCount(self, item):
        cnt = item.find('citation-count')
        return cnt.text

if __name__ == '__main__':
    parser = xmlParsing(papery.KEY, "컴퓨터", papery.paperDataUrl, 1, 300)
    parser.parse()
    parser.printAsXML('paper.xml')