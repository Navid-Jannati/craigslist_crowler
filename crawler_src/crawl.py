import json
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from config import BASE_LINK
from parser import AdvertisementPageParser


class CrawlerBase(ABC):
    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data, file_name=None):
        pass

    @staticmethod
    def get(link):
        try:
            res = requests.get(link)
        except requests.HTTPError:
            return None
        return res


class LinkCrawler(CrawlerBase):

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.find_all('a', attrs={'class': 'hdrlnk'})

    def start_crawl_city(self, url):
        start = 0
        crawl = True
        adv_links = list()
        while crawl:
            response = self.get(url + start)
            new_links = self.find_links(response.text)
            adv_links.extend(new_links)
            start += 120
            crawl = bool(len(new_links))
        return adv_links

    def start(self, store=False):
        adv_links = list()
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            print(f'city: {city}, total: {len(links)}')
            adv_links.extend(links)
        if store:
            self.store([li.get('href') for li in adv_links])
        return adv_links

    def store(self, data, *args):
        with open('data/links.json', 'w') as file:
            file.write(json.dumps(data))


class DataCrawler(CrawlerBase):
    def __init__(self):
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()

    @staticmethod
    def __load_links():
        with open('data/links.json', 'r') as file:
            links = json.loads(file.read())
            return links

    def start(self, store=False):
        for link in self.links:
            response = self.get(link)
            data = self.parser.pars(response.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))

    def store(self, data, file_name):
        with open(f'data/adv/{file_name}.json', 'w') as file:
            file.write(json.dumps(data))
        print(f'data/adv/{file_name}.json')
