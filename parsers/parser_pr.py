"""

    'pravda.com.ua' parser


"""

from bs4 import BeautifulSoup
import requests

def parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    article = soup.find('article', class_='post')

    data = {}
    if article.find('img', class_='post_photo_news_img'):
        data['preview'] = article.find('img', class_='post_photo_news_img').get('src')
    else:
        data['preview'] = None
    post_text = article.find('div', class_='post_text')
    data['content'] = []
    element = post_text.find('p')
    data['content'].append({'p': element.text.strip()})
    while element != None:
        element = element.find_next_sibling()
        if element == None:
            break
        if element.name == 'p':
            data['content'].append({'p': element.text.strip()})
        elif element.name == 'div' and 'image-box' in element['class']:
            img = element.find('img')
            if img == None:
                continue
            data['content'].append({'img': 'https:'+img.get('src')})
    return data
