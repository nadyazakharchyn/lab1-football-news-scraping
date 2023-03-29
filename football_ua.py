import requests
from bs4 import BeautifulSoup
import re


def to_txt_file(string_list, file_name):
    print(file_name)
    with open('txt_files/'+file_name.replace('\"', '').replace('/', '').replace(':', '').replace('?', '')+'.txt', 'w', encoding='utf-8') as f:
        for line in string_list:
            f.write(line+'\n')


articles_added = 0
current_page = 1

while articles_added < 200:
    url = 'https://football.ua/newsarc/page'+str(current_page)+'.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    s = soup.find('ul', class_='archive-list')

    links = set(filter(lambda x: x.startswith('https://football.ua'), list(map(lambda x: x.get('href'), s.find_all('a')))))

    current_page += 1

    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='article-text')
        article_name = soup.find('h1').get_text()
        if s:
            content = list(map(lambda x: x.get_text(), s.find_all('p')))
            to_txt_file(content, article_name)
            articles_added += 1
