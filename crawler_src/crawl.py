import json
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from config import BASE_LINK, STORAGE_TYPE
from parser import AdvertisementPageParser
from storage import MongoStorage, FileStorage


class CrawlerBase(ABC):
    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == "mongo":
            return MongoStorage()
        return FileStorage()

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
        super().__init__()

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.find_all('a', attrs={'class': 'hdrlnk'})

    def start_crawl_city(self, url):
        start = 0
        crawl = True
        adv_links = list()
        while crawl:
            response = self.get(url + str(start))
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
            self.store([{'url': li.get('href'), 'flag': False} for li in adv_links])
        return adv_links

    def store(self, data, *args):
        self.storage.store(data, 'advertisement_links')


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()

    def __load_links(self):
        return self.storage.load('advertisement_links', {'flag': False})

    def start(self, store=False):
        for link in self.links:
            response = self.get(link['url'])
            data = self.parser.pars(response.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))

            self.storage.update_flag(link)
            print(link)

    def store(self, data, file_name):
        self.storage.store(data, 'advertisement_data')


class ImageDownloader(CrawlerBase):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.advertisements = self.__load_advertisements()

    def __load_advertisements(self):
        return self.storage.load('advertisement_data')

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, stream=True)
        except requests.HTTPError:
            return None
        return response

    def start(self, store=True):
        for advertisement in self.advertisements:
            for image in advertisement['images']:
                counter = 0
                response = self.get(image['url'])
                if store:
                    self.store(response, advertisement['post_id'], counter)
                counter += 1

    def store(self, data, adv_id, img_number):
        file_name = f'{adv_id}-{img_number}'
        return self.save_to_disk(data, file_name)

    def save_to_disk(self, response, file_name):
        with open(f'data/images/{file_name}.jpg', 'ab') as f:
            f.write(response.content)
            for _ in response.iter_content():
                f.write(response.content)

        print(file_name)
        return file_name
