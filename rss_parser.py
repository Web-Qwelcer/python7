from feedparser import *
from pprint import pprint
from datetime import datetime
from time import mktime
import json
from parsers.parser_pr import parse as parser_pr
from parsers.parser_epr import parse as parser_epr
from parsers.parser_eipr import parse as parser_eipr
from parsers.parser_lpr import parse as parser_lpr

RSS_URL = 'https://www.pravda.com.ua/rss/view_news/'
feed = parse(RSS_URL)
urls = [
    'pravda.com.ua',
    'eurointegration.com.ua',
    'life.pravda.com.ua',
    'epravda.com.ua'
]
news = []

for item in feed.entries:
    data = {}
    data['title'] = item.title
    data['description'] = item.summary
    data['url'] = item.link
    data['date'] = f'{item.published_parsed[2]}-{item.published_parsed[1]}-{item.published_parsed[0]}  {item.published_parsed[3]}:{item.published_parsed[4]}:{item.published_parsed[5]}'
    if data['url'].split('/')[2][4:] == urls[0]:
        data.update(parser_pr(data['url']))
    elif data['url'].split('/')[2][4:] == urls[3]:
        data.update(parser_epr(data['url']))
    elif data['url'].split('/')[2][0:] == urls[2]:
        data.update(parser_lpr(data['url']))
    elif data['url'].split('/')[2][0:] == urls[1]:
        data.update(parser_eipr(data['url']))
    news.append(data)

with open('news.json', 'w', encoding='utf8') as file:
    json.dump(news, file, indent=4, ensure_ascii=False)
    file.close()
