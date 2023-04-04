import hashlib

import requests
from bs4 import BeautifulSoup
import re

def to_txt_file(string_list, link, article_name):
    with open('txt_files/'+hashlib.sha256(str(link).encode('utf-8')).hexdigest()+'.txt', 'w', encoding='utf-8') as f:
        f.write(article_name + '\n\n')
        for line in string_list:
            f.write(line+'\n')


articles_added = 0
current_page = 1

while articles_added < 200:
    url = 'https://ukrfootball.ua/news-football/?p='+str(current_page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    s = soup.find('div', class_='news_list_block')
    links = set(filter(lambda x: x.startswith('https://ukrfootball.ua'), list(map(lambda x: x.get('href'), s.find_all('a')))))

    current_page += 1

    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='tpl_one_news_mc_text_before htmlContent')
        article_name = soup.find('h1').get_text()
        if s:
            content = list(map(lambda x: x.get_text(), s.find_all('p')))
            to_txt_file(content, link, article_name)
            articles_added += 1