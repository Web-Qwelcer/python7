"""

    'life.pravda.com.ua' parser

    
"""

from bs4 import BeautifulSoup
import requests

def parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = {}
    data['title'] = soup.find('h1', class_='page-heading').text
    article = soup.find('article', class_='article')
    elem = article.find('p')
    data['content'] = []
    data['content'].append({'p': elem.text.strip()})

    while elem != None:
        elem = elem.find_next_sibling()
        if elem == None:
            break
        if elem.name == 'p':
            data['content'].append({'p': elem.text.strip()})
        elif elem.name == 'table':
            data['content'].append(
                {'img': 'https://life.pravda.com.ua' + elem.find('img').get('src')})
        elif elem.name == 'blockquote':
            data['content'].append({'blockquote': elem.text.strip()})
        elif elem.name == 'ul':
            data['content'].append({'li': elem.text.strip()})
    return data
