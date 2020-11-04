import requests
from bs4 import BeautifulSoup as bs
import os
from datetime import date
import aiohttp

articles_ids = []


def get_links(path):
    check_file(path)
    article_links = []
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    base_url = 'https://habr.com/ru/all/page'
    i = 1
    while i <= 3:
        url = base_url + str(i)
        try:
            get_page = requests.get(url, headers=headers)
            if get_page.status_code == 200:
                article_links += parse_page(get_page.text.encode('utf-8'))
                i += 1
            else:
                break
        except Exception as e:
            print(e)
    rewrite_ids()
    return article_links


def parse_page(page_html):
    page_links = []
    bs_obj: bs = bs(page_html, 'html.parser')
    bs_articles = bs_obj.find_all('article', {'class': 'post post_preview'})
    for article in bs_articles:
        bs_titles = article.find_all('a', {'class': 'post__title_link'})
        for a in bs_titles:
            post_link = article.find('a', {'class': 'post__title_link'})
            post_body = article.find('div', {'class': 'post__body post__body_crop'})
            post_preview = post_body.find('div', {'class': 'post__text'})
            try:
                image = post_body.find('img').get('src')
            except Exception as e:
                image = 'None'
            if post_link.get('href') not in articles_ids:
                articles_ids.append(post_link.get('href'))
                article_link = []
                article_link.append(post_link.get('href'))
                article_link.append(post_link.text.strip())
                if len(post_preview.text.strip()) + len(post_link.get('href')) + len(post_link.text.strip()) > 1013:
                    maxlength = 1010 - len(post_link.get('href')) - len(post_link.text.strip())
                    post_preview_text = post_preview.text.strip()[:maxlength] + '...'
                else:
                    post_preview_text = post_preview.text.strip()
                article_link.append(post_preview_text)
                article_link.append(image)
                page_links.append(article_link)
    return page_links


def rewrite_ids():
    file_name = get_filename()
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(';'.join(articles_ids))


def get_filename():
    date_today = date.today()
    filename = date_today.strftime('%Y%m%d') + 'ids.txt'
    return filename


def check_file(dir_name):
    global articles_ids
    file_name = get_filename()
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            articles_ids = f.read().split(';')
    else:
        _delete_ids(dir_name)
        with open(file_name, 'w', encoding='utf-8') as f:
            pass


def _delete_ids(dir_name):
    for root, dirs, names in os.walk(dir_name):
        for name in names:
            if 'ids.txt' in name:
                os.remove(os.path.join(root, name))
