import sys

from crawl import LinkCrawler

def get_pages_data():
    raise NotImplementedError()


if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == 'find_links':
        crawler = LinkCrawler(cities=['amsterdam', 'paris', 'london'])
        crawler.start()

    elif switch == 'extract_pages':
        get_pages_data()
