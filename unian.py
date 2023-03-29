import requests
from bs4 import BeautifulSoup
import re


def to_txt_file(string_list, file_name):
    print(file_name)
    with open('txt_files/'+re.sub('[^A-Za-zА-Яа-я0-9 ]+', '', file_name)+'.txt', 'w', encoding='utf-8') as f:
        for line in string_list:
            f.write(line+'\n')


for i in range(1, 10):
    url = 'https://sport.unian.ua/football?page=' + str(i)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    s = soup.find('div', class_='list-thumbs')

    links = set(filter(lambda x: x.startswith('https://sport.unian.ua/'), list(map(lambda x: x.get('href'), s.find_all('a')))))

    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='article-text')
        article_name = soup.find('h1').get_text()
        if s:
            content = list(map(lambda x: x.get_text(), s.find_all('p')))
            to_txt_file(content, article_name)