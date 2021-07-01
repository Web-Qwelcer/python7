"""

    'epravda.com.ua' parser


"""

from bs4 import BeautifulSoup
import requests

def parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    article = soup.find('div', class_='article_content')
    data = {}
    x = article.find('div', class_='image-box image-box_center')
    data['preview'] = x.find('img').get('src')
    y = article.find('div', class_='post__text')
    data['content'] = []

    elem = y.find('p')
    data['content'].append({'p': elem.text.strip()})
    while elem != None:
        elem = elem.find_next_sibling()
        if elem == None:
            break
        if elem.name == 'p':
            data['content'].append({'p': elem.text})
        elif elem.name == 'div' and 'image-box' in elem['class']:
            print()
            img = elem.find('img')
            if img == None:
                continue
            data['content'].append({'img': 'https:' + img.get('src')})
    return data
