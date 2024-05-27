import paper
import sys
import xml.etree.ElementTree as ET
import requests

papers = []
for i in range(1, 21):
    testParams = {'serviceKey' : paper.KEY, 'recordCnt' : 2, 'pageNo' : i}
    response = requests.get(paper.paperDataUrl, params=testParams)
    
    root = ET.fromstring(response.text)

    for item in root.iter('item'):
        paper = {
            'Title' : item.findtext('ARTI_KOR_TITL'),
            'Abst' : item.findtext('KOR_ABST')
        }
        papers.append(paper)

for paper in papers:
    print('Title :', paper['Title'])
    print('Abstract :', paper['Abst'])
    print()
