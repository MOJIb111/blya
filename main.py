import time
import requests
from bs4 import BeautifulSoup as B
from datetime import datetime
import pickle

class Article:
    
    @classmethod
    def __init__(cls, title, desc, url, time, id):
        cls.title = title
        cls.desc = desc
        cls.url = url
        cls.time = time
        cls.id = id
    @classmethod
    def __getstate__(cls) -> dict:
        '''Метод для записи атрибутов класса в файл'''
        state = {}
        state['title'] = cls.title
        state['desc'] = cls.desc
        state['url'] = cls.url
        state['time'] = cls.time
        state['id'] = cls.id
        return state
    @classmethod
    def __setstate__(cls, state:dict):
        '''Метод для восстановления класса из байтов'''
        cls.title = state['title']
        cls.desc = state['desc']
        cls.url = state['url']
        cls.time = state['time']
        cls.id = state['id']

def get_first():
    '''Собирает первую партию новостей в объект'''
    heads = {
        "User-Agent" :
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
    }

    URL = "https://habr.com/ru/search/?q=python&target_type=posts&order=date"
    r = requests.get(url=URL, headers=heads)

    soup = B(r.text, "lxml")
    articles = soup.find_all("article", class_="tm-articles-list__item")

    for article in articles:
        Article.title = article.find("h2", class_="tm-title").text
        Article.desc = article.find(class_="tm-article-body").text
        Article.url = f'https://habr.com{article.find("h2").find("a").get("href")}'

        article_date_time = article.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
        Article.time = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

        Article.id = Article.url.split("/")
        Article.id = Article.id[-2]
        Article.__getstate__()
        
        with open('News.pkl', 'wb') as fp:
            pickle.dump(Article, fp)
            
            
def check_news_upd():
    with open("news_dict.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    heads = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
    }

    URL = "https://habr.com/ru/search/?q=python&target_type=posts&order=date"
    r = requests.get(url=URL, headers=heads)

    soup = B(r.text, "lxml")
    articles = soup.find_all("article", class_="tm-articles-list__item")

    fresh_news = {}
    for article in articles:
        article_url = f'https://habr.com{article.find("h2").find("a").get("href")}'
        article_id = article_url.split("/")
        article_id = article_id[-2]

        if article_id in news_dict:
            continue

        else:
            article_title = article.find("h2", class_="tm-title").text
            article_desc = article.find(class_="tm-article-body").text


            article_date_time = article.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_desc": article_desc,
                "article_url": article_url
            }
            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_desc": article_desc,
                "article_url": article_url
            }

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    return fresh_news

def main():
    check_news_upd()

if __name__ == '__main__':
    main()