import requests
from bs4 import BeautifulSoup
import re


def to_txt_file(string_list, file_name):
    print(file_name)
    with open('txt_files/'+file_name.replace('\"', '').replace('/', '').replace(':', '').replace('?', '')+'.txt', 'w', encoding='utf-8') as f:
        for line in string_list:
            f.write(line+'\n')


for i in range(1, 10):
    url = 'https://ua.tribuna.com/uk/football/news/page'+str(i)+'/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    s = soup.find('div', class_=re.compile("^NewsFeed_news-feed__news"))
    links = set(map(lambda x: 'https://ua.tribuna.com'+x.get('href'), s.find_all('a')))
    for link in links:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html.parser')
            s = soup.find('div', class_='card__content')
            article_name = soup.find(class_='header__title').get_text()
            if s:
                content = list(map(lambda x: x.get_text(), s.find_all('p')))
                to_txt_file(content, article_name)
        except Exception as ex:
            print("Oh shit: "+link)
            print(ex)