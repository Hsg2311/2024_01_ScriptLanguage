import os

KCI_PAPER_DATA_URL = 'https://open.kci.go.kr/po/openapi/openApiSearch.kci'
SCOPUS_SCOPUS_SEARCH_URL = 'https://api.elsevier.com/content/search/scopus'
SCOPUS_ABSTRACT_URL = 'http://api.elsevier.com/content/abstract/eid'
KCI_KEY = os.environ['PAPER_API_KCI_KEY']
SCOPUS_KEY = os.environ['PAPER_API_SCOPUS_KEY']
CACHE_PREFIX = 'cache/'

parseCnt = 100