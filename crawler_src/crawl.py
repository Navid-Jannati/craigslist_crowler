import json
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from config import BASE_LINK


class CrawlerBase(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass


class LinkCrawler(CrawlerBase):

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link

    def get_page(self, url, start):
        try:
            res = requests.get(url + str(start))
        except:
            return None
        return res

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.find_all('a', attrs={'class': 'hdrlnk'})

    def start_crawl_city(self, url):
        start = 0
        crawl = True
        adv_links = list()
        while crawl:
            response = self.get_page(url, start)
            new_links = self.find_links(response.text)
            adv_links.extend(new_links)
            start += 120
            crawl = bool(len(new_links))
        return adv_links

    def start(self):
        adv_links = list()
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            print(f'city: {city}, total: {len(links)}')
            adv_links.extend(links)
        self.store([li.get('href') for li in adv_links])

    def store(self, data):
        with open('data/links.json', 'w') as file:
            file.write(json.dumps(data))


class DataCrawler(CrawlerBase):
    pass
