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

    def __init__(self, searchStr, searchMode, basePage, parseCnt
    ):
        self.papers = []
        self.__searchStr = searchStr
        self.__key = papery.KEY
        self.__paperDataURL = papery.paperDataUrl
        self.__basePage = basePage
        self.__cnt = parseCnt
        self.__pages = []
        self.__details = []
        self.__searchMode = searchMode

    # short for internet search
    def isearch(self, willCache=True):
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
        
        if not willCache:
            return self.__pages
        
        for i, xml in enumerate(self.__pages):
            path = papery.CACHE_PREFIX + self.__searchStr + '.xml' + str(i)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(xml)

        return self.__pages

    # short for file search
    # expect the file to be named as @.xml#
    # where @ is the search string and # is the page number
    def fsearch(self):
        i = 0
        while True:
            file_path = papery.CACHE_PREFIX + self.__searchStr + '.xml' + str(i)

            if os.path.isfile(file_path):
                self.__pages.append( open(file_path, 'r', encoding='utf-8').read() )
            else:
                break

            i += 1

        return self.__pages if len(self.__pages) > 0 else None
    
    def search(self, willCache=True):
        fResult = self.fsearch()
        if fResult is not None:
            return fResult
        
        return self.isearch(willCache)

    # one-based index
    def __getPage(self, idx):
        return self.__pages[idx - self.__basePage]

    def isearchAndParse(self, willCache=True):
        self.isearch(willCache)
        return self.parse()

    def fsearchAndParse(self):
        self.fsearch()
        return self.parse()
    
    def searchAndParse(self, willCache=True):
        self.search(willCache)
        return self.parse()

    def parse(self):
        for page in self.__pages:
            root = ET.fromstring(page)

            for item in root.iter('record'):
                jour = item.find('journalInfo')
                arti = item.find('articleInfo')

                self.papers.append( PageParseResult(
                    self.__getArticleID(arti),
                    self.__getTitle(arti),
                    self.__getAuthorNames(arti),
                    self.__getPubYear(jour),
                    self.__getAbstract(arti),
                    self.__getJournal(jour),
                    self.__getInstitution(jour),
                    self.__getVolume(jour),
                    self.__getIssue(jour),
                    self.__getDOI(arti),
                    self.__getURL(arti),
                    self.__getCitationCount(arti)
                ) )

        return self.papers

    def __getItem(self, item, tag):
        tag = item.find(tag)
        return tag.text if tag is not None else None
    
    def __getArticleID(self, item):
        return item.attrib['article-id']

    def __getPubYear(self, item):
        return self.__getItem(item, 'pub-year')
    
    def __getTitle(self, item):
        title_group = item.find('title-group')
        article_title = title_group.find('article-title')
        return article_title.text
    
    def __getAuthorNames(self, item):
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
        return self.__getItem(item, 'journal-name')
    
    def __getVolume(self, item):
        return self.__getItem(item, 'volume')
    
    def __getIssue(self, item):
        return self.__getItem(item, 'issue')
    
    def __getInstitution(self, item):
        return self.__getItem(item, 'publisher-name')
    
class PageParseResult:
    def __init__(self, articleID, title, authors,
        year, abstract ,journal, institution,
        volume, issue, doi, url, citationCnt
    ):
        self.articleID = articleID
        self.title = title
        self.authors = authors
        self.year = year
        self.abstract = abstract
        self.journal = journal
        self.institution = institution
        self.volume = volume
        self.issue = issue
        self.doi = doi
        self.url = url
        self.citationCnt = citationCnt

    def reflect(self, paper):
        paper.title = self.title
        paper.authors = self.authors
        paper.year = self.year
        paper.abstract = self.abstract
        paper.journal = self.journal
        paper.institution = self.institution
        paper.volume = self.volume
        paper.issue = self.issue
        paper.doi = self.doi
        paper.url = self.url
        paper.citationCnt = self.citationCnt
        paper.articleID = self.articleID

class DetailParser:
    def __init__(self, articleID):
        self.__key = papery.KEY
        self.__paperDataURL = papery.paperDataUrl
        self.__articleID = articleID
        self.__detail = None

    # short for internet search
    def isearch(self, willCache=True):
        params = {'key' : self.__key, 'apiCode' : 'articleDetail',
            'id' : self.__articleID
        }
        self.__detail = requests.get(self.__paperDataURL, params=params).text

        if not willCache:
            return self.__detail
        
        with open(papery.CACHE_PREFIX + self.__articleID + '.xml', 'w', encoding='utf-8') as f:
            f.write(self.__detail)

        return self.__detail
    
    # short for file search
    # expect the file to be named as #.xml
    # where # is the article ID
    def fsearch(self):
        file_path = papery.CACHE_PREFIX + self.__articleID + '.xml'

        if os.path.isfile(file_path):
            self.__detail = open(file_path, 'r', encoding='utf-8').read()

        return self.__detail if self.__detail is not None else None
    
    def search(self, willCache=True):
        fResult = self.fsearch()
        if fResult is not None:
            return fResult
        
        return self.isearch(willCache)
    
    def parse(self):
        refs = []
        keywords = []
        authorInsts = []

        root = ET.fromstring(self.__detail)
        for item in root.iter('record'):
            arti = item.find('articleInfo')
            ref = item.find('referenceInfo')

            refs.extend( self.__getRefs(ref) )
            keywords.extend( self.__getKeywords(arti) )
            authorInsts.extend( self.__getAuthorInsts(arti) )

        return DetailParseResult(keywords, refs, authorInsts)

    def isearchAndParse(self, willCache=True):
        self.isearch(willCache)
        return self.parse()
    
    def fsearchAndParse(self):
        self.fsearch()
        return self.parse()
    
    def searchAndParse(self, willCache=True):
        self.search(willCache)
        return self.parse()
    
    def __getItem(self, item, tag):
        tag = item.find(tag)
        return tag.text if tag is not None else None
    
    def __getKeywords(self, item):
        result = []
        keyword_group = item.find('keyword-group')
        for keyword in keyword_group.findall('keyword'):
            result.append(keyword.text)
        return result
    
    def __getRefs(self, item):
        refs = []

        for ref_item in item.findall('reference'):
            titleObj = ref_item.find('title')
            if titleObj is not None:
                refs.append( ref_item.attrib['type-name'] + ' | ' + titleObj.text )
            else:
                refs.append( ref_item.attrib['type-name'] + ' | ' + ref_item.text )

        return refs if len(refs) > 0 else None
    
    def __getAuthorInsts(self, item):
        result = []
        author_group = item.find('author-group')

        for author in author_group.findall('author'):
            result.append( author.find('institution').text )
        
        return result
    
class DetailParseResult:
    def __init__(self, keywords, refs, authorInsts):
        self.keywords = keywords
        self.refs = refs
        self.authorInsts = authorInsts

    def reflect(self, paper):
        paper.keywords = self.keywords
        paper.refs = self.refs
        paper.authorInsts = self.authorInsts

if __name__ == '__main__':
    r = DetailParser('ART001564843').isearchAndParse()
    print('keywords:', r.keywords)
    print('references:', r.refs)
    print('author institutions:', r.authorInsts)