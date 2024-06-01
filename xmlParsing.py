import papery
from paper import Paper
import xml.etree.ElementTree as ET
import requests
import os

class PageParser:
    TITLE_MODE = 0
    AUTHOR_MODE = 1
    JORNAL_MODE = 2
    INSTITUTION_MODE = 3

    def __init__(self, apiKey, searchStr, searchMode,
        paperDataURL, basePage, parseCnt
    ):
        self.papers = []
        self.__searchStr = searchStr
        self.__key = apiKey
        self.__paperDataURL = paperDataURL
        self.__basePage = basePage
        self.__cnt = parseCnt
        self.__pages = []
        self.__details = []
        self.__searchMode = searchMode

    # short for internet search
    def isearch(self):
        for i in range(0, self.__cnt // 100):
            params = {'key' : self.__key, 'apiCode' : 'articleSearch',
                'page' : self.__basePage + i, 'displayCount' : 100          
            }

            if self.__searchMode == self.TITLE_MODE:
                params['title'] = self.__searchStr
            elif self.__searchMode == self.AUTHOR_MODE:
                params['author'] = self.__searchStr
            elif self.__searchMode == self.JORNAL_MODE:
                params['journal'] = self.__searchStr
            elif self.__searchMode == self.INSTITUTION_MODE:
                params['institution'] = self.__searchStr
            else:
                raise ValueError('Invalid search mode')
            
            self.__pages.append(
                 requests.get(self.__paperDataURL, params=params).text
            )
        
        return self.__pages

    # short for file search
    def fsearch(self):
        i = 0
        while True:
            file_path = self.__searchStr + str(i)

            if os.path.isfile(file_path):
                self.__pages.append( open(file_path, 'r', encoding='utf-8').read() )
            else:
                break

            i += 1

        return self.__pages

    # one-based index
    def __getPage(self, idx):
        return self.__pages[idx - self.__basePage]

    def iSearchAndParse(self):
        self.isearch()
        return self.parse()

    def fSearchAndParse(self):
        self.fsearch()
        return self.parse()

    def parse(self):
        for page in self.__pages:
            root = ET.fromstring(page)

            for item in root.iter('record'):
                jour = item.find('journalInfo')
                arti = item.find('articleInfo')

                self.papers.append(
                        Paper(title=self.__getTitle(arti),
                        author=', '.join( self.__getAuthor(arti) ),
                        year=self.__getPubYear(jour),
                        school='',
                        doi=self.__getDOI(arti),
                        url=self.__getURL(arti),
                        abstract=self.__getAbstract(arti),
                        citationCnt=self.__getCitationCount(arti)
                    )
                )

        return self.papers

    def __getItem(self, item, tag):
        tag = item.find(tag)
        return tag.text if tag is not None else None
    
    def __getPubYear(self, item):
        return self.__getItem(item, 'pub-year')
    
    def __getTitle(self, item):
        title_group = item.find('title-group')
        article_title = title_group.find('article-title')
        return article_title.text
    
    def __getAuthor(self, item):
        result = []
        author_group = item.find('author-group')
        for author in author_group.findall('author'):
            result.append(author.text)
        return result
    
    def __getAbstract(self, item):
        abst_group = item.find('abstract-group')
        return self.__getItem(abst_group, 'abstract')
    
    def __getDOI(self, item):
        return self.__getItem(item, 'doi')
    
    def __getURL(self, item):
        return self.__getItem(item, 'url')
    
    def __getCitationCount(self, item):
        return self.__getItem(item, 'citation-count')
    
    def __getJournal(self, item):
        return self.__getItem(item, 'journal')
    
    def __getVolume(self, item):
        return self.__getItem(item, 'volume')
    
    def __getIssue(self, item):
        return self.__getItem(item, 'issue')

    # TODO: Add DetailParser Class and implement the following methods

    # def __searchDetail(self, articleId):
    #     params = {'key' : self.__key, 'apiCode' : 'articleDetail',
    #         'id' : articleId
    #     }
    #     self.__details.append(
    #         requests.get(self.__paperDataURL, params=params)
    #     )

    #     # one-based index
    # def __getDetail(self, idx):
    #     return self.__details[idx - (self.__basePage - 1) * 100 - 1]

if __name__ == '__main__':
    xmls = PageParser(papery.KEY, "사랑", PageParser.TITLE_MODE, papery.paperDataUrl, 1, 300).isearch()
    for i, xml in enumerate(xmls):
        with open("사랑.xml" + str(i), 'w', encoding='utf-8') as f:
            f.write(xml)