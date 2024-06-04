import pybliometrics.scopus
import papery
from paper import Paper
import xml.etree.ElementTree as ET
import requests
import os

import pybliometrics
from pybliometrics.scopus import ScopusSearch

class KCIPageParser:
    TITLE_MODE = 0
    AUTHOR_MODE = 1
    JOURNAL_MODE = 2
    INSTITUTION_MODE = 3
    PAGE_SIZE = 100

    def __init__(self, searchStr, searchMode, basePage, parseCnt):
        self.__searchStr = searchStr
        self.__searchMode = searchMode
        self.__basePage = basePage
        self.__key = papery.KCI_KEY
        self.__paperDataURL = papery.KCI_PAPER_DATA_URL
        self.__pages = []
        self.results = []
        self.__cnt = parseCnt

    # short for file search
    # expect the file to be named as @.xml#
    # where @ is the search string and # is the page number
    def fsearch(self):
        i = 0
        while True:
            if self.__searchMode == self.TITLE_MODE:
                file_path = papery.CACHE_PREFIX + 'kci/title/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.AUTHOR_MODE:
                file_path = papery.CACHE_PREFIX + 'kci/author/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.JOURNAL_MODE:
                file_path = papery.CACHE_PREFIX + 'kci/journal/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.INSTITUTION_MODE:
                file_path = papery.CACHE_PREFIX + 'kci/institution/' + self.__searchStr + '.xml' + str(i)
            else:
                raise ValueError('Invalid search mode')

            if os.path.isfile(file_path):
                self.__pages.append( open(file_path, 'r', encoding='utf-8').read() )
            else:
                break

            i += 1

        return self.__pages if len(self.__pages) > 0 else None

    # short for internet search
    def isearch(self, willCache=True):
        for i in range(0, self.__cnt // KCIPageParser.PAGE_SIZE):
            params = {'key' : self.__key, 'apiCode' : 'articleSearch',
                'page' : self.__basePage + i, 'displayCount' : KCIPageParser.PAGE_SIZE          
            }

            if self.__searchMode == self.TITLE_MODE:
                params['title'] = self.__searchStr
            elif self.__searchMode == self.AUTHOR_MODE:
                params['author'] = self.__searchStr
            elif self.__searchMode == self.JOURNAL_MODE:
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
            if self.__searchMode == self.TITLE_MODE:
                path = papery.CACHE_PREFIX + 'kci/title/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.AUTHOR_MODE:
                path = papery.CACHE_PREFIX + 'kci/author/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.JOURNAL_MODE:
                path = papery.CACHE_PREFIX + 'kci/journal/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.INSTITUTION_MODE:
                path = papery.CACHE_PREFIX + 'kci/institution/' + self.__searchStr + '.xml' + str(i)
            else:
                raise ValueError('Invalid search mode')

            with open(path, 'w', encoding='utf-8') as f:
                f.write(xml)

        return self.__pages
    
    def search(self, willCache=True):
        fResult = self.fsearch()
        if fResult is not None:
            return fResult
        
        return self.isearch(willCache)
    
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

                self.results.append( KCIPageParseResult(
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

        return self.results
    
    # one-based index
    def __getPage(self, idx):
        return self.__pages[idx - self.__basePage]

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
    
class ScopusPageParser:
    TITLE_MODE = 0
    AUTHOR_MODE = 1
    JOURNAL_MODE = 2
    INSTITUTION_MODE = 3
    PAGE_SIZE = 20

    XML_NAMESPACES = {
        'atom': 'http://www.w3.org/2005/Atom',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
        'prism': 'http://prismstandard.org/namespaces/basic/2.0/'
    }

    def __init__(self, searchStr, searchMode, basePage, parseCnt):
        self.__searchStr = searchStr
        self.__searchMode = searchMode
        self.__basePage = basePage
        self.__key = papery.SCOPUS_KEY
        self.__paperDataURL = papery.SCOPUS_SCOPUS_SEARCH_URL
        self.__pages = []
        self.results = []
        self.__cnt = parseCnt

    # short for file search
    # expect the file to be named as @.xml#
    # where @ is the search string and # is the page number
    def fsearch(self):
        i = 0
        while True:
            if self.__searchMode == self.TITLE_MODE:
                file_path = papery.CACHE_PREFIX + 'scopus/title/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.AUTHOR_MODE:
                file_path = papery.CACHE_PREFIX + 'scopus/author/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.JOURNAL_MODE:
                file_path = papery.CACHE_PREFIX + 'scopus/journal/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.INSTITUTION_MODE:
                file_path = papery.CACHE_PREFIX + 'scopus/institution/' + self.__searchStr + '.xml' + str(i)
            else:
                raise ValueError('Invalid search mode')

            if os.path.isfile(file_path):
                self.__pages.append( open(file_path, 'r', encoding='utf-8').read() )
            else:
                break

            i += 1

        return self.__pages if len(self.__pages) > 0 else None
    
    # short for internet search
    def isearch(self, willCache=True):
        for i in range(self.__cnt // ScopusPageParser.PAGE_SIZE):
            params = { 'httpAccept':'application/xml', 'apiKey': self.__key,
                'start': (self.__basePage + i) * ScopusPageParser.PAGE_SIZE,
                'count': ScopusPageParser.PAGE_SIZE
            }

            if self.__searchMode == self.TITLE_MODE:
                params['query'] = 'TITLE("' + self.__searchStr + '")'
            elif self.__searchMode == self.AUTHOR_MODE:
                params['query'] = 'AUTH("' + self.__searchStr + '")'
            elif self.__searchMode == self.JOURNAL_MODE:
                params['query'] = 'SRCTITLE("' + self.__searchStr + '")'
            elif self.__searchMode == self.INSTITUTION_MODE:
                params['query'] = 'AFFIL("' + self.__searchStr + '")'
            else:
                raise ValueError('Invalid search mode')

            self.__pages.append( requests.get(self.__paperDataURL, params=params).text )
        
        if not willCache:
            return self.__pages
        
        for i, xml in enumerate(self.__pages):
            if self.__searchMode == self.TITLE_MODE:
                path = papery.CACHE_PREFIX + 'scopus/title/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.AUTHOR_MODE:
                path = papery.CACHE_PREFIX + 'scopus/author/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.JOURNAL_MODE:
                path = papery.CACHE_PREFIX + 'scopus/journal/' + self.__searchStr + '.xml' + str(i)
            elif self.__searchMode == self.INSTITUTION_MODE:
                path = papery.CACHE_PREFIX + 'scopus/institution/' + self.__searchStr + '.xml' + str(i)
            else:
                raise ValueError('Invalid search mode')
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(xml)

        return self.__pages
    
    def search(self, willCache=True):
        fResult = self.fsearch()
        if fResult is not None:
            return fResult
        
        return self.isearch(willCache)
    
    def parse(self):
        for page in self.__pages:
            root = ET.fromstring(page)

            for item in root.findall('atom:entry', ScopusPageParser.XML_NAMESPACES):
                self.results.append( ScopusPageParseResult(
                    articleID=self.__getArticleID(item),
                    title=self.__getTitle(item),
                    authors=self.__getAuthorNames(item),
                    year=self.__getPubYear(item),
                    journal=self.__getJournal(item),
                    institution=self.__getInstitution(item),
                    volume=self.__getVolume(item),
                    issue=self.__getIssue(item),
                    doi=self.__getDOI(item),
                    url=None,
                    citationCnt=self.__getCitationCount(item)
                ) )

        return self.results
    
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
        tag = item.find(tag, ScopusPageParser.XML_NAMESPACES)
        return tag.text if tag is not None else None

    def __getArticleID(self, entry):
        return self.__getItem(entry, 'atom:eid')
    
    def __getTitle(self, entry):
        return self.__getItem(entry, 'dc:title')
    
    def __getAuthorNames(self, entry):
        return self.__getItem(entry, 'dc:creator')
    
    def __getPubYear(self, entry):
        return self.__getItem(entry, 'prism:coverDate')
    
    def __getJournal(self, entry):
        return self.__getItem(entry, 'prism:publicationName')
    
    def __getInstitution(self, entry):
        affList = entry.findall('atom:affiliation', ScopusPageParser.XML_NAMESPACES)

        for aff in affList:
            affName = aff.find('atom:affilname', ScopusPageParser.XML_NAMESPACES)
            if affName is not None:
                return affName.text
            
        return None
    
    def __getVolume(self, entry):
        return self.__getItem(entry, 'prism:volume')
    
    def __getIssue(self, entry):
        return self.__getItem(entry, 'prism:issueIdentifier')
    
    def __getDOI(self, entry):
        return self.__getItem(entry, 'prism:doi')
    
    def __getCitationCount(self, entry):
        return self.__getItem(entry, 'atom:citedby-count')
    

class PageParser:
    KCI = 'KCI'
    SCOPUS = 'Scopus'
    TITLE_MODE = 0
    AUTHOR_MODE = 1
    JOURNAL_MODE = 2
    INSTITUTION_MODE = 3

    def __init__(self, searchStr, searchMode, basePage, parseCnt, source=KCI):
        self.__KCIParser = KCIPageParser(searchStr, searchMode, basePage, parseCnt)
        self.__source = source

    def isearch(self, willCache=True):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.isearch(willCache)
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')

    # short for file search
    # expect the file to be named as @.xml#
    # where @ is the search string and # is the page number
    def fsearch(self):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.fsearch()
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def search(self, willCache=True):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.search(willCache)
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def parse(self):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.parse()
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def isearchAndParse(self, willCache=True):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.isearchAndParse(willCache)
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def fsearchAndParse(self):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.fsearchAndParse()
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def searchAndParse(self, willCache=True):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.searchAndParse(willCache)
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')

    def getResults(self):
        if self.__source == PageParser.KCI:
            return self.__KCIParser.results
        elif self.__source == PageParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
class KCIPageParseResult:
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

class ScopusPageParseResult:
    def __init__(self, articleID, title, authors,
        year, journal, institution,
        volume, issue, doi, citationCnt
    ):
        self.articleID = articleID
        self.title = title
        self.authors = authors
        self.year = year
        self.journal = journal
        self.institution = institution
        self.volume = volume
        self.issue = issue
        self.doi = doi
        self.citationCnt = citationCnt

    def reflect(self, paper):
        paper.title = self.title
        paper.authors = self.authors
        paper.year = self.year
        paper.journal = self.journal
        paper.institution = self.institution
        paper.volume = self.volume
        paper.issue = self.issue
        paper.doi = self.doi
        paper.citationCnt = self.citationCnt
        paper.articleID = self.articleID

class KCIDetailParser:
    def __init__(self, articleID):
        self.__key = papery.KCI_KEY
        self.__paperDataURL = papery.KCI_PAPER_DATA_URL
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
        
        with open(papery.CACHE_PREFIX + 'kci/detail/' + self.__articleID + '.xml', 'w', encoding='utf-8') as f:
            f.write(self.__detail)

        return self.__detail
    
    # short for file search
    # expect the file to be named as #.xml
    # where # is the article ID
    def fsearch(self):
        file_path = papery.CACHE_PREFIX + 'kci/detail/' + self.__articleID + '.xml'

        if os.path.isfile(file_path):
            self.__detail = open(file_path, 'r', encoding='utf-8').read()

        return self.__detail
    
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

        return KCIDetailParseResult(keywords, refs, authorInsts)

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
    
class ScopusDetailParser:
    XML_NAMESPACES = {
        'dn': 'http://www.elsevier.com/xml/svapi/abstract/dtd',
        'ait': 'http://www.elsevier.com/xml/ani/ait',
        'ce': 'http://www.elsevier.com/xml/ani/common',
        'cto': 'http://www.elsevier.com/xml/cto/dtd',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'prism': 'http://prismstandard.org/namespaces/basic/2.0/',
        'xocs': 'http://www.elsevier.com/xml/xocs/dtd',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    def __init__(self, articleID):
        self.__articleID = articleID
        self.__detail = None

    def isearch(self, willCache=True):
        params = { 'httpAccept':'text/xml', 'apiKey': papery.SCOPUS_KEY}
        self.__detail = requests.get(
            papery.SCOPUS_ABSTRACT_URL + '/' + self.__articleID, params=params
        ).text

        if not willCache:
            return self.__detail
        
        with open(papery.CACHE_PREFIX + 'scopus/abstract/' + self.__articleID + '.xml', 'w', encoding='utf-8') as f:
            f.write(self.__detail)

        return self.__detail
    
    def fsearch(self):
        file_path = papery.CACHE_PREFIX + 'scopus/abstract/' + self.__articleID + '.xml'

        if os.path.isfile(file_path):
            self.__detail = open(file_path, 'r', encoding='utf-8').read()

        return self.__detail
    
    def search(self, willCache=True):
        fResult = self.fsearch()
        if fResult is not None:
            return fResult
        
        return self.isearch(willCache)
    
    def parse(self):
        refs = []
        keywords = []
        authorInsts = []
        abstract = None

        root = ET.fromstring(self.__detail)
        coredata = root.find('db:coredata', ScopusDetailParser.XML_NAMESPACES)
        keywords = self.__getKeywords(coredata)
        authorInsts = self.__getAuthorInsts(coredata)
        abstract = self.__getAbstract(coredata)
        refs = self.__getRefs(root)

        return ScopusDetailParseResult(abstract, keywords, refs, authorInsts)
    
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
        tag = item.find(tag, ScopusDetailParser.XML_NAMESPACES)
        return tag.text if tag is not None else None
    
    def __getKeywords(self, item):
        pass
    
    def __getRefs(self, item):
        pass
    
    def __getAuthorInsts(self, item):
        pass
    
    def __getAbstract(self, item):
        return self.__getItem(item, 'dc:description')
    
class DetailParser:
    KCI = 'KCI'
    SCOPUS = 'Scopus'

    def __init__(self, articleID, source=KCI):
        self.__KCIDetailParser = KCIDetailParser(articleID)
        self.__source = source

    def fsearch(self):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.fsearch()
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')

    def isearch(self, willCache=True):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.isearch(willCache)
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def parse(self):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.parse()
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def isearchAndParse(self, willCache=True):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.isearchAndParse(willCache)
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')

    def fsearchAndParse(self):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.fsearchAndParse()
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')

    def searchAndParse(self, willCache=True):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.searchAndParse(willCache)
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
    def getResults(self):
        if self.__source == DetailParser.KCI:
            return self.__KCIDetailParser.results
        elif self.__source == DetailParser.SCOPUS:
            return None
        raise ValueError('Invalid source')
    
class KCIDetailParseResult:
    def __init__(self, keywords, refs, authorInsts):
        self.keywords = keywords
        self.refs = refs
        self.authorInsts = authorInsts

    def reflect(self, paper):
        paper.keywords = self.keywords
        paper.refs = self.refs
        paper.authorInsts = self.authorInsts

class ScopusDetailParseResult:
    def __init__(self, abstract, keywords, refs, authorInsts):
        self.abstract = abstract
        self.keywords = keywords
        self.refs = refs
        self.authorInsts = authorInsts

    def reflect(self, paper):
        paper.abstract = self.abstract
        paper.keywords = self.keywords
        paper.refs = self.refs
        paper.authorInsts = self.authorInsts

if __name__ == '__main__':
    # r = DetailParser('ART001564843').isearchAndParse()
    # print('keywords:', r.keywords)
    # print('references:', r.refs)
    # print('author institutions:', r.authorInsts)

    r = ScopusDetailParser('2-s2.0-85192867679').isearch()