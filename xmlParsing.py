import papery
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
            print('Year :', paper['Year'])
            print('Title :', paper['Title'])
            print('Author :', paper['Author'])
            print('Abstract :', paper['Abstract'])
            print('DOI :', paper['DOI'])
            print('URL :', paper['URL'])
            print('Citation Count :', paper['Citation Count'])
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

                paper = {
                    'Year' : self.getPubYear(jour),
                    'Title' : self.getTitle(arti),
                    'Author' : self.getAuthor(arti),
                    'Abstract' : self.getAbstract(arti),
                    'DOI' : self.getDOI(arti),
                    'URL' : self.getURL(arti),
                    'Citation Count' : self.getCitationCount(arti)
                }
                self.papers.append(paper)

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
            return '없음'
        else:
            return abst.text

    def getDOI(self, item):
        doi = item.find('doi')

        if doi.text is None:
            return '없음'
        else:
            return doi.text

    def getURL(self, item):
        url = item.find('url')

        if url.text is None:
            return '없음'
        else:
            return url.text

    def getCitationCount(self, item):
        cnt = item.find('citation-count')
        return cnt.text

if __name__ == '__main__':
    parser = xmlParsing(papery.KEY, "컴퓨터", papery.paperDataUrl, 1, 200)
    parser.parse()
    parser.printPapers()