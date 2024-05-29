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

    def printPapers(self):
        for paper in self.papers:
            print('Year :', paper.year)
            print('Title :', paper.title)
            print('Author :', paper.author)
            print('Abstract :', paper.abstract)
            print('DOI :', paper.doi if paper.doi is not None else 'DOI 정보가 없습니다.')
            print('URL :', paper.url if paper.url is not None else 'URL 정보가 없습니다.')
            print('Citation Count :', paper.citationCnt)
            print()

    def parse(self):
        for i in range(0, self.cnt // 100):
            paperDataParams = {'key' : self.key, 'apiCode' : 'articleSearch',
                'title' : self.searchStr, 'page' : i + self.basePage,
                'displayCount' : 100
            }
            response = requests.get(self.paperDataURL, params=paperDataParams)

            root = ET.fromstring(response.text)

            for item in root.iter('record'):
                jour = item.find('journalInfo')
                arti = item.find('articleInfo')

                self.papers.append( Paper(
                    title=self.getTitle(arti),
                    author=self.getAuthor(arti),
                    year=self.getPubYear(jour),
                    school='',
                    doi=self.getDOI(arti),
                    url=self.getURL(arti),
                    abstract=self.getAbstract(arti),
                    citationCnt=self.getCitationCount(arti)
                ) )

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
    parser = xmlParsing(papery.KEY, "컴퓨터", papery.paperDataUrl, 1, 200)
    parser.parse()
    parser.printPapers()